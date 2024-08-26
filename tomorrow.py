from flask import Flask, request, jsonify, render_template
import requests
from geopy.geocoders import Nominatim

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/weather', methods=['POST'])
def get_weather():
    data = request.json
    city = data.get('city')
    zipcode = data.get('zipcode')

    if not (city or zipcode):
        return jsonify({'error': 'City or Zipcode is required'}), 400

    # Convert city and zipcode to lat and long
    geolocator = Nominatim(user_agent="Suppperees weather dashboard")
    location = None
    if city:
        location = geolocator.geocode(city)
    if zipcode and not location:
        location = geolocator.geocode(zipcode)

    if location is None:
        return jsonify({'error': 'Location not found'}), 404

    lat, lon = location.latitude, location.longitude

    url = f"https://api.tomorrow.io/v4/weather/forecast?location={lat},{lon}&apikey=XJVVeLKtPt9BTUquispvrac4dxVf1rk3"
    response = requests.get(url)
    weather_data = response.json()
    daylist=[] # index 0 is today, index 1-4 is next 4 days 
    #goal, send back 1 of 5 possible values for the weather
    #this must be done for each day
    #day list will just be a list of integers, 0-4
    # 0 = sun
    # 1 = snow
    # 2 = raining
    # 3 = part cloud
    # 4 = cloud
    for day in weather_data['timelines']['daily']:
        curDay = {}
        curDay['temp'] = (day['values']['temperatureAvg'] * 1.8) +32 
        if day['values']['snowIntensityAvg'] > 0.05:
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
        elif cloud <= 60 and cloud >30:
            curDay['icon'] = 3
            daylist.append(curDay)
            continue
        else:
            curDay['icon'] = 0
            daylist.append(curDay)
        
    return jsonify({
        'days': daylist
    })

if __name__ == '__main__':
    app.run(debug=True)
