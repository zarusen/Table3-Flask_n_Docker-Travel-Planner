import requests
import os

def get_lat_lng(api_key, city_name):
    geocode_url = "https://maps.googleapis.com/maps/api/geocode/json"
    
    params = {
        'address': city_name,
        'key': api_key
    }
    
    response = requests.get(geocode_url, params=params)
    
    if response.status_code == 200:
        result = response.json().get('results', [])
        if result:
            location = result[0]['geometry']['location']
            return location['lat'], location['lng']
        else:
            print("No results found for the city.")
            return None, None
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return None, None


def get_top_5_nearby_attractions(api_key, lat, lng, radius=1000, attraction_type='tourist_attraction'):
    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    
    params = {
        'location': f'{lat},{lng}',
        'radius': radius,
        'type': attraction_type,
        'key': api_key
    }
    
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        results = response.json().get('results', [])
        top_5_attractions = []
        
        # Slice the results to only get the top 5
        for place in results[:3]:
            name = place.get('name')
            address = place.get('vicinity')
            top_5_attractions.append({
                'name': name,
                'address': address,
            })
        
        return top_5_attractions
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return []
    
def get_restaurants(api_key, location):
    #api_key = load_api_key('api-key.txt')
    query = f"restaurants in {location}"  # Modify query to focus on restaurants
    url = f"https://maps.googleapis.com/maps/api/place/textsearch/json?query={query}&key={api_key}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check for HTTP errors
        restaurants = response.json().get('results', [])[:5]  # Get the top 5 restaurants
        
        if not restaurants:
            print("No restaurants found.")
            return
        
        print("Top 5 Restaurants in "+location+":")
        for restaurant in restaurants:
            name = restaurant.get('name')
            address = restaurant.get('formatted_address')
            print("Location: "+f"{name}, {address}")

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

def get_weather(api_key, location):
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        'q': location,
        'appid': api_key,
        'units': 'imperial'  # Use 'metric' for Celsius, 'imperial' for Fahrenheit
    }
    
    response = requests.get(base_url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        main = data['main']
        wind = data['wind']
        weather_desc = data['weather'][0]['description']
        
        
        print(f"Weather for: {location}")
        print(f"Temperature: {main['temp']}°F")
        print(f"Humidity: {main['humidity']}%")
        print(f"Weather: {weather_desc}")
        print(f"Wind Speed: {wind['speed']} m/s")
    else:
        print(f"Error: {response.status_code}, unable to retrieve weather data")


def main():
    # Exported keys for security


    ATR_API_KEY = os.environ.get('ATR_API_KEY')
    REST_API_KEY = os.environ.get('REST_API_KEY')
    WEA_API_KEY = os.environ.get('WEA_API_KEY')
    

    
    # Ask the user to enter a city
    city_name = input("Enter the city name: ")
    
    # Get the latitude and longitude of the city
    lat, lng = get_lat_lng(ATR_API_KEY, city_name)
    
    if lat and lng:
        print(f"Fetching top 3 attractions near {city_name}...\n")
        
        # Get the top 5 nearby attractions
        top_5_attractions = get_top_5_nearby_attractions(ATR_API_KEY, lat, lng)
        
        if top_5_attractions:
            for idx, attraction in enumerate(top_5_attractions, start=1):
                print(f"{idx}. Name: {attraction['name']}, Address: {attraction['address']}")
        else:
            print("No attractions found.")
    else:
        print("Unable to find the city coordinates.")
    print("----------------------------------")
    get_restaurants(REST_API_KEY, city_name)
    print("----------------------------------")
    get_weather(WEA_API_KEY, city_name)





if __name__ == "__main__":
    main()
