import sys
import json
import time
import tkinter as tk
from pynput.keyboard import Controller, Key
from tkinter import simpledialog, messagebox

# Quick function to clear Input field where user types
def clearInput():
    global userOption
    userOption.delete(0, tk.END)

# Saves macro by appending on array then pushing to Json
def saveMacro(event=None):
    global sentenceList, userOption
    if (userOption.get() == ""):
        messagebox.showinfo("Aborted", "Field was empty.\nReturning...")
    else:
        macro = userOption.get()
        sentenceList.append(macro)
        with open("sentences.json", "w") as f:
            json.dump(sentenceList, f)
        messagebox.showinfo("Saved", f"Macro saved: {macro}")
        clearInput()
    
    goBackMenu()

# Shows All Macros, edits from input then pushes to array, and Json
def editMacro():
    global sentenceList
    infoText = "\n".join(f"[{i}] --> {word}" for i, word in enumerate(sentenceList))

    macroEdit = simpledialog.askinteger("Macro List", f"Choose the macro you wish to edit:\n{infoText}")
    if macroEdit is None:
        messagebox.showinfo("Cancelled", "No input or invalid input.")
    elif 0 <= macroEdit < len(sentenceList):
        editMode = simpledialog.askstring("Macro Editor", f"Edit this macro:\n{sentenceList[macroEdit]}")
        if not editMode:
            messagebox.showinfo("Canceled", "Empty input. Leaving...")
        else:
            sentenceList[macroEdit] = editMode
            with open("sentences.json", "w") as f:
                json.dump(sentenceList, f)
            messagebox.showinfo("Edited", "Macro edited successfully!")
    else:
        messagebox.showinfo("Error", "Invalid index.")

# === LOAD SETTINGS ===
#     # VIA jSon #
def loadSettings():
    try:
        with open("settings.json", "r") as f:
            return json.load(f)
    except:
        # Default values if file doesn't exist
        return {
            "delay_speed": 5,
            "macro_speed": 0.1,
            "loops": 1
        }

# Setting Macro, defines time for input, input speed, and repeats?
def saveSettings():
    global settingList, delayOption, macroSpeedOption, loopOption, delayWindow, macroSpeed, loop, delayWindow

    settingList = {}  # clean list


    # =================== DELAY SPEED SETTINGS ========================== #
    delayHolder = delayOption.get()
    if delayHolder == "Default is: 5 seconds." or delayHolder == "":
        delayWindow = 5.0
        messagebox.showinfo("Empty Field Detected", "Delay empty → Defaulting to 5 seconds.")
    else:
        delayWindow = float(delayHolder)

    settingList["delay_speed"] = delayWindow  
    # =================================================================== #

    # ====================== MACRO SPEEDSETTINGS ======================= #
    macroHolder = macroSpeedOption.get()
    if macroHolder == "Default is: 0.1 second."or macroHolder == "":
        macro = 0.1
        messagebox.showinfo("Empty Field Detected", "Macro speed empty → Defaulting to 0.1 seconds.")
    else:
        macro = float(macroHolder)
    
    settingList["macro_speed"] = macro
    # =================================================================== #

    # ========================== LOOPS SETTINGS ======================= #
    loopHolder = loopOption.get()
    if loopHolder == "Default is: 1 loop." or loopHolder == "":
        loop = 1
        messagebox.showinfo("Empty Field Detected", "Loop empty → Defaulting to 1 seconds.")
    else:
        loop = float(loopHolder)
   
    settingList["loops"] = loop
    # =================================================================== #

    # Saves JSON
    with open("settings.json", "w") as f:
        json.dump(settingList, f, indent=4)

    messagebox.showinfo("Saved", "Settings saved successfully!")

    delayWindow.pack_forget()
    delayOption.pack_forget()
    macroSpeedOption.pack_forget()
    loopOption.pack_forget()
    
    resetMacrosButton.pack_forget()
    selectButton.pack_forget()
    
    topFrame.pack_forget()
    topFrame2.pack_forget()
    topFrame3.pack_forget()
    
    goBackMenu()

