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
            st.write(f"**Condition:** {data['current']['condition']['text']}")
            st.write(f"**Humidity:** {data['current']['humidity']}%")
            st.write(f"**Wind Speed:** {data['current']['wind_kph']} kph")
            st.write(f"**Location:** {data['location']['name']}, {data['location']['country']}")

# -----------------------------
# MODE: FORECAST
# -----------------------------
elif mode == "Forecast":
    st.subheader("📅 3-Day Weather Forecast")
    days = st.slider("Select number of days:", 1, 7, 3)
    if st.button("Get Forecast"):
        params = {"q": city, "days": days}
        data = fetch_data("forecast.json", params)
        if data:
            for day in data["forecast"]["forecastday"]:
                st.markdown(f"### {day['date']}")
                st.image(f"https:{day['day']['condition']['icon']}", width=80)
                st.metric("Avg Temp (°C)", day["day"]["avgtemp_c"])
                st.write(f"Condition: {day['day']['condition']['text']}")
                st.write(f"Max Temp: {day['day']['maxtemp_c']}°C | Min Temp: {day['day']['mintemp_c']}°C")
                st.divider()

# -----------------------------
# MODE: HISTORICAL
# -----------------------------
elif mode == "Historical":
    st.subheader("🕰 Historical Weather Data")
    selected_date = st.date_input(
        "Select Date:",
        value=date.today() - timedelta(days=1),
        max_value=date.today() - timedelta(days=1)
    )
    if st.button("Get Historical Weather"):
        params = {"q": city, "dt": selected_date.strftime("%Y-%m-%d")}
        data = fetch_data("history.json", params)
        if data:
            hist = data["forecast"]["forecastday"][0]
            st.markdown(f"### {hist['date']}")
            st.image(f"https:{hist['day']['condition']['icon']}", width=80)
            st.metric("Avg Temp (°C)", hist["day"]["avgtemp_c"])
            st.write(f"Condition: {hist['day']['condition']['text']}")
            st.write(f"Max Temp: {hist['day']['maxtemp_c']}°C | Min Temp: {hist['day']['mintemp_c']}°C")
            st.write(f"Total Precipitation: {hist['day']['totalprecip_mm']} mm")
