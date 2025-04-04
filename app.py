from flask import Flask, render_template, request
import requests

app = Flask(__name__)
API_KEY = "3e9cdb9bf2644cc499795035250404"

@app.route("/", methods = ["GET", "POST"])

def index():
    weather_data = None
    error = None
    if request.method == "POST":
        location = request.form.get("location")
        if location:
            url =  f"http://api.weatherapi.com/v1/current.json?key={API_KEY}&q={location}&aqi=yes"


            try:
                response = requests.get(url)
                response.raise_for_status()
                data = response.json()

                weather_data = {
                    "location": f"{data['location']['name']}, {data['location']['country']}",
                    "condition": data['current']['condition']['text'],
                    "icon": data['current']['condition']['icon'],
                    "temp_c": data['current']['temp_c'],
                    "temp_f": data['current']['temp_f'],
                    "humidity": data['current']['humidity'],
                    "wind_kph": data['current']['wind_kph'],
                    "aqi": data['current']['air_quality']['pm2_5'],
                }
            
            except Exception as e:
                error = "Can't Fetch the weather data for the location, Sorry!!"
                print(e)
            
    return render_template("index.html", weather=weather_data, error=error)

if __name__ == "__main__":
    app.run(debug = True)
