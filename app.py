import os
import streamlit as st
import requests
from datetime import date, timedelta

# -----------------------------
# CONFIG
# -----------------------------
st.set_page_config(page_title="Weather Forecast App", page_icon="🌦️", layout="centered")

RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY", "YOUR_RAPIDAPI_KEY_HERE")
RAPIDAPI_HOST = "weatherapi-com.p.rapidapi.com"

# -----------------------------
# APP HEADER
# -----------------------------
st.title("🌤️ Global Weather App")
st.caption("Powered by [WeatherAPI.com](https://rapidapi.com/weatherapi/api/weatherapi-com) via RapidAPI")

# -----------------------------
# USER INPUTS
# -----------------------------
st.sidebar.header("⚙️ Options")
mode = st.sidebar.radio("Select Mode:", ["Current Weather", "Forecast", "Historical"])
city = st.sidebar.text_input("Enter City:", "Accra")

# -----------------------------
# HELPER FUNCTION
# -----------------------------
def fetch_data(endpoint, params):
    url = f"https://{RAPIDAPI_HOST}/{endpoint}"
    headers = {
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": RAPIDAPI_HOST
    }
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Error {response.status_code}: {response.text}")
        return None

# -----------------------------
# MODE: CURRENT WEATHER
# -----------------------------
if mode == "Current Weather":
    st.subheader("🌤 Current Weather")
    if st.button("Get Current Weather"):
        params = {"q": city}
        data = fetch_data("current.json", params)
        if data:
            st.image(f"https:{data['current']['condition']['icon']}", width=80)
            st.metric("Temperature (°C)", data['current']['temp_c'])
            st.metric("Feels Like (°C)", data['current']['feelslike_c'])
            st.write(f"**Condition:** {data['current']['condition']['text']
