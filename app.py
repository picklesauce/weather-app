from flask import Flask, request, render_template_string
import requests
import os

app = Flask(__name__)
# MAKE SURE TO SET YOUR API KEY HERE
API_KEY = os.getenv("WEATHER_API_KEY")


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
    <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap" rel="stylesheet">
    <style>
        body {
            background-color: #e9ecef; /* Lighter gray background */
            font-family: 'Roboto', sans-serif;
        }
        .container {
            max-width: 800px; /* Constrain width for better readability */
        }
        .navbar-brand {
            font-weight: 500;
        }
        .weather-card {
            background: linear-gradient(135deg, #ffffff 0%, #f7f9fc 100%);
            border-radius: 1.5rem;
            border: none;
        }
        .current-weather h2 {
            font-weight: 500;
            font-size: 1.75rem;
        }
        .current-temp {
            font-size: 5rem; /* Big temperature */
            font-weight: 700;
        }
        .current-condition {
            font-size: 1.25rem;
            font-weight: 500;
        }
        .details-list li {
            font-size: 1rem;
            color: #555;
        }
        .forecast-list-item {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 0.75rem 0;
            border-bottom: 1px solid #dee2e6;
        }
        .forecast-list-item:last-child {
            border-bottom: none;
        }
        .forecast-day {
            font-weight: 500;
        }
        .forecast-temp {
            font-weight: 500;
            color: #333;
        }
        .vr {
            opacity: 0.15;
        }
    </style>
</head>
<body>
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
            <div class="row g-0">
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
                    <ul class="list-unstyled details-list">
                        <li><strong>Max Temp:</strong> {{ weather['forecast']['forecastday'][0]['day']['maxtemp_c'] }}°C</li>
                        <li><strong>Min Temp:</strong> {{ weather['forecast']['forecastday'][0]['day']['mintemp_c'] }}°C</li>
                        <li><strong>Humidity:</strong> {{ weather['current']['humidity'] }}%</li>
                        <li><strong>Wind:</strong> {{ weather['current']['wind_kph'] }} kph</li>
                    </ul>
                </div>

                <div class="col-auto d-none d-md-block">
                    <div class="vr h-100"></div>
                </div>

                <div class="col-md-5 p-4">
                    <h4 class="mb-3">3-Day Forecast</h4>
                    <ul class="list-unstyled forecast-list">
                        {% for day in weather['forecast']['forecastday'] %}
                        <li class="forecast-list-item">
                            <span class="forecast-day">{{ day['date'][-5:] }}</span> {# Show just MM-DD #}
                            <img src="{{ day['day']['condition']['icon'] }}" alt="icon" style="width: 40px;">
                            <span class="forecast-temp">{{ day['day']['maxtemp_c']|round|int }}° / {{ day['day']['mintemp_c']|round|int }}°</span>
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
# --- COPY TO HERE ---

@app.route("/", methods=["GET", "POST"])
def index():
    weather = None
    error = None
    city_name = request.form.get("city") if request.method == "POST" else "Waterloo" # Default to Waterloo
    
    if city_name:
        url = f"http://api.weatherapi.com/v1/forecast.json?key={API_KEY}&q={city_name}&days=3"
        try:
            response = requests.get(url)
            response.raise_for_status() # Raise an exception for bad status codes
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