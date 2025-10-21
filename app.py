import os
import streamlit as st
import requests

# Load API key from environment (for safety)
RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY", "YOUR_RAPIDAPI_KEY_HERE")
RAPIDAPI_HOST = "weatherapi-com.p.rapidapi.com"

st.set_page_config(page_title="Weather Forecast App", page_icon="🌦️", layout="centered")
st.title("🌤️ Simple Weather Forecast App")
st.write("Using WeatherAPI.com via RapidAPI")

city = st.text_input("Enter city name:", "Accra")

if st.button("Get Weather"):
    url = f"https://{RAPIDAPI_HOST}/timezone.json"
    querystring = {"q": city}
    headers = {
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": RAPIDAPI_HOST
    }

    response = requests.get(url, headers=headers, params=querystring)
    if response.status_code == 200:
        data = response.json()
        location = data["location"]["name"]
        country = data["location"]["country"]
        temp_c = data["current"]["temp_c"]
        condition = data["current"]["condition"]["text"]
        icon = data["current"]["condition"]["icon"]

        st.subheader(f"Weather in {location}, {country}")
        st.image(f"https:{icon}", width=80)
        st.metric(label="Temperature (°C)", value=temp_c)
        st.write(f"Condition: {condition}")
    else:
        st.error("Unable to fetch weather data. Please check city name or API key.")