# Resets macro by pushing an empty list to Json
def resetMacros():
    global sentenceList
    
    sentenceList = []
    with open("sentences.json", "w") as f:
        json.dump(sentenceList, f, indent=4)
    messagebox.showinfo("MACROS Reset","All your macros were sucessfully deleted")
    
    delayOption.pack_forget()
    macroSpeedOption.pack_forget()
    loopOption.pack_forget()
    selectButton.pack_forget()
    topFrame.pack_forget()
    topFrame2.pack_forget()
    topFrame3.pack_forget()
    resetMacrosButton.pack_forget()
    
    goBackMenu()

def entryFocusIn(event):
    widget = event.widget

    if widget is delayOption and widget.get() == "Default is: 5 seconds.":
        widget.delete(0, 'end')
        widget.config(fg="Black")

    if widget is macroSpeedOption and widget.get() == "Default is: 0.1 second.":
        widget.delete(0, 'end')
        widget.config(fg="Black")

    if widget is loopOption and widget.get() == "Default is: 1 loop.":
        widget.delete(0, 'end')
        widget.config(fg="Black")

def settingsWindow():
    global delayWindow, delayOption,macroSpeed, macroSpeedOption, loop, loopOption, resetMacrosButton, sentenceList
    
    clearInput()
    root.title("Settings")
    
    # Forget everything first
    mainLabel.pack_forget()
    userOption.pack_forget()
    selectButton.pack_forget()
    
    #  clear previous UI first in case
    for widget in topFrame.winfo_children():
        widget.destroy()
    for widget in topFrame2.winfo_children():
        widget.destroy()
    for widget in topFrame3.winfo_children():
        widget.destroy()
        
    # Show the frames
    topFrame.pack(pady=3)
    topFrame2.pack(pady=3)
    topFrame3.pack(pady=3)

    
    # ======== 1st Line DELAY BEFORE MACRO =========== #
    delayWindow = tk.Label(topFrame)
    delayWindow.config(text="Delay of Macro: ")
    delayWindow.pack(side="left", padx=5)
    delayOption = tk.Entry(topFrame, fg="Gray")
    delayOption.pack(side="left", padx=5)
    delayOption.insert(0, "Default is: 5 seconds.")
    delayOption.bind("<FocusIn>", entryFocusIn)
    # ================================================ #

    # =========== 2nd Line MACRO SPEED =============== #
    macroSpeed = tk.Label(topFrame2)
    macroSpeed.config(text="Speed of Macro: ")
    macroSpeed.pack(side="left", padx=5)
    macroSpeedOption = tk.Entry(topFrame2, fg="Gray")
    macroSpeedOption.pack(side="left", padx=5)
    macroSpeedOption.insert(0, "Default is: 0.1 second.")
    macroSpeedOption.bind("<FocusIn>", entryFocusIn)
    # ================================================ #

    # =============== 3rd Line LOOPS ================== #
    loop = tk.Label(topFrame3)
    loop.config(text="Loops: ")
    loop.pack(side="left", padx=5)
    loopOption = tk.Entry(topFrame3, fg="Gray")
    loopOption.pack(side="left", padx=5)
    loopOption.insert(0, "Default is: 1 loop.")
    loopOption.bind("<FocusIn>", entryFocusIn)
    # ================================================ #
    
    # ================ SAVING BUTTON ================== #
    selectButton.config(text="Save Settings!", command=saveSettings)
    selectButton.pack(pady=5)
    # ================================================= #

    # ================ RESET MACROS BUTTON ================== #
    resetMacrosButton = tk.Button(root)
    resetMacrosButton.config(text="Reset all Macros!", command=resetMacros)
    resetMacrosButton.pack(pady=5)
    # ================================================= #


