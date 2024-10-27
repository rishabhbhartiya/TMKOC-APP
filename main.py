from flask import Flask, request, jsonify, render_template
import pandas as pd

app = Flask(__name__)

# Load the data
df = pd.read_csv('TMKOC_MODEL_DATA_with_keywords.csv')

# Search function for episodes based on keywords
def find_episodes(keywords):
    keywords = [kw.strip().lower() for kw in keywords.split(',')]
    
    # Filter based on single or multiple keywords
    if len(keywords) == 1:
        # Single keyword - list all matching episodes
        matches = df[df['all keywords'].str.contains(keywords[0], case=False, na=False)]
    else:
        # Multiple keywords - match episodes with all keywords
        matches = df[df['all keywords'].apply(lambda x: all(kw in x.lower() for kw in keywords) if pd.notnull(x) else False)]
        
    return matches[['episode_number', 'Episode_title']].to_dict(orient='records')

# Home route to render the main page with HTML
@app.route('/')
def home():
    return render_template('index.html')

# Search route for AJAX requests
@app.route('/search', methods=['POST'])
def search():
    keywords = request.json.get('keywords', '')
    episodes = find_episodes(keywords)
    return jsonify({"episodes": episodes})

if __name__ == '__main__':
    app.run(debug=True)
