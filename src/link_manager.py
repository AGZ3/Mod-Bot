import json
import os

links = [
    '.com', 
    '.net',  
    '.ru', 
    '.io', 
    '.org',
    '.en'
    ]

TOGGLE_STATE_PATH = os.path.join('data', 'toggle_state.json')
PENDING_LINKS_PATH = os.path.join('data', 'pending_links.json')

#### LOAD PENDING LINKS JSON ####

def load_pending_links():
    try:
        with open(PENDING_LINKS_PATH, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

#### SAVE PENDING LINKS TO JSON ####

def save_pending_links(pending_links):
    with open(PENDING_LINKS_PATH, 'w') as file:
        json.dump(pending_links, file, indent=4)

#### REMOVE PENDING LINKS FROM JSON ####

def remove_pending_link(user_id):
    pending_links = load_pending_links()
    
    # Convert user_id to str for consistency, as JSON keys are always strings
    user_id_str = str(user_id)
    
    # Remove the link if it exists
    if user_id_str in pending_links:
        del pending_links[user_id_str]
        save_pending_links(pending_links)
        return True  # Return True to indicate successful removal
    return False  # Return False if there was nothing to remove

def get_toggle_state():
    try:
        with open(TOGGLE_STATE_PATH, 'r') as file:
            data = json.load(file)
            return data.get('pending_links_toggle', 1)  # Default to 1 (on) if not found
    except FileNotFoundError:
        return 1  # Default to on if file not found

def set_toggle_state(state):
    with open(TOGGLE_STATE_PATH, 'w') as file:
        json.dump({'pending_links_toggle': state}, file)


#### WHITELIST LINK LIST ADMIN CAN ADD/REMOVE