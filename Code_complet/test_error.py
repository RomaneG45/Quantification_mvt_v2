import os
from datetime import datetime, time
import openpyxl
from tkinter import messagebox

"""This file handles any errors related to the input file. A message is displayed in the interface if there is something to change in the input folder.
errors tested:
- If the input folder contains the right files
- If the values in the info file are of the right type

Called interface.py"""

def test_error(input_folder, modalities_list, threshold_selected):
    """
    This function ckecks if the input folder contains the right files and if the values in the info file are of the right type.
    :param input_folder (str) : folder containing the input files
    :param modalities_list (list) : modalities to check
    :param threshold_selected (str) : name of the selected movement detection method
    :return True if any errors occur
    :return False if the script meets an error or a warning"""
    
    """ ******************************************************** Checks if a input folder and a threshold method are selected **************************************************************************"""
    if input_folder == " " or input_folder == "":
        messagebox.showwarning("Fin","Veuillez choisir un dossier")
        return False

    if threshold_selected == " " :
        messagebox.showwarning("Fin","Veuillez choisir une méthode de seuillage")
        return False

    """ ******************************************************** Checks if the input folder contains the right files **************************************************************************"""
    for modality in modalities_list:
        # Initialize the index of record file for the modality (ex: Stage 1)
        idx_file_modality = 1
        # Browse files in the input folder
        for file in os.listdir(input_folder):
            # Check if the file correspond to the modality
            if file.startswith(modality+ "_" + str(idx_file_modality)):
                # Display error if the sensor files are not in the input folder
                if  modality + "_" + str(idx_file_modality) + "_Droit" + ".csv" not in os.listdir(input_folder):
                    # Notify the user that there is no dom file in the inupt folder
                    messagebox.showerror("Fin", f"Aucun fichier {modality + '_' + str(idx_file_modality) + '_Droit' + '.csv'} dans le dossier sélectionné. Ajoutez le fichier avant de relancer le programme.")
                    return False
                if  modality + "_" + str(idx_file_modality) + "_Gauche" + ".csv" not in os.listdir(input_folder):
                    # Notify the user that there is no non_dom file in the inupt folder
                    messagebox.showerror("Fin", f"Aucun fichier {modality + '_' + str(idx_file_modality) + '_Gauche' + '.csv'} dans le dossier sélectionné. Ajoutez le fichier avant de relancer le programme.")
                    return False
                
                idx_file_modality += 1

            # Check if the info file for the modality exists
            if modality + "_Info.xlsx" not in os.listdir(input_folder): #///////////////////////////////////////////////////////// Pour mettre un nom d'enfant dans le nom du fichier
                # Notify the user that there is no info file in the inupt folder
                messagebox.showerror("Fin", f"Aucun fichier {modality + '_Info.xlsx'} dans le dossier sélectionné. Ajoutez le fichier avant de relancer le programme.")
                return False
        

            """ ******************************************************** Checks if the input files contains the right type **************************************************************************"""
            #///////////////////////////////////////////////////////// Pour mettre un nom d'enfant dans le nom du fichier ///////////////////////////////////////////////////////////
            # Select the Info file in the input folder
            input_info_file = input_folder + "/" + modality + "_Info.xlsx"
            # Load excel file containing the information
            info_wb = openpyxl.load_workbook(input_info_file)
            # Select the sheet 
            info_sheet = info_wb.active
            
            if file.startswith(modality + "_Info.xlsx"):
                # Check if the type of value in the info file are the right ones
                for cell in info_sheet["E"]:
                    if cell.row > 1 and not isinstance(cell.value, datetime) and cell.value is not None:
                        messagebox.showerror("Fin", f"La valeur de la cellule JOUR DE PORT {cell.row} dans le fichier {modality}_Info.xlsx n'est pas de type date. Modifiez la valeur avant de relancer le programme.")
                        return False
                for cell in info_sheet["I"]:
                    if cell.row > 1 and not isinstance(cell.value,time) and cell.value is not None:
                        messagebox.showerror("Fin", f"La valeur de la cellule HEURE DE DEBUT D'ACTIVITE {cell.row} dans le fichier {modality}_Info.xlsx n'est pas de type heure. Modifiez les valeurs avant de relancer le programme.")
                        return False
                for cell in info_sheet["J"]:
                    if cell.row > 1 and not isinstance(cell.value,time) and cell.value is not None:
                        messagebox.showerror("Fin", f"La valeur de la cellule HEURE DE FIN D'ACTIVITE {cell.row} dans le fichier {modality}_Info.xlsx n'est pas de type heure.  Modifiez les valeurs avant de relancer le programme.")
                        return False

            """ ******************************************************** Checks if the input files are closed (necessary to be read) **************************************************************************"""
            if file.startswith(modality+ "_" + str(idx_file_modality)) or file.startswith("Résultat"):
                full_path = os.path.join(input_folder, file)
                # Check if the selected item is a file
                if os.path.isfile(full_path):
                    try:
                        with open(full_path, 'a'):
                            pass
                    except PermissionError:
                        messagebox.showerror("Fin", f"Le fichier {file} est ouvert. Fermez le avant de relancer le programme.")
                        return False
                else:
                    continue
    return True