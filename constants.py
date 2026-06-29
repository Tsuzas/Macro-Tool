import os

TITLE = 'Macro Tool'

RESOLUTION = '300x300'

MAIN_MENU_TEXT = 'Welcome to the macro tool!\n''Choose an option:\n\n''[1] Record a macro\n''[2] See your macros\n''[3] Edit a macro\n''[4] Delete a macro\n''[5] Execute a macro\n''[8] Settings\n''[9] Exit\n'

DEFAULT_SETTINGS = {
            "delay_speed": 5,
            "macro_speed": 0.1,
            "loops": 1,
            "listener": "f10",
            "click": "f11"
        }


#CHANGES THE JSON PATH TO THE CURRENT FOLDER
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# JSON PATHS FOR SETTINGS AND SENTENCES
SETTINGS_PATH = os.path.join(BASE_DIR,"storage/", "settings.json")
SENTENCES_PATH = os.path.join(BASE_DIR,"storage/", "sentences.json")
ICON_PATH = os.path.join(BASE_DIR, "media", "icon.png")