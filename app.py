from flask import Flask, request, render_template_string
import requests
import os

app = Flask(__name__)
API_KEY = '2929177a1fd64a9c8d9101145251407'  

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Weather App</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body class="bg-light">
    <div class="container mt-5">
        <h1 class="mb-4">🌤️ Weather App</h1>
        <form method="POST" class="mb-3">
            <input name="city" class="form-control" placeholder="Enter city name" required>
            <button type="submit" class="btn btn-primary mt-2">Get Weather</button>
        </form>

        {% if weather %}
            <div class="card p-3 shadow-sm">
                <h2>Weather in {{ weather['location']['name'] }}, {{ weather['location']['country'] }}:</h2>
                <ul class="list-unstyled">
                    <li>🌡️ Temperature: {{ weather['current']['temp_c'] }}°C</li>
                    <li>🌥️ Condition: {{ weather['current']['condition']['text'] }}</li>
                    <li>💧 Humidity: {{ weather['current']['humidity'] }}%</li>
                    <li>🌬️ Wind: {{ weather['current']['wind_kph'] }} kph</li>
                </ul>
            </div>
        {% elif error %}
            <div class="alert alert-danger mt-3">❌ {{ error }}</div>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    weather = None
    error = None
    if request.method == "POST":
        city = request.form.get("city")
        url = f"http://api.weatherapi.com/v1/current.json?key={API_KEY}&q={city}"
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
