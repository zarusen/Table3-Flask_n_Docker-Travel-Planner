from flask import Flask, render_template, request, redirect, url_for
import requests

app = Flask(__name__)

# Google Places API key (replace with your actual API key)
GOOGLE_API_KEY = 'AIzaSyA4witeIUyn2Zu9cnEodZw698Y7qcgUquk'
GOOGLE_PLACES_TEXTSEARCH_URL = 'https://maps.googleapis.com/maps/api/place/textsearch/json'

@app.route('/', methods=['GET'])
def index():
    # Render the form for the user to input the location
    return render_template('index.html', restaurants=None)

@app.route('/restaurants', methods=['POST'])
def get_restaurants():
    location = request.form.get('location')  # Get the location from the form

    if not location:
        return redirect(url_for('index'))  # If no location is entered, redirect back to the form

    # Build the query string for the Places API
    query = f"restaurants in {location}"

    # Parameters for Google Places Text Search API
    params = {
        'query': query,
        'key': GOOGLE_API_KEY
    }

    # Make the request to the Google Places Text Search API
    response = requests.get(GOOGLE_PLACES_TEXTSEARCH_URL, params=params)

    if response.status_code != 200:
        return jsonify({"error": "Error fetching data from Google Places API."}), 500

    data = response.json()

    if 'results' not in data or len(data['results']) == 0:
        return render_template('index.html', restaurants=[], location=location)

    # Extract the names of the first 5 restaurants
    restaurant_names = [place.get('name') for place in data['results'][:5]]

    # Render the template with the restaurant names
    return render_template('index.html', restaurants=restaurant_names, location=location)


if __name__ == '__main__':
    app.run(
        debug=True,
        host='0.0.0.0',
        port=5000
    )
