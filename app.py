import streamlit as st
import requests

st.set_page_config(page_title="Weather Clothing Recommender", page_icon="👕")

st.title("👕 Weather-Based Clothing Recommender")

# Function to get weather data from Open-Meteo
def get_weather(city):
    # Get coordinates for the city using Open-Meteo's geocoding API
    geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}"
    geo_response = requests.get(geo_url)
    if geo_response.status_code != 200 or not geo_response.json().get("results"):
        return None
    
    location = geo_response.json()["results"][0]
    lat, lon = location["latitude"], location["longitude"]

    # Get weather info
    weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m,precipitation"
    response = requests.get(weather_url)
    if response.status_code == 200:
        data = response.json()["current"]
        weather = {
            "city": location["name"],
            "temperature": data["temperature_2m"],
            "humidity": data["relative_humidity_2m"],
            "precipitation": data["precipitation"],
        }
        return weather
    else:
        return None

# Clothing recommendation logic
def recommend_clothing(temp, rain):
    if rain > 0:
        return "🌧️ Take an umbrella or raincoat — it might rain!"
    elif temp < 10:
        return "🧥 It's cold! Wear a warm jacket, sweater, and trousers."
    elif 10 <= temp < 20:
        return "👕 Cool weather! A light jacket or hoodie would work."
    elif 20 <= temp < 30:
        return "👚 Warm day — wear breathable clothes like t-shirts and jeans."
    else:
        return "🩳 Hot weather! Go for shorts, light cotton wear, and drink water."

# Input field
city = st.text_input("Enter a city name:", "")

# Button to fetch and recommend
if st.button("Get Recommendation"):
    if city:
        weather = get_weather(city)
        if weather:
            st.success(f"**City:** {weather['city']}")
            st.write(f"🌡️ **Temperature:** {weather['temperature']}°C")
            st.write(f"💧 **Humidity:** {weather['humidity']}%")
            st.write(f"🌧️ **Precipitation:** {weather['precipitation']} mm")

            recommendation = recommend_clothing(weather['temperature'], weather['precipitation'])
            st.subheader("👗 Clothing Recommendation:")
            st.info(recommendation)
        else:
            st.error("City not found or unable to fetch weather data.")
    else:
        st.warning("Please enter a city name.")
