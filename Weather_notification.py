import requests
import json
from datetime import datetime, timedelta
import pytz
from twilio.rest import Client


account_sid= "YOUR TWILIO SID"
auth_token = "YOUR TWILIO TOKEN"
# Replace with your OpenWeatherMap API key and location coordinates
api_key = "YOUR OPENWEATHER KEY"
latitude = 6.257394  # Replace with the actual latitude of your location
longitude = 80.054769  # Replace with the actual longitude of your location

url = f'https://api.openweathermap.org/data/2.5/onecall?lat={latitude}&lon={longitude}&exclude=minutely,daily&units=metric&appid={api_key}'

response = requests.get(url)

if response.status_code == 200:
    data = json.loads(response.text)
    hourly_forecast = data.get('hourly', [])

    # Get the time zone from the API response
    api_timezone = pytz.timezone(data['timezone'])

    if hourly_forecast:
        weather_id_below_600 = False  # Initialize a flag

        for hour in hourly_forecast:
            timestamp = hour['dt']  # UNIX timestamp (in UTC)

            # Convert the timestamp to your local time zone
            utc_time = datetime.utcfromtimestamp(timestamp)
            local_time = utc_time.replace(tzinfo=pytz.UTC).astimezone(api_timezone)

            # Define the current time in your local time zone
            current_time = datetime.now(api_timezone)

            if local_time < current_time + timedelta(hours=12 ):
                temperature = hour['temp']  # Temperature in °C
                humidity = hour['humidity']  # Humidity as a percentage
                weather_id = hour['weather'][0]['id']  # Weather ID

                print(
                    f'Timestamp: {local_time.strftime("%Y-%m-%d %H:%M:%S")}, Temperature: {temperature}°C, Humidity: {humidity}%')

            if weather_id < 600:
                weather_id_below_600 = True

        # Check the weather condition flag
        if weather_id_below_600:
            client = Client(account_sid, auth_token)
            message = client.messages \
                .create(
                body="It's going rain today. Remember to bring an ☂️",
                from_="YOUR VIR NUMBER",
                to="YOUR NUMBER"
            )

            print(message.status)
    else:
        print("Hourly forecast data not available.")
else:
    print(f'Error: {response.status_code}')
