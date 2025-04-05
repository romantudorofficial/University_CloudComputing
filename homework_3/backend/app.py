from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return jsonify(message="Hello from Flask on Cloud Run!")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
