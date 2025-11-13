import streamlit as st
import requests

# ---------- CONFIG ----------
API_KEY = "de626dfff0b29cea814545cb47bdce09"
BASE_URL = "http://api.openweathermap.org/data/2.5/weather?"

# ---------- FUNCTION TO GET WEATHER ----------
def get_weather(city):
    url = f"{BASE_URL}q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        weather = {
            "city": data["name"],
            "temperature": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "description": data["weather"][0]["description"],
        }
        return weather
    else:
        return None

# ---------- FUNCTION TO RECOMMEND CLOTHES ----------
def recommend_clothing(temp, weather_desc):
    if "rain" in weather_desc.lower():
        return "🌧️ Carry an umbrella and wear waterproof clothing!"
    elif temp < 10:
        return "🧥 It's cold! Wear a jacket, sweater, and warm pants."
    elif 10 <= temp < 20:
        return "👕 Light jacket or hoodie should work fine."
    elif 20 <= temp < 30:
        return "👚 Comfortable casual wear like t-shirts and jeans."
    else:
        return "🩳 It's hot! Go for shorts, light cotton clothes, and stay hydrated."

# ---------- STREAMLIT UI ----------
st.set_page_config(page_title="Weather Clothing Recommender", page_icon="👕")
st.title("👕 Weather-Based Clothing Recommender")

city = st.text_input("Enter a city name:", "")

if st.button("Get Recommendation"):
    if city:
        weather = get_weather(city)
        if weather:
            st.success(f"**City:** {weather['city']}")
            st.write(f"🌡️ **Temperature:** {weather['temperature']}°C")
            st.write(f"💧 **Humidity:** {weather['humidity']}%")
            st.write(f"🌥️ **Condition:** {weather['description'].capitalize()}")
            
            recommendation = recommend_clothing(weather['temperature'], weather['description'])
            st.subheader("👗 Clothing Recommendation:")
            st.info(recommendation)
        else:
            st.error("City not found. Please enter a valid city name.")
    else:
        st.warning("Please enter a city name first.")
