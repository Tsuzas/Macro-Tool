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

# Options of app with their subsequent code
def optionSelect(event=None):
    global userOption, mainLabel, selectButton, sentenceList
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
            f'-- {macroWord} -- will start typing in 5 seconds.\nPrepare the target window!'
        )
        time.sleep(5)

        # What types for you
        kb = Controller()
        for letter in macroWord:
            kb.tap(letter)
            time.sleep(0.1)
        kb.tap(Key.enter)

        messagebox.showinfo("Success", "The macro was executed successfully.")
        exit()

    # Exits app
    elif option == 9:
        sys.exit()

# App's Main Menu and UI
def mainMenu():
    global root, userOption, mainLabel, selectButton, sentenceList

    try:
        with open("sentences.json", "r") as f:
            content = f.read()
            sentenceList = json.loads(content)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sentenceList = []

    root = tk.Tk()
    root.title("Macro Tool")
    root.geometry("250x220")

    mainLabel = tk.Label(root, text=(
        "Welcome to the macro tool!\n"
        "Choose an option:\n\n"
        "[1] Record a macro\n"
        "[2] See your macros\n"
        "[3] Edit a macro\n"
        "[4] Execute a macro\n"
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
    mainLabel.config(text=(
        "Welcome to the macro tool!\n"
        "Choose an option:\n\n"
        "[1] Record a macro\n"
        "[2] See your macros\n"
        "[3] Edit a macro\n"
        "[4] Execute a macro\n"
        "[9] Exit\n"
    ))
    selectButton.config(text="Choose", command=optionSelect)

# Start the app
mainMenu()
