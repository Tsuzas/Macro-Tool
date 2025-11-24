# Keyboard Macro Tool

A simple Python GUI application for creating and executing keyboard macros to automate repetitive typing tasks.

## Features

-  **Record text macros** - Save frequently used text sentences
-  **View all macros** - See your entire macro list
-  **Edit macros** - Update existing macros
-  **Execute macros** - Automatically type saved text with a 5-second delay
-  **Persistent storage** - Macros saved to JSON file
-  **Clean GUI** - Simple tkinter interface

## Screenshots

*( FUTURE PRINTSCREEN OF THE APPLICATION )*

## Requirements

- Python 3.x
- pynput library

## Installation

### Option 1: Download executable (Windows only)

Download the latest `.exe` from the [Releases](https://github.com/Tsuzas/macro-tool/releases) page.

### Option 2: Run from source

1. Clone this repository:
```bash
git clone https://github.com/Tsuzas/macro-tool.git
cd macro-tool
```

2. Install dependencies:
```bash
pip install pynput
```

3. Run the application:
```bash
python KeyRecUI.py
```


## Usage

1. **Record a macro**: Choose option [1], type your text, and click "Add Macro"
2. **View macros**: Choose option [2] to see all saved macros
3. **Edit a macro**: Choose option [3], select the macro to edit
4. **Execute a macro**: Choose option [4], select which macro to type, then switch to your target window within 5 seconds

## How It Works

The tool stores your text macros in a `sentences.json` file and uses the `pynput` library to simulate keyboard input when executing macros.

## Future Plans

-  Mouse macro support ( clicks, movements )
-  Hotkey triggers for quick macro execution ( Shortcut for macro activation )
-  Macro loops and custom delays ( Repeat x times, and activate after Y seconds )
-  Special key combinations ( Ctrl, Alt, etc. )

## License

This project is not licensed – see the LICENSE file for details or check https://unlicense.org/.

## Author

[Fernando Pereira] - [Tsuzas]
