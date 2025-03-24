import json, requests
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app)  # Enable CORS for all routes
HEADERS = {"User-Agent": "Mozilla/5.0"}
# Dictionary to store the next 10 words for each query length
autocomplete_suggestions = []
@app.route('/')
def index():
    return app.send_static_file('layout.html')

@app.route('/v1/autocomplete', methods=['GET'])
def autocomplete():
    query = request.args.get('query', '').lower()
    
    # Get suggestions based on query
    suggestions = requests.request(method="GET", url=f"http://35.200.185.69:8000/v1/autocomplete?query", params={"query": query}, headers=HEADERS).json()["results"]
    
    # Format suggestions in the same structure expected by the frontend
    formatted_suggestions = [
        {
            "title": suggestion,
            "desc": f"Search results for '{suggestion}'"
        }
        for suggestion in suggestions
    ]
    
    return jsonify(formatted_suggestions)

if __name__ == '__main__':
    app.run(debug=True, port=8000)
