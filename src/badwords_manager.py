# badwords_manager.py

import json
import os
import re

# Construct the path to badwords.json
BADWORDS_PATH = os.path.join('data', 'badwords.json')

# Function to load bad words from JSON
def load_badwords():
    try:
        with open(BADWORDS_PATH, 'r') as file:
            data = json.load(file)
            return data['badwords']
    except FileNotFoundError:
        return []

def save_badwords(badwords):
    with open(BADWORDS_PATH, 'w') as file:
        json.dump({"badwords": badwords}, file, indent=4)

def normalize_message(message):
    # Convert to lowercase and remove non-alphanumeric characters
    cleaned = re.sub(r'[^a-z0-9\s]', '', message.lower())
    # Reduce repeated characters (e.g., "shiiit" → "shit")
    return re.sub(r'(.)\1+', r'\1', cleaned)

