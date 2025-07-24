# 🌤️ Weather App (Flask + WeatherAPI)

A simple web app that displays the current weather and a 3-day forecast for any city using the [WeatherAPI](https://www.weatherapi.com/).

## Live Demo

[🌤️ View the live Weather‑App](https://weather-app-1-xet6.onrender.com/)

## 🚀 Features
- Current weather (temperature, wind, humidity, condition)
- 3-day forecast with weather icons
- Bootstrap-powered responsive UI
- Deployable to [Render](https://render.com)

## 🧪 Technologies
- Python 3
- Flask
- requests
- WeatherAPI

## 🛠️ Setup

1. Clone this repo:
   ```bash
   git clone https://github.com/your-username/weather-app.git
   cd weather-app
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set your environment variable:
   ```bash
   export WEATHER_API_KEY=your_api_key_here
   ```

4. Run the app:
   ```bash
   python app.py
   ```

Then go to [http://localhost:5000](http://localhost:5000) in your browser.

## 🌐 Deploy to Render

1. Push to GitHub
2. Go to [Render.com](https://render.com)
3. Click “New Web Service” → Connect GitHub → Select repo
4. Add environment variable:
   ```
   WEATHER_API_KEY=your_api_key
   ```
5. Use these commands:
   - Build command: `pip install -r requirements.txt`
   - Start command: `python app.py`

Done! 🎉

---
