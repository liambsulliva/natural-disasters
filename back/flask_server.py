from flask import Flask, jsonify
import json
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET'])
def get_data():
    # Load data from the JSON file
    with open('events.json', 'r') as f:
        data = json.load(f)
    
    # Return the data as JSON response
    return jsonify(data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6969, debug=False)