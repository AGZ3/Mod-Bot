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
    """
    Reduces repeated characters in words to a single character.
    
    Example:
        Input:  "Heeeeellloooo wooorllddd"
        Output: "Helo world"
    """
    # This regex replaces any character that repeats more than twice with a single instance
    normalized_message = re.sub(r'(.)\1+', r'\1', message)
    return normalized_message

