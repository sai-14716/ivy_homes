import json
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

app = Flask(__name__, static_folder='.', static_url_path='http://35.200.185.69:8000/v1/autocomplete')
CORS(app)  # Enable CORS for all routes

# Dictionary to store the next 10 words for each query length
autocomplete_suggestions = {
    "w": ["web", "why", "what", "where", "when", "who", "which", "workout", "weather", "world"],
    "wh": ["what", "where", "when", "why", "which", "who", "whether", "whole", "while", "white"],
    "wha": ["what", "what's", "whatever", "what is", "what are", "what if", "what time", "what does", "what happened", "what about"],
    "what": ["what", "what's", "what is", "what are", "what if", "what time", "what does", "what happened", "what about", "what should"],
    # Add more example search terms
    "web": ["web design", "web development", "website builder", "web hosting", "web designer", "web browser", "web series", "web api", "webpack", "webinar"],
    "ph": ["photography", "phone", "philosophy", "phantom", "phoenix", "photoshop", "physics", "phrase", "photo", "philanthropy"],
    "de": ["design", "depression", "development", "definition", "deep learning", "default", "delivery", "denmark", "description", "democracy"]
}

@app.route('/')
def index():
    return app.send_static_file('layout.html')

@app.route('/v1/autocomplete', methods=['GET'])
def autocomplete():
    query = request.args.get('query', '').lower()
    
    # Get suggestions based on query
    if query in autocomplete_suggestions:
        suggestions = autocomplete_suggestions[query]
    else:
        # Try to find the closest prefix match
        matches = []
        for prefix in autocomplete_suggestions:
            if query.startswith(prefix):
                matches.append(prefix)
            elif prefix.startswith(query):
                matches.append(prefix)
        
        if matches:
            # Get the closest match by length
            closest_match = max(matches, key=len) if query.startswith(matches[0]) else min(matches, key=len)
            suggestions = autocomplete_suggestions[closest_match]
        else:
            suggestions = []
    
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