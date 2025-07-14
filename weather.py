import requests

def get_weather(city):
    API_KEY =  '2929177a1fd64a9c8d9101145251407'
    url = f"http://api.weatherapi.com/v1/current.json?key={API_KEY}&q={city}"

    print("Requesting:", url)  
    response = requests.get(url)
    data = response.json()

    if "error" in data:
        print("❌ Error:", data["error"]["message"])
        return

    print(f"🌤️ Weather in {data['location']['name']}, {data['location']['country']}:")
    print(f"Temperature: {data['current']['temp_c']}°C")
    print(f"Condition: {data['current']['condition']['text']}")
    print(f"Humidity: {data['current']['humidity']}%")
    print(f"Wind: {data['current']['wind_kph']} kph")

city = input("Enter city name: ")
get_weather(city)
