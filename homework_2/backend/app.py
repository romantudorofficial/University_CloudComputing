from flask import Flask, jsonify, request
from flask_cors import CORS
import requests



# Create the Flask application.

app = Flask(__name__)
CORS(app)



# Get the Books Service.

BOOKS_SERVICE_URL = "http://localhost:8000/books"



# Get the Weather Service.

WEATHER_API_URL = "https://api.open-meteo.com/v1/forecast"

WEATHER_PARAMS = {
    "latitude": 47.1738775658356,
    "longitude": 27.574806233895167,
    "current_weather": True,
    "timezone": "Europe/Bucharest"
}



@app.route('/api/books', methods = ['GET'])

def get_books ():

    '''
        Gets all the books.
    '''

    try:

        response = requests.get(BOOKS_SERVICE_URL)

        return jsonify(response.json()), response.status_code
    
    except Exception as e:

        return jsonify({"error": f"Failed to retrieve books: {str(e)}"}), 500



@app.route('/api/author-info', methods = ['GET'])

def get_author_info ():

    '''
        Gets the information about an author.
    '''

    author = request.args.get('author')

    if not author:
        return jsonify({"error": "Author parameter is required"}), 400

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



@app.route('/api/weather', methods = ['GET'])

def get_weather ():

    '''
        Gets the weather information.
    '''

    try:

        response = requests.get(WEATHER_API_URL, params = WEATHER_PARAMS)

        if response.status_code == 200:
            return jsonify(response.json()), 200
        else:
            return jsonify({"error": "Could not retrieve weather information"}), response.status_code
        
    except Exception as e:

        return jsonify({"error": f"Exception occurred: {str(e)}"}), 500



if __name__ == '__main__':
    
    app.run(debug = True, port = 5000)