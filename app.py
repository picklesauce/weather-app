from flask import Flask, request, render_template_string
import requests
import os

app = Flask(__name__)
# Make sure to set your API key as an environment variable
API_KEY = os.getenv("WEATHER_API_KEY")

# --- COMPLETE HTML TEMPLATE WITH ALL IMPROVEMENTS ---

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Weather App</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
    
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Nunito:wght@400;500;700&display=swap" rel="stylesheet">

    <style>
        /* 4. Use a Friendlier Font */
        body {
            font-family: 'Nunito', sans-serif;
            transition: background-color 0.5s ease;
        }

        /* 1. Dynamic Background Colors */
        body { background: linear-gradient(to top, #d3d9e2, #e9ecf0); } /* Default */
        body.sunny { background: linear-gradient(to top, #89cff0, #cdeefd); }
        body.rainy { background: linear-gradient(to top, #a9b7c2, #dde3e9); }
        body.cloudy { background: linear-gradient(to top, #cfd9df, #e2ebf0); }

        .container { max-width: 800px; }
        .navbar-brand { font-weight: 500; }
        .weather-card {
            background: rgba(255, 255, 255, 0.7);
            backdrop-filter: blur(10px);
            border-radius: 1.5rem;
            border: 1px solid rgba(255, 255, 255, 0.2);
        }
        .current-weather h2 { font-weight: 500; font-size: 1.75rem; }
        .current-temp { font-size: 5rem; font-weight: 700; }
        .current-condition { font-size: 1.25rem; font-weight: 500; }
        .vr { opacity: 0.15; }
        
        /* 3. Add Subtle Hover Effects */
        .forecast-list-item {
            transition: background-color 0.2s ease, transform 0.2s ease;
            border-radius: 0.5rem;
            padding: 0.75rem;
        }
        .forecast-list-item:hover {
            background-color: rgba(0, 0, 0, 0.05);
            transform: scale(1.03);
        }
    </style>
</head>

{% set condition = weather['current']['condition']['text'] | lower if weather else '' %}
<body class="
    {% if 'sunny' in condition or 'clear' in condition %}
        sunny
    {% elif 'rain' in condition or 'drizzle' in condition or 'mist' in condition %}
        rainy
    {% elif 'cloudy' in condition or 'overcast' in condition %}
        cloudy
    {% endif %}
">
    <nav class="navbar bg-transparent border-bottom mb-4">
        <div class="container">
            <a class="navbar-brand" href="#">🌤️ Weather App</a>
        </div>
    </nav>

    <div class="container">
        <form method="POST" class="input-group mb-4 shadow-sm" style="border-radius: 0.75rem; overflow: hidden;">
            <input name="city" type="text" class="form-control form-control-lg border-0" placeholder="Enter city name (e.g., London)" required>
            <button type="submit" class="btn btn-primary px-4">Get Weather</button>
        </form>

        {% if weather %}
        <div class="card weather-card shadow-lg p-2 p-md-4">
            <div class="row g-0 align-items-center">
                <div class="col-md-6 p-4 current-weather">
                    <h2>{{ weather['location']['name'] }}, {{ weather['location']['country'] }}</h2>
                    <div class="d-flex align-items-center mt-3">
                        <img src="{{ weather['current']['condition']['icon'] }}" alt="icon" style="width: 100px; margin-right: 1rem;">
                        <div>
                            <span class="current-temp">{{ weather['current']['temp_c']|round|int }}°</span>
                            <p class="current-condition mb-0">{{ weather['current']['condition']['text'] }}</p>
                        </div>
                    </div>
                    <hr class="my-4">
                    <div class="row text-center">
                        <div class="col-6 mb-3">
                            🌡️
                            <div><small>Max Temp</small></div>
                            <strong>{{ weather['forecast']['forecastday'][0]['day']['maxtemp_c'] }}°C</strong>
                        </div>
                        <div class="col-6 mb-3">
                            💧
                            <div><small>Humidity</small></div>
                            <strong>{{ weather['current']['humidity'] }}%</strong>
                        </div>
                        <div class="col-6">
                            🌡️
                            <div><small>Min Temp</small></div>
                            <strong>{{ weather['forecast']['forecastday'][0]['day']['mintemp_c'] }}°C</strong>
                        </div>
                        <div class="col-6">
                            🌬️
                            <div><small>Wind</small></div>
                            <strong>{{ weather['current']['wind_kph'] }} kph</strong>
                        </div>
                    </div>
                </div>

                <div class="col-auto d-none d-md-block">
                    <div class="vr h-100"></div>
                </div>

                <div class="col-md-5 p-4">
                    <h4 class="mb-3">3-Day Forecast</h4>
                    <ul class="list-unstyled">
                        {% for day in weather['forecast']['forecastday'] %}
                        <li class="forecast-list-item d-flex justify-content-between align-items-center">
                            <span>{{ day['date'][-5:] }}</span>
                            <img src="{{ day['day']['condition']['icon'] }}" alt="icon" style="width: 40px;">
                            <span>{{ day['day']['maxtemp_c']|round|int }}° / {{ day['day']['mintemp_c']|round|int }}°</span>
                        </li>
                        {% endfor %}
                    </ul>
                </div>
            </div>
        </div>

        {% elif error %}
            <div class="alert alert-danger mt-3 shadow-sm">❌ {{ error }}</div>
        {% endif %}
    </div>
</body>
</html>
"""

# --- END OF HTML TEMPLATE ---

@app.route("/", methods=["GET", "POST"])
def index():
    weather = None
    error = None
    city_name = request.form.get("city") if request.method == "POST" else "Waterloo" # Default city
    
    if city_name:
        url = f"http://api.weatherapi.com/v1/forecast.json?key={API_KEY}&q={city_name}&days=3"
        try:
            response = requests.get(url)
            response.raise_for_status() 
            data = response.json()

            if "error" in data:
                error = data["error"]["message"]
            else:
                weather = data
        except requests.exceptions.RequestException as e:
            error = f"Could not connect to weather service: {e}"
        except Exception as e:
            error = f"An unexpected error occurred: {e}"
            
    return render_template_string(HTML, weather=weather, error=error)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
    