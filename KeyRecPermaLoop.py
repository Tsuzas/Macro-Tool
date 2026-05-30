import os
import sys
import json
import time
import tkinter as tk
from pynput import keyboard
from pynput.keyboard import Controller, Key
from tkinter import simpledialog, messagebox

# LISTENER VARIABLE FOR CONTINUOUS LOOPS    
stopFlag = False
# LISTENER VARIABLE FLAG
listenerTrigger = False

#CHANGES THE JSON PATH TO THE CURRENT FOLDER
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# JSON PATHS FOR SETTINGS AND SENTENCES
settings_path = os.path.join(BASE_DIR, "settings.json")
sentences_path = os.path.join(BASE_DIR, "sentences.json")

# ================ CLEAR INPUT FUNCTION ================= #
#                   Clears userOption                     #
#           so it doesn't keep the previous option        #
def clearInput():
    global userOption
    userOption.delete(0, tk.END)

# ================ SAVE MACRO FUNCTION ================== #
#          Saves macro by appending to array              #
#                  And pushing to Json                    #
def saveMacro(event=None):
    global sentenceList, userOption
    if (userOption.get() == ""):
        messagebox.showinfo("Aborted", "Field was empty.\nReturning...")
    else:
        macro = userOption.get()
        sentenceList.append(macro)
        with open(sentences_path, "w") as f:
            json.dump(sentenceList, f)
        messagebox.showinfo("Saved", f"Macro saved: {macro}")
        clearInput()

    goBackMenu()

# ================ EDIT MACRO FUNCTION ================== #
#           Shows all macros, edits from input            #
#            then pushes to array and to Json             #
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
            with open(sentences_path, "w") as f:
                json.dump(sentenceList, f)
            messagebox.showinfo("Edited", "Macro edited successfully!")
    else:
        messagebox.showinfo("Error", "Invalid index.")

# === LOAD SETTINGS === #
#     # VIA jSon #     #
def loadSettings():
    try:
        with open(settings_path, "r") as f:
            return json.load(f)
    except:
        # Default values if file doesn't exist
        return {
            "delay_speed": 5,
            "macro_speed": 0.1,
            "loops": 1
        }

# ================ SAVE SETTINGS FUNCTION ================== #
#       Defines time for input, input speed, and loops       #
def saveSettings():
    global settingList, delayOption, macroSpeedOption, loopOption, delayWindow, macroSpeed, loop, delayWindow

    settingList = {}  # clean list


    # =================== DELAY SPEED SETTINGS ========================== #
    delayHolder = delayOption.get()
    if delayHolder == "Default is: 5 seconds." or delayHolder == "":
        delayValue = 5.0
        messagebox.showinfo("Empty Field Detected", "Delay empty → Defaulting to 5 seconds.")
    else:
        delayValue= float(delayHolder)

    settingList["delay_speed"] = delayValue  
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
    
    with open(settings_path, "w") as f:
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

# ================ CLEAR MACRO LIST FUNCTION ================== #
#         Resets macro by pushing an empty list to Json         #
def resetMacros():
    global sentenceList
    
    sentenceList = []
    with open(sentences_path, "w") as f:
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

# ================ PLACEHOLDERS FOR SETTINGS ================== #
#        Whole shenanigans, putting values in field             #
#        Then tunning colour until user clicks on it            #
#        Clearing the input field allowing user to write        #
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

# ================ CREATES SETTING WINDOWS  ================== #
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


