import json
import requests
from geopy.geocoders import Nominatim

def lambda_handler(event, context):
    try:
        # Extract city and zipcode from the request body
        data = json.loads(event['body'])
        city = data.get('city')
        zipcode = data.get('zipcode')

        if not (city or zipcode):
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'City or Zipcode is required'})
            }

        # Convert city and zipcode to lat and long
        geolocator = Nominatim(user_agent="Suppperees weather dashboard")
        location = None
        if city:
            location = geolocator.geocode(city)
        if zipcode and not location:
            location = geolocator.geocode(zipcode)

        if location is None:
            return {
                'statusCode': 404,
                'body': json.dumps({'error': 'Location not found'})
            }

        lat, lon = location.latitude, location.longitude

        # Fetch weather data using Tomorrow.io API
        url = f"https://api.tomorrow.io/v4/weather/forecast?location={lat},{lon}&apikey=XJVVeLKtPt9BTUquispvrac4dxVf1rk3"
        response = requests.get(url)
        weather_data = response.json()

        # Process the weather data
        daylist = []
        for day in weather_data['timelines']['daily']:
            curDay = {}
            curDay['temp'] = (day['values']['temperatureAvg'] + 32) * 1.8
            if day['values']['snowIntensity'] > 0.05:
                curDay['icon'] = 1
                daylist.append(curDay)
                continue
            if day['values']['precipitationProbabilityAvg'] > 40:
                curDay['icon'] = 2
                daylist.append(curDay)
                continue
            cloud = day['values']['cloudCoverAvg']
            if cloud > 60:
                curDay['icon'] = 4
                daylist.append(curDay)
                continue
            elif cloud <= 60 and cloud > 30:
                curDay['icon'] = 3
                daylist.append(curDay)
                continue
            else:
                curDay['icon'] = 0
                daylist.append(curDay)

        # Return the response
        return {
            'statusCode': 200,
            'body': json.dumps({'days': daylist})
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
