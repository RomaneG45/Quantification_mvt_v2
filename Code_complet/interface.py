import tkinter as tk
from tkinter import filedialog

def select_input_file():
    # Create a tk window (without display)
    racine = tk.Tk()
    # Hide main window
    racine.withdraw() 

    # Open the folder selection dialog box
    folder_path = filedialog.askdirectory(title = "Sélectionner un dossier")

    return folder_path