# ================ OPTION MENU FOR USER ================== #
#                  Switch case with all                    #
#             The options related code on it               #
def optionSelect(event=None):
    ## LIST OF OPTION  = [1, 2 ,3 ,4 ,5 ,8 ,9]
    
    global userOption, mainLabel, selectButton, sentenceList, topFrame, stopFlag, listenerTrigger


    # ===================== TRY CATCH BLOCK ===================== #
    try:
        option = int(userOption.get())
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid number.")
        return
    # ============ Catches String Floats and Empty ============== #

    match option:
        # ==================== SWITCH CASE ====================== #
        # Gets Sentence from Input then uses function SaveMacro() #

        case 1:
            clearInput()
            mainLabel.config(text="Write the sentence you wish to add below:\n\nEmpty input will count as aborted")
            selectButton.config(text="Add Macro", command=saveMacro)

        # Shows all Sentences from Array on a Quick Window
        case 2:
            clearInput()
            if not sentenceList:
                messagebox.showinfo("Macros", "No macros saved yet.")
            else:
                infoText = "\n".join(f"[{i}] --> {word}" for i, word in enumerate(sentenceList))
                messagebox.showinfo("Macro List", infoText)
        case 3:
            # If no macros, quick display alerting User, if there's Sentences editMacro()
            clearInput()
            if not sentenceList:
                messagebox.showinfo("Macros", "No macros to edit.")
            else:
                editMacro()
        case 4:
            clearInput()
            if not sentenceList:
                messagebox.showinfo("Macros", "No macros saved yet.")
                return
        
            # Lets User choose which macro to replicate
            infoText = "\n".join(f"[{i}] --> {word}" for i, word in enumerate(sentenceList))
            macroEdit = simpledialog.askinteger("Macro List", f"Choose the macro to execute:\n{infoText}")

            # Simple error handling
            if macroEdit is None or not (0 <= macroEdit < len(sentenceList)):
                messagebox.showinfo("Cancelled", "Invalid selection.")
                return

            macroWord = sentenceList[macroEdit]

            #ASKS FOR LISTENER
            permission = allowListener()
            if permission == 1:
                while stopFlag != True:
                    time.sleep(0.1)
                    while listenerTrigger != True:
                        time.sleep(0.1)

                    # What types for you
                    kb = Controller()
                    loops = int(settingList["loops"])  # convert to int para rodar no FOR
                    for _ in range(loops):
                        for letter in macroWord:
                            print(letter)
                            kb.tap(letter)
                            time.sleep(settingList["macro_speed"])
                        kb.tap(Key.enter)
                    listenerTrigger = False
                messagebox.showinfo("Success", "The macro was executed successfully.")
                listener.stop()
                stopFlag = False
            else:
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
        #Delete specific index of Macro
        case 5:
            deleteMacro = simpledialog.askinteger("Delete Macro", "Choose the macro to delete:\n" + "\n".join(f"[{i}] --> {word}" for i, word in enumerate(sentenceList)))

            if deleteMacro is not None and 0 <= deleteMacro < len(sentenceList):
                del sentenceList[deleteMacro]
                with open(sentences_path, "w") as f:
                    json.dump(sentenceList, f)
                messagebox.showinfo("Success", "The macro was deleted successfully.")
            else:
                messagebox.showinfo("Cancelled", "Invalid selection.")
        # Settings
        case 8:
            settingsWindow()
        # Exits app
        case 9:
            sys.exit()
        # Wild card for numbers not in previous switches
        case _:
            messagebox.showerror("Warning", "Noone of the options were selected")
            clearInput()


# ================ MAIN MENU ================== #
#           Creates the first menu              #
def mainMenu():
    global root, userOption, mainLabel, selectButton, sentenceList, topFrame, topFrame2, topFrame3, settingList
    
    settingList = loadSettings()
    
    try:
        with open(sentences_path, "r") as f:
            content = f.read()
            sentenceList = json.loads(content)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sentenceList = []
    
    root = tk.Tk()
    root.title("Macro Tool")
    root.geometry("300x300")
    
    # Sets the icon for the application with try catch preventing error 
    icon_path = os.path.join(BASE_DIR, "media", "icon.png")
    try:
        icon = tk.PhotoImage(file=icon_path)
        root.iconphoto(True, icon)
    except Exception as e:
        print(f"Error loading icon: {e}")
        pass
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
        "[5] Delete a macro\n"
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

# ================ GO BACK MENU ================== #
#              Goes back to Main menu              #
#           Also prevent multiple windows          #
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
        "[5] Delete a macro\n"
        "[8] Settings\n"
        "[9] Exit\n"
    ))
    
    # Re assigns the proper command on the button.
    selectButton.config(text="Choose", command=optionSelect)

# ================ LISTENER ================== #
def on_press(key):
        global listenerTrigger, stopFlag
        if key == keyboard.Key.esc:
            stopFlag = True
            return
        elif key == keyboard.Key.f10:
            listenerTrigger = True
            return
        try:
            k = key.char  # single-char keys
        except:
            k = key.name  # other keys
        if k in ['1', '2', 'left', 'right']:  # keys of interest
            # self.keys.append(k)  # store it in global-like variable
            print('Key pressed: ' + k)
            return False  # stop listener; remove this if want more keys 

# ========== LISTENER PERMISSIONS ============ #
#               Quick user prompt              #
#    To allow listener before macro starts     #
def allowListener():
    global userOption, listener
    response = messagebox.askquestion("Allow Listener?", "Would you like it to listen for a hotkey press (default F10) to initiate or start right now?")

    if response == "yes":
        messagebox.showinfo("Listening!", "The app is currently listening for a keypress, to stop it press (Esc) to stop or close the app.")
        # STARTS LISTENER
        listener = keyboard.Listener(on_press=on_press)
        listener.start()  # start to listen on a separate thread

        return 1
    else: return


# ========== APLICATION YUPI ============ #
mainMenu()


