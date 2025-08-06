
import os
from datetime import datetime, time
import openpyxl
from tkinter import messagebox



def test_error(input_folder, modalities_list):
    """
    This function ckecks if the input folder contains the right files and if the values in the info file are of the right type.
    :param input_folder: The folder containing the input files
    :param modalities_list: The list of modalities to check"""
    
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
                    messagebox.showinfo("Fin", f"Aucun fichier {modality + '_' + str(idx_file_modality) + '_Droit' + '.csv'} dans le dossier sélectionné. Ajoutez le fichier avant de relancer le programme.")
                    exit()
                if  modality + "_" + str(idx_file_modality) + "_Gauche" + ".csv" not in os.listdir(input_folder):
                    # Notify the user that there is no non_dom file in the inupt folder
                    messagebox.showinfo("Fin", f"Aucun fichier {modality + '_' + str(idx_file_modality) + '_Gauche' + '.csv'} dans le dossier sélectionné. Ajoutez le fichier avant de relancer le programme.")
                    exit()

                # Select the Info file in the input folder
                input_info_file = input_folder + "/" + modality + "_Info.xlsx"
                # Load excel file containing the information
                info_wb = openpyxl.load_workbook(input_info_file)
                # Select the sheet 
                info_sheet = info_wb.active
                
                idx_file_modality += 1

            # Check if the info file for the modality exists
            if modality + "_Info.xlsx" not in os.listdir(input_folder):
                # Notify the user that there is no info file in the inupt folder
                messagebox.showinfo("Fin", f"Aucun fichier {modality + '_Info.xlsx'} dans le dossier sélectionné. Ajoutez le fichier avant de relancer le programme.")
                exit()

            if file.startswith(modality + "_Info.xlsx"):
                # Check if the type of value in the info file are the right ones
                for cell in info_sheet["E"]:
                    if cell.row > 1 and not isinstance(cell.value, datetime) and cell.value is not None:
                        messagebox.showinfo("Fin", f"La valeur de la cellule JOUR DE PORT {cell.row} dans le fichier {modality}_Info.xlsx n'est pas de type date. Modifier la valeur avant de relancer le programme.")
                        exit()
                for cell in info_sheet["I"]:
                    if cell.row > 1 and not isinstance(cell.value,time) and cell.value is not None:
                        messagebox.showinfo("Fin", f"La valeur de la cellule HEURE DE DEBUT D'ACTIVITE {cell.row} dans le fichier {modality}_Info.xlsx n'est pas de type heure. Modifier les valeurs avant de relancer le programme.")
                        exit()
                for cell in info_sheet["J"]:
                    if cell.row > 1 and not isinstance(cell.value,time) and cell.value is not None:
                        messagebox.showinfo("Fin", f"La valeur de la cellule HEURE DE FIN D'ACTIVITE {cell.row} dans le fichier {modality}_Info.xlsx n'est pas de type heure.  Modifier les valeurs avant de relancer le programme.")
                        exit()