import streamlit as st
import requests

st.set_page_config(page_title="Weather Clothing Recommender", page_icon="👕")

st.title("👕 Weather-Based Clothing Recommender")
st.write("This App is created by Tanuj Jain")
# ---------- FUNCTION TO GET WEATHER ----------
def get_weather(city):
    # Get coordinates for the city using Open-Meteo's geocoding API
    geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}"
    geo_response = requests.get(geo_url)
    if geo_response.status_code != 200 or not geo_response.json().get("results"):
        return None
    
    location = geo_response.json()["results"][0]
    lat, lon = location["latitude"], location["longitude"]

    # Get extended weather info
    weather_url = (
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={lat}&longitude={lon}"
        f"&current=temperature_2m,apparent_temperature,relative_humidity_2m,"
        f"precipitation,cloud_cover,wind_speed_10m,wind_direction_10m,weather_code"
    )

    response = requests.get(weather_url)
    if response.status_code == 200:
        data = response.json().get("current", {})
        weather = {
            "city": location["name"],
            "temperature": data.get("temperature_2m"),
            "feels_like": data.get("apparent_temperature"),
            "humidity": data.get("relative_humidity_2m"),
            "precipitation": data.get("precipitation"),
            "cloud_cover": data.get("cloud_cover"),
            "wind_speed": data.get("wind_speed_10m"),
            "wind_direction": data.get("wind_direction_10m"),
            "weather_code": data.get("weather_code"),
        }
        return weather
    else:
        return None

# ---------- WEATHER CODE DESCRIPTION ----------
WEATHER_CODES = {
    0: "☀️ Clear sky",
    1: "🌤️ Mainly clear",
    2: "⛅ Partly cloudy",
    3: "☁️ Overcast",
    45: "🌫️ Fog",
    48: "🌫️ Depositing rime fog",
    51: "🌦️ Light drizzle",
    61: "🌧️ Rain",
    71: "🌨️ Snow fall",
    80: "🌦️ Rain showers",
    95: "⛈️ Thunderstorm",
}

# ---------- CLOTHING RECOMMENDATION ----------
def recommend_clothing(temp, rain, wind_speed, weather_code):
    if rain > 0 or weather_code in [61, 80, 95]:
        return "🌧️ Carry an umbrella or wear waterproof clothes."
    elif temp < 10:
        return "🧥 It's cold — wear a thick jacket, sweater, and warm pants."
    elif 10 <= temp < 20:
        return "👕 Mild weather — a light hoodie or jacket works fine."
    elif 20 <= temp < 30:
        return "👚 Warm day — go for breathable cotton clothes."
    else:
        return "🩳 Hot day — wear shorts and stay hydrated."

# ---------- STREAMLIT UI ----------
city = st.text_input("Enter a city name:", "")

if st.button("Get Recommendation"):
    if city:
        weather = get_weather(city)
        if weather:
            st.success(f"**City:** {weather['city']}")
            st.write(f"🌡️ **Temperature:** {weather['temperature']}°C")
            st.write(f"🥵 **Feels Like:** {weather['feels_like']}°C")
            st.write(f"💧 **Humidity:** {weather['humidity']}%")
            st.write(f"🌧️ **Precipitation:** {weather['precipitation']} mm")
            st.write(f"☁️ **Cloud Cover:** {weather['cloud_cover']}%")
            st.write(f"💨 **Wind Speed:** {weather['wind_speed']} km/h")
            st.write(f"🧭 **Wind Direction:** {weather['wind_direction']}°")
            
            desc = WEATHER_CODES.get(weather['weather_code'], "🌈 Weather data unavailable")
            st.write(f"🌥️ **Condition:** {desc}")

            recommendation = recommend_clothing(
                weather['temperature'], weather['precipitation'], weather['wind_speed'], weather['weather_code']
            )
            st.subheader("👗 Clothing Recommendation:")
            st.info(recommendation)
        else:
            st.error("City not found or weather data unavailable.")
    else:
        st.warning("Please enter a city name.")