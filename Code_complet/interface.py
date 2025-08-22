"""This file contains the interface of the Actinalyseur application, allowing users to select a folder and initiate calculations.
Called in main.py and agcounts_filter.py"""

import customtkinter as ctk
from tkinter import filedialog, PhotoImage
from PIL import Image
from customtkinter import CTkImage
import os
from test_error import test_error

# Global variable to store the selected folder path
folder = " "

# Folder selection function
def choose_folder(window):
    """Function to open a dialog for folder selection and update the label with the selected folder path.
    :param window: The main application window.
    :return: The selected folder path."""
    try:
        global folder
        folder = filedialog.askdirectory()
        if folder:
            folder_label.configure(text = folder,  wraplength = 230) 
            folder_label.pack(padx = (10,0))
        else:
            folder_label.configure(text = "Aucun dossier sélectionné")

        return folder
    except Exception as e:
        print("Erreur dans le thread interface: ", e)

# Function to launch calculations
def start_calculation(window, selected_threshold):
    """Function to handle the action when the user clicks the 'Metrics calculation' button.
    :param window: The main application window."""
    try:
        modalities_list = ["Vie_quotidienne", "Stage"]
        
        # Close the first window if a there is no error or warning in the input items
        if test_error(folder, modalities_list, selected_threshold.get()):
            window.destroy()

    except Exception as e:
        print("Erreur dans le thread interface: ", e)


# Function called when selecting a threshold
def on_option_change(selected_threshold):
    print(f"Option sélectionnée : {selected_threshold.get()}")

# --- Layout ---
def create_window():
    """Function to create the main application window with a folder selection interface.
    :return: The selected folder path."""
    try:
        # Basic configuration
        ctk.set_appearance_mode("light")     
        ctk.set_default_color_theme("green") 

        # Main window
        window = ctk.CTk()
        # Actinalyseur icon
        script_dir = os.path.dirname(os.path.abspath(__file__)) 
        image_path = os.path.join(script_dir, "Images", "Actinalyseur.png")
        icon = PhotoImage(file = image_path)
        window.iconphoto(True, icon)
        window.title("Actinalyseur")
        window.geometry("650x380")

        # Load image
        folder_image_path = os.path.join(script_dir, "Images", "folder_image.png")
        file_img = CTkImage(Image.open(folder_image_path), size = (90, 90))  # ajuste la taille selon ton image

        # ------------------------------------------------ Frames creation ---------------------------------------
        # Horizontal frame for image + button + label
        selection_frame = ctk.CTkFrame(window, fg_color = "transparent" )
        selection_frame.pack()

        frame_text = ctk.CTkFrame(selection_frame, fg_color = "transparent")
        frame_text.pack(side = "right", pady = (20,0))

        frame_please = ctk.CTkFrame(frame_text, fg_color = "transparent" )
        frame_please.pack(fill = "x", padx = (30,0),expand = True)

        frame_choose_button = ctk.CTkFrame(frame_text, fg_color = "transparent" )
        frame_choose_button.pack(fill = "x", expand = True, padx = (30,0), pady = (20,0))

        frame_separating_line = ctk.CTkFrame(window, fg_color = "transparent" )
        frame_separating_line.pack(fill = "x", expand = True)

        frame_threshold_selection =  ctk.CTkFrame(window, fg_color = "transparent" )
        frame_threshold_selection.pack(fill = "x", expand = True, pady = (0,10))

        frame_instruction_threshold = ctk.CTkFrame(frame_threshold_selection, fg_color = "transparent")
        frame_instruction_threshold.pack(pady = (15,15))

        frame_radio_button = ctk.CTkFrame(frame_threshold_selection, fg_color = "transparent")
        frame_radio_button.pack()

        frame_calculation_button = ctk.CTkFrame(window, fg_color = "transparent" )
        frame_calculation_button.pack(fill = "x", expand = True)#, pady = (20,0))


        # ------------------------------------------------ Filling frames with items ---------------------------------------
        #IMAGE
        # Image on the left handside
        image_label = ctk.CTkLabel(selection_frame, image = file_img, text = "")
        image_label.pack(side = "left", padx = (70,35), pady = (50, 30))
        

        # THRESHOLD SELECTION
        # Variable to store the threshold selection
        selected_option = ctk.StringVar(value = " ")
        # Label instruction (threshold method)
        threshold_instruction = ctk.CTkLabel(frame_instruction_threshold, text = "Choisir la méthode de seuillage : ", font = ("Arial", 14, "bold"))
        threshold_instruction.pack(anchor = "n")

        # Threshold selection button
        radio_button_1 = ctk.CTkRadioButton(frame_radio_button, text = "AC > 0", variable = selected_option, value = "AC > 0", command = lambda:on_option_change(selected_option))
        radio_button_2 = ctk.CTkRadioButton(frame_radio_button, text = "Random Forest", variable = selected_option, value = "Random Forest", command = lambda:on_option_change(selected_option))
        radio_button_3 = ctk.CTkRadioButton(frame_radio_button, text ="Coley", variable = selected_option, value = "Coley", command = lambda:on_option_change(selected_option))
        # Horizontal alignement with grid
        radio_button_1.grid(row = 0, column = 0, padx = 80, pady = 10)
        radio_button_2.grid(row = 0, column = 1, padx = 50, pady = 10)
        radio_button_3.grid(row = 0, column = 2, padx = 50, pady = 10)


        # SEPARATING LINE
        canvas = ctk.CTkCanvas(frame_separating_line, height = 20, width = 1000, bg = "gray92", highlightthickness=0)
        canvas.pack(expand = True)
        # Horizontal line
        canvas.create_line(100, 10, 700, 10, fill = "black", width = 2)


        # FOLDER SELECTION
        # Label instruction (folder selection)
        instruction_label = ctk.CTkLabel(frame_please, text = "Choisir le dossier de l'enfant : ", font = ("Arial", 14,"bold"), anchor = "w", justify = "left")
        instruction_label.pack(side = "left", padx = 10)

        # Selection folder button
        choose_button = ctk.CTkButton(frame_choose_button, text = "Choisir un dossier", command = lambda:choose_folder(window), fg_color = "transparent", border_width = 2, border_color = "#2ecc71", text_color = "#2ecc71", hover_color = "#DFDFDF" , width = 120, height = 40)
        choose_button.pack(side = "left", padx = 5)

        # Label to display the selected folder
        global folder_label
        folder_label= ctk.CTkLabel(frame_choose_button, text = "Aucun dossier choisi", text_color = "gray", anchor = "w", width = 300)
        folder_label.pack(side = "left", padx = (10,0))#pady=(0, 20))


        # FINAL BUTTON
        # Button to launch calculations
        calculation_button = ctk.CTkButton(frame_calculation_button, text = "Calculer les métriques", command = lambda:start_calculation(window, selected_option), fg_color = "#2ecc71", hover_color = "#27ae60")
        calculation_button.pack(side = "right", padx = (0,20), pady = (20,20))

        # Run the main loop
        window.mainloop()

        return folder, selected_option.get()
    
    except Exception as e:
        print("Erreur dans le thread interface: ", e)


