from flask import Flask, jsonify, request
import requests
from flask_cors import CORS
app = Flask(__name__)
CORS(app)


# If you have CORS issues (for development), you might install and use Flask-CORS:
# from flask_cors import CORS
# CORS(app)

# --------- Configuration ---------
# URL of your external books service:
BOOKS_SERVICE_URL = "http://localhost:8000/books"

# For the weather service we use Open-Meteo for London (for simplicity).
# Open-Meteo API example for London coordinates (latitude: 51.5074, longitude: -0.1278)
WEATHER_API_URL = "https://api.open-meteo.com/v1/forecast"
WEATHER_PARAMS = {
    "latitude": 51.5074,
    "longitude": -0.1278,
    "current_weather": True,
    "timezone": "Europe/London"
}

# ---------------------------------

@app.route('/api/books', methods=['GET'])
def get_books():
    """
    Calls the external Books Service to get all books.
    """
    try:
        response = requests.get(BOOKS_SERVICE_URL)
        # Forward the status code and response from the books service.
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({"error": f"Failed to retrieve books: {str(e)}"}), 500

@app.route('/api/author-info', methods=['GET'])
def get_author_info():
    """
    Calls Wikipedia's REST API to get a summary about the given author.
    Expect a query parameter "author".
    """
    author = request.args.get('author')
    if not author:
        return jsonify({"error": "Author parameter is required"}), 400

    # Wikipedia REST API endpoint (replace spaces with underscores)
    wiki_author = author.replace(" ", "_")
    url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{wiki_author}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return jsonify(response.json()), 200
        else:
            return jsonify({"error": "Could not retrieve author information"}), response.status_code
    except Exception as e:
        return jsonify({"error": f"Exception occurred: {str(e)}"}), 500

@app.route('/api/weather', methods=['GET'])
def get_weather():
    """
    Calls the weather API to get current weather data.
    (For simplicity, we're using fixed coordinates for London.)
    """
    # Optionally, you could allow a 'city' parameter and then map it to lat/long.
    try:
        response = requests.get(WEATHER_API_URL, params=WEATHER_PARAMS)
        if response.status_code == 200:
            return jsonify(response.json()), 200
        else:
            return jsonify({"error": "Could not retrieve weather information"}), response.status_code
    except Exception as e:
        return jsonify({"error": f"Exception occurred: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
