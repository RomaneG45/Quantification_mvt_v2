"""This file contains the interface for the Actinalyseur application, allowing users to select a folder and initiate calculations."""

import customtkinter as ctk
from tkinter import filedialog
from PIL import Image
from customtkinter import CTkImage

# Global variable to store the selected folder path
folder = ""

# Folder selection function
def choose_folder(window):
    """Function to open a dialog for folder selection and update the label with the selected folder path.
    :param window: The main application window.
    :return: The selected folder path."""
    try:
        global folder
        folder = filedialog.askdirectory()
        if folder:
            folder_label.configure(text=folder, width=200, height=40, anchor="nw", wraplength=280)
            window.geometry("630x220")
        else:
            folder_label.configure(text="Aucun dossier sélectionné")

        return folder
    except Exception as e:
        print("Erreur dans le thread interface: ", e)

# Function to launch calculations
def start_calculation(window):
    """Function to handle the action when the user clicks the 'Metrics calculation' button.
    :param window: The main application window."""
    try:
        window.destroy()
    except Exception as e:
        print("Erreur dans le thread interface: ", e)


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
        window.title("Actinalyseur")
        window.geometry("500x220")

        # Load image
        file_img = CTkImage(Image.open("C:/Users/roman/Documents/BEaCHILD/Quantification_mvt_v2/Quantification_mvt_v2/Code_complet/folder_image.png"), size=(90, 90))  # ajuste la taille selon ton image

        # Horizontal frame for image + button + label
        selection_frame = ctk.CTkFrame(window, fg_color= "transparent" )
        selection_frame.pack()

        # Image à gauche
        image_label = ctk.CTkLabel(selection_frame, image=file_img, text="")
        image_label.pack(side="left", padx=(50,15), pady=(30, 30))

        frame_text = ctk.CTkFrame(selection_frame, fg_color= "transparent" )
        frame_text.pack(side = "right")

        frame_please = ctk.CTkFrame(frame_text, fg_color= "transparent" )
        frame_please.pack(fill="x", expand=True)

        frame_choose_button = ctk.CTkFrame(frame_text, fg_color= "transparent" )
        frame_choose_button.pack(fill="x", expand=True, pady = (20,0))

        frame_calculation_button = ctk.CTkFrame(window, fg_color= "transparent" )
        frame_calculation_button.pack(fill="x", expand=True)#, pady = (20,0))

        # Label instruction
        instruction_label = ctk.CTkLabel(frame_please, text="Choisir le dossier de l'enfant", font=("Arial", 14, "italic"), anchor="w", justify="left")
        instruction_label.pack(side="left", padx=10)

        # Bouton de sélection
        choose_button = ctk.CTkButton(frame_choose_button, text="Choisir un dossier", command=lambda:choose_folder(window), fg_color = "transparent",border_width=2, border_color = "#2ecc71", text_color = "#2ecc71", hover_color = "#DFDFDF" , width = 120, height = 40)
        choose_button.pack(side="left", padx=5)


        # Label to display the selected folder
        global folder_label
        folder_label= ctk.CTkLabel(frame_choose_button, text="Aucun dossier choisi", text_color="gray", anchor="w", width=300)
        folder_label.pack(side="left", padx=(10,0))#pady=(0, 20))

        # Button to launch calculations
        calculation_button = ctk.CTkButton(frame_calculation_button, text="Calculer les métriques", command= lambda: start_calculation(window), fg_color="#2ecc71", hover_color="#27ae60")
        calculation_button.pack(side = "right", padx = (0,20), pady=(20,20))

        # Run the main loop
        window.mainloop()

        return folder
    
    except Exception as e:
        print("Erreur dans le thread interface: ", e)


def update_progress(idx_interface,progress_bar, progress_interface, message, message_label, progress_title):
    """Function to update the progress bar.
    :param idx_interface: The current index of the progress.
    :param progress_bar: The progress bar widget.
    :param progress_interface: ctk.CTK() The main interface window.
    :param message: Str message to display in the interface windox.
    :param message_label: The label widget to display the message."""
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
            # Update the title interface (first or second modality)
            if message_label.cget("text") != "Lancement ...":
                progress_title.configure(text = "Progression 2/2")
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
        progress_interface.geometry("400x200")
        progress_interface.title("Actinalyseur")

        # Title label
        title_label = ctk.CTkLabel(progress_interface, text="Progression 1/2", font=("Arial", 20, "bold"))
        title_label.pack(pady = (20, 10))

        # Create a progress bar
        progress_bar = ctk.CTkProgressBar(progress_interface, orientation="horizontal", mode="determinate", width=300, height=20)
        progress_bar.pack(pady=20)

        # Create the message in the interface
        message_frame = ctk.CTkFrame(progress_interface, fg_color= "transparent" )
        message_frame.pack()
        message_label = ctk.CTkLabel(message_frame, text = "Lancement ...", font=("Arial", 12))
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