# Options of app with their subsequent code
def optionSelect(event=None):
    global userOption, mainLabel, selectButton, sentenceList, topFrame
    try:
        option = int(userOption.get())
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid number.")
        return

    # Gets Sentence from Input then uses function SaveMacro()
    if option == 1:
        clearInput()
        mainLabel.config(text="Write the sentence you wish to add below:\n\nEmpty input will count as aborted")
        selectButton.config(text="Add Macro", command=saveMacro)

    # Shows all Sentences from Array on a Quick Window
    elif option == 2:
        clearInput()
        if not sentenceList:
            messagebox.showinfo("Macros", "No macros saved yet.")
        else:
            infoText = "\n".join(f"[{i}] --> {word}" for i, word in enumerate(sentenceList))
            messagebox.showinfo("Macro List", infoText)

    # If no macros, quick display alerting User, if there's Sentences editMacro()
    elif option == 3:
        clearInput()
        if not sentenceList:
            messagebox.showinfo("Macros", "No macros to edit.")
        else:
            editMacro()

    # Lets User choose which macro to replicate
    elif option == 4:
        clearInput()
        if not sentenceList:
            messagebox.showinfo("Macros", "No macros saved yet.")
            return

        infoText = "\n".join(f"[{i}] --> {word}" for i, word in enumerate(sentenceList))
        macroEdit = simpledialog.askinteger("Macro List", f"Choose the macro to execute:\n{infoText}")

        # Simple error handling
        if macroEdit is None or not (0 <= macroEdit < len(sentenceList)):
            messagebox.showinfo("Cancelled", "Invalid selection.")
            return

        macroWord = sentenceList[macroEdit]

        # Quick warning, alerting user to, after clicking ok, swithc to wanted window.
        messagebox.showinfo(
            "Macro Starting...",
            f'-- {macroWord} -- will start typing in {settingList["delay_speed"]} seconds after closing this window.\nPrepare the target window!'
        )
        time.sleep(settingList["delay_speed"])


        # What types for you
        kb = Controller()
        loops = int(settingList["loops"])  # convert to int para rodar no FOR
        for _ in range(loops):
            for letter in macroWord:
                kb.tap(letter)
                time.sleep(settingList["macro_speed"])
            kb.tap(Key.enter)

        

        messagebox.showinfo("Success", "The macro was executed successfully.")
        exit()

    # Settings
    elif option == 8:
        settingsWindow()
    # Exits app
    elif option == 9:
        sys.exit()

# App's Main Menu and UI
def mainMenu():
    global root, userOption, mainLabel, selectButton, sentenceList, topFrame, topFrame2, topFrame3, settingList
    
    settingList = loadSettings()
    
    try:
        with open("sentences.json", "r") as f:
            content = f.read()
            sentenceList = json.loads(content)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sentenceList = []
    
    root = tk.Tk()
    root.title("Macro Tool")
    root.geometry("250x250")

    # Create a frame to hold label and entry on same line
    topFrame = tk.Frame(root)
    topFrame2 = tk.Frame(root)
    topFrame3 = tk.Frame(root)

    mainLabel = tk.Label(root, text=(
        "Welcome to the macro tool!\n"
        "Choose an option:\n\n"
        "[1] Record a macro\n"
        "[2] See your macros\n"
        "[3] Edit a macro\n"
        "[4] Execute a macro\n"
        "[8] Settings\n"
        "[9] Exit\n"
    ))
    mainLabel.pack(pady=6, padx=6)

    userOption = tk.Entry(root)
    userOption.pack(pady=6, padx=6)

    selectButton = tk.Button(root, text="Choose", command=optionSelect)
    selectButton.pack(pady=6, padx=6)

    userOption.bind("<Return>", lambda event: selectButton.invoke())
    root.mainloop()

# Called to go back to Main Menu and prevent various windows to be opened
def goBackMenu(): 
    clearInput()

    # Calls back main Menu
    mainLabel.pack(pady=6, padx=6)
    userOption.pack(pady=6, padx=6)
    selectButton.pack(pady=6, padx=6)
    
    # Re assigns the proper text on the main Label.
    mainLabel.config(text=(
        "Welcome to the macro tool!\n"
        "Choose an option:\n\n"
        "[1] Record a macro\n"
        "[2] See your macros\n"
        "[3] Edit a macro\n"
        "[4] Execute a macro\n"
        "[8] Settings\n"
        "[9] Exit\n"
    ))
    
    # Re assigns the proper command on the button.
    selectButton.config(text="Choose", command=optionSelect)

# Start the app
mainMenu()

