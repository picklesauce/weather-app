from flask import Flask, request, render_template_string
import requests
import os

app = Flask(__name__)
API_KEY = os.getenv("WEATHER_API_KEY")  # Set this in your environment variables

# Improved HTML template with better Bootstrap-based UI
HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Weather App</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
      body { background-color: #f0f4f8; }
      .card { border-radius: 1rem; }
      .current-card img { width: 100px; }
      .forecast-card img { width: 60px; }
      .input-group .form-control { border-top-left-radius: 1rem; border-bottom-left-radius: 1rem; }
      .input-group .btn { border-top-right-radius: 1rem; border-bottom-right-radius: 1rem; }
    </style>
</head>
<body>
  <nav class="navbar navbar-expand-lg navbar-light bg-white shadow-sm">
    <div class="container">
      <a class="navbar-brand" href="#">🌤️ Weather App</a>
    </div>
  </nav>

  <div class="container my-5">
    <form method="POST" class="input-group mb-4 shadow-sm">
      <input name="city" type="text" class="form-control" placeholder="Enter city name" required>
      <button type="submit" class="btn btn-primary">Get Weather</button>
    </form>

    {% if weather %}
      <div class="card current-card mb-5 shadow-sm p-4 text-center">
        <h2>Now in {{ weather['location']['name'] }}, {{ weather['location']['country'] }}</h2>
        <div class="d-flex justify-content-center align-items-center mt-3 gap-4">
          <img src="{{ weather['current']['condition']['icon'] }}" alt="icon">
          <ul class="list-unstyled mb-0 text-start">
            <li>🌡️ <strong>{{ weather['current']['temp_c'] }}°C</strong></li>
            <li>🌥️ {{ weather['current']['condition']['text'] }}</li>
            <li>💧 {{ weather['current']['humidity'] }}% Humidity</li>
            <li>🌬️ {{ weather['current']['wind_kph'] }} kph</li>
          </ul>
        </div>
      </div>

      <h3 class="mb-3">📅 3-Day Forecast</h3>
      <div class="d-flex flex-wrap justify-content-between gap-3">
        {% for day in weather['forecast']['forecastday'] %}
          <div class="card forecast-card flex-fill shadow-sm p-3 text-center" style="min-width: 220px; max-width: 250px;">
            <h5 class="mb-2">{{ day['date'] }}</h5>
            <img src="{{ day['day']['condition']['icon'] }}" alt="icon">
            <p class="mt-2 mb-1">{{ day['day']['condition']['text'] }}</p>
            <p class="mb-1">🌡️ <small>Max:</small> {{ day['day']['maxtemp_c'] }}°C</p>
            <p class="mb-1">🌡️ <small>Min:</small> {{ day['day']['mintemp_c'] }}°C</p>
            <p class="mb-0">💧 {{ day['day']['avghumidity'] }}% Humidity</p>
          </div>
        {% endfor %}
      </div>

    {% elif error %}
      <div class="alert alert-danger mt-3 shadow-sm">❌ {{ error }}</div>
    {% endif %}
  </div>

  <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    weather = None
    error = None
    if request.method == "POST":
        city = request.form.get("city")
        url = f"http://api.weatherapi.com/v1/forecast.json?key={API_KEY}&q={city}&days=3"
        response = requests.get(url)
        data = response.json()

        if "error" in data:
            error = data["error"]["message"]
        else:
            weather = data

    return render_template_string(HTML, weather=weather, error=error)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
    