def update_progress(idx_interface,progress_bar, progress_interface, message, message_label, progress_title):
    """Function to update the progress bar.
    :param idx_interface: Int of the current index of the progress bar.
    :param progress_bar:  ctk.CTkProgressBar The progress bar widget.
    :param progress_interface: ctk.CTK The main interface window.
    :param message: Str message to display in the interface windox.
    :param message_label: ctk.CTkLabel The label widget to display the message."""
    # Update the progress bar value
    #print(f" type de idx_interface : {type(idx_interface)}")
    try:
        if idx_interface > 0.0:
            progress_bar.set(idx_interface) 
            progress_interface.update_idletasks()
            # Update the message in the interface
            message_label.configure(text = message)

        else:
            progress_bar.set(idx_interface) 
            progress_interface.update_idletasks()
            # Update the title interface (first or second)
            #if message_label.cget("text") != "Lancement ...":
            progress_title.configure(text = f"Progression")
            # Update the message in the interface
            message_label.configure(text = message)
            


    except Exception as e:
        print("Erreur dans le thread interface: ", e)



def create_progress_interface(progress_dict):
    """Function to create a CustomTkinter progress bar interface.
    :param progress_dict: A dictionary to store references to the progress bar and interface."""
    try : 
        # Initialize the CustomTkinter app
        progress_interface = ctk.CTk()
        # Actinalyseur icon
        script_dir = os.path.dirname(os.path.abspath(__file__)) 
        icon_path = os.path.join(script_dir, "Images", "Actinalyseur.png")
        icon = PhotoImage(file=icon_path)
        progress_interface.iconphoto(True, icon)
        progress_interface.geometry("650x380")
        progress_interface.title("Actinalyseur")

        # Frame containing the window items
        main_frame = ctk.CTkFrame(progress_interface,  fg_color = "transparent")
        main_frame.pack(expand = True)

        # Title label
        title_label = ctk.CTkLabel(main_frame, text = "Progression", font = ("Arial", 20, "bold"))
        title_label.pack(pady = (20, 10))

        # Create a progress bar
        progress_bar = ctk.CTkProgressBar(main_frame, orientation = "horizontal", mode = "determinate", width = 300, height = 20)
        progress_bar.pack(pady = 20)

        # Create the message in the interface
        message_frame = ctk.CTkFrame(main_frame, fg_color = "transparent" )
        message_frame.pack()
        message_label = ctk.CTkLabel(message_frame, text = "Lancement ...", font = ("Arial", 12))
        message_label.pack()

        # Initialize the progress bar
        progress_bar.set(0)  
        # Stocker les références dans un dictionnaire partagé
        progress_dict["bar"] = progress_bar
        progress_dict["interface"] = progress_interface
        progress_dict["message_label"] = message_label
        progress_dict["progress_title"] = title_label


        progress_interface.mainloop()
    except Exception as e:
        print("Erreur dans le thread interface: ", e)



