from flask import Flask, render_template, request, redirect, url_for
import requests

app = Flask(__name__)

# Google Places API key (replace with your actual API key)
GOOGLE_API_KEY = 'AIzaSyA4witeIUyn2Zu9cnEodZw698Y7qcgUquk'
GOOGLE_PLACES_TEXTSEARCH_URL = 'https://maps.googleapis.com/maps/api/place/textsearch/json'

@app.route('/', methods=['GET'])
def index():
    # Render the form for the user to input the location
    return render_template('index.html', restaurants=None, attractions=None)

@app.route('/places', methods=['POST'])
def get_places():
    location = request.form.get('location')  # Get the location from the form

    if not location:
        return redirect(url_for('index'))  # If no location is entered, redirect back to the form

    # Build the queries for both restaurants and attractions
    restaurant_query = f"restaurants in {location}"
    attraction_query = f"tourist attractions in {location}"

    # Parameters for Google Places Text Search API
    params = {
        'key': GOOGLE_API_KEY
    }

    # Fetch restaurants
    restaurant_params = params.copy()
    restaurant_params['query'] = restaurant_query
    restaurant_response = requests.get(GOOGLE_PLACES_TEXTSEARCH_URL, params=restaurant_params)

    # Check if request is successful for restaurants
    if restaurant_response.status_code != 200:
        return render_template('index.html', error="Error fetching data for restaurants.", restaurants=None, attractions=None)

    restaurant_data = restaurant_response.json()

    # Extract restaurant details (name, address, rating)
    restaurants = []
    if 'results' in restaurant_data:
        for place in restaurant_data['results'][:5]:  # Limit to 5 restaurants
            restaurant = {
                'name': place.get('name'),
                'address': place.get('formatted_address'),
                'rating': place.get('rating', 'N/A')
            }
            restaurants.append(restaurant)

    # Fetch attractions
    attraction_params = params.copy()
    attraction_params['query'] = attraction_query
    attraction_response = requests.get(GOOGLE_PLACES_TEXTSEARCH_URL, params=attraction_params)

    # Check if request is successful for attractions
    if attraction_response.status_code != 200:
        return render_template('index.html', error="Error fetching data for attractions.", restaurants=None, attractions=None)

    attraction_data = attraction_response.json()

    # Extract attraction details (name, address, rating)
    attractions = []
    if 'results' in attraction_data:
        for place in attraction_data['results'][:5]:  # Limit to 5 attractions
            attraction = {
                'name': place.get('name'),
                'address': place.get('formatted_address'),
                'rating': place.get('rating', 'N/A')
            }
            attractions.append(attraction)

    # Render the template with both restaurants and attractions
    return render_template('index.html', restaurants=restaurants, attractions=attractions, location=location)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
