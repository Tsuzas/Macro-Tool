#  CURRENTLY NOT WORKING, UNDER DEVELOPMENT



import json
import os



#CHANGES THE JSON PATH TO THE CURRENT FOLDER
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# JSON PATHS FOR SETTINGS AND SENTENCES
settings_path = os.path.join(BASE_DIR, "settings.json")
sentences_path = os.path.join(BASE_DIR, "sentences.json")

def load_json(file_path):
    
    default = {}

    if not os.path.exists(file_path):
        return default

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return default
    
def save_json(file_path, data):
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)