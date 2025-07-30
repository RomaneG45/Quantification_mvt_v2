""""
This file contains the calculation of different metrics.
:import interface: program that contains the interface for the Actinalyseur application, allowing users to select a folder and initiate calculations.
:import agcounts_filter : program that filter program that pre-processes the raw data and returns it as counted data (acceleration into Activity Counts).
:import segment_file: program that segments the data depending on the therapy modality and hours of activity.
:import metrics_calculation : program that calculates the movement metrics from activity counts.
:import save_metrics_in_excel : program that saves the calculated metrics in an excel file.

:return excel files that contains mean value or value for 8 metrics.
"""

""" ******************************************************************* Import ********************************************************************************************"""
import os
from datetime import datetime
import openpyxl
from tkinter import messagebox
import time
import threading

#from segment_file import
from interface import create_window
from agcounts_filter import convert_AC
from segment_file import segment_time
from metrics_calculation import metrics
from save_metrics_in_excel import select_output_file, write_in_file
from interface import create_progress_interface, update_progress


""" **************************************************************** Browse files **************************************************************************"""
#/////////////////////////AJOUTER UNE BOUCLE POUR PARCOURIR TOUS LES FICHIERS D'UN DOSSIER = AVOIR LES DONNEES DOM NON DOM DE PLUSIEURS ENFANTS//////////////////////////////
"""Pour lister les fichiers contenus dans un dossier :
files_data= os.list("Chemin du dossier contenant les fichiers")
"""

algo_start_time= datetime.now()

output_dir = "Activity_counts_files"

# Create an activity count folder to register the ones created in agcounts_filter.py
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

""" ******************************************************** Selecting input folder **************************************************************************"""

modalities_list = ["Vie_quotidienne", "Stage"]
input_folder = create_window()

# Dict that register the dom and non dom AC for the different time lapse
AC_for_comp = {"Vie_quotidienne" : {"comp_daily_life" : {}},
               "Stage" : {"comp_5h" : {},
                        "comp_1h30" : {}}}

""" ******************************************************** Progress interface **************************************************************************"""

# Start progress interface in a thread
idx_interface = 0
progress_data = {}
interface_thread = threading.Thread(target=create_progress_interface, args = (progress_data,))
interface_thread.daemon = True  # Close the interface with the main script
interface_thread.start()

# Wait for the progress interface to be created
while "bar" not in progress_data or "interface" not in progress_data:
    time.sleep(3)

""" ******************************************************** Getting info from input folder **************************************************************************"""

for modality in modalities_list:
    # Select the Info file in the input folder
    if  modality + "_Info.xlsx" not in os.listdir(input_folder):
        # Notify the user that there is no info file in the inupt folder
        messagebox.showinfo("Fin", f"Aucun fichier {modality + '_Info.xlsx'} dans le dossier sélectionné")
    input_info_file = input_folder + "/" + modality + "_Info.xlsx"

    # Load excel file containing the information
    info_wb = openpyxl.load_workbook(input_info_file)
    # Select the sheet 
    info_sheet = info_wb.active

    # Define the important information (selecting info from info_input_file)
    child_id = str(info_sheet["A2"].value)
    therapy = str(info_sheet["B2"].value)
    non_dom_UL = str(info_sheet["D2"].value)

    # Notify the user if no child ID is provided
    if child_id == "None" :
        messagebox.showinfo("Information manquante", f"L'identifiant de l'enfant n'est pas renseigné dans le fichier {modality}_Info.xlsx.")

    # Define dominant UL
    ul_list = ["Droit", "Gauche"]
    ul_list.remove(non_dom_UL)
    dom_UL = ul_list[0]

    # Define date, start time and end time of the record to analyse
    comp_daily_life, comp_1h30, comp_5h = segment_time(modality, therapy, info_sheet) 
    time_comp = {"Vie_quotidienne" : {"comp_daily_life" : comp_daily_life}, 
                 "Stage":{"comp_1h30" : comp_1h30, "comp_5h" : comp_5h}}
    """print(f"Vie quot : {comp_daily_life}")
    print(f"Comparaison 1h30 : {comp_1h30}")
    print(f"Comparaison 5h : {comp_5h}")"""
    
    # time_comp contains the hour to cut, AC_for_comp contains the AC
    
    """******************************************************** Create output files ***************************************************************"""
    
    if modality == "Stage":
        # Create the output file for the 5h comparison
        output_comp_5h_file_path = input_folder + "/" + "Résultats_comp_5h.xlsx"
        output_comp_5h_wb = select_output_file(output_comp_5h_file_path, child_id, therapy)

        # Create the output file for the 1h30 comparison
        output_comp_1h30_file_path = input_folder + "/" + "Résultats_comp_1h30.xlsx"
        output_comp_1h30_wb = select_output_file(output_comp_1h30_file_path, child_id, therapy)

    elif modality == "Vie_quotidienne":
        # Create the output file for the daily life comparison
        output_daily_file_path = input_folder + "/" + "Résultats_comp_daily_life.xlsx"
        output_daily_wb = select_output_file(output_daily_file_path, child_id, therapy)


    """****************************************************** Getting AC ********************************************************************************************"""

    if  modality + "_" + dom_UL + ".csv" not in os.listdir(input_folder):
        # Notify the user that there is no dom file in the inupt folder
        messagebox.showinfo("Fin", f"Aucun fichier {modality + '_' + dom_UL + '.csv'} dans le dossier sélectionné")
    if  modality + "_" + non_dom_UL + ".csv" not in os.listdir(input_folder):
        # Notify the user that there is no non_dom file in the inupt folder
        messagebox.showinfo("Fin", f"Aucun fichier {modality + '_' + non_dom_UL + '.csv'} dans le dossier sélectionné")

    file_dom = input_folder + "/" + modality + "_" + dom_UL + ".csv"
    file_non_dom = input_folder + "/" + modality + "_" + non_dom_UL + ".csv"

    #update_progress(idx_interface + 10,progress_data["bar"], progress_data["interface"])
    
    # ////////////////////////////////////////////////////////////////////////////////////////// TROP LONG : PEUT ETRE DECOUPER LES FICHIERS AVANT
    #/ /////////////////////////////////////////////// IDEE : AU LIEU DE GARDER LES LIGNE QUE L'ON VEUT? ON SUPPRIME AVEC PANDAS CELLES QUE L'ON NE VEUT PAS, COMME CA ON GARDE UN FICHEIR DONNABLE A AGCOUNTS ET C'EST UN FICHIER PLUS PETIT
    # /////////////////////////////////////////////////////// -> VERIFIER SI C'EST POSSIBLE EN CONSIDERANT LES AUTRES FICHIERS (SAVE METRIC IN EXCEL ...)
    
    #Progress interface
    if modality == "Stage":
        progress_new_step = True
    else: 
        progress_new_step = False
    progress_data["interface"].after(0, update_progress, 0 , progress_data["bar"], progress_data["interface"], f"Lecture des données des capteurs de '{modality}' ...", progress_data["message_label"],progress_data["progress_title"])

    print("Converting raw data into Activity Counts")
    dom_counts, non_dom_counts = convert_AC(file_dom, file_non_dom, progress_data) 

    """***************************************************** Selecting the AC from the time wanted intervals **************************************************************************"""

    # Loop on the number of epoches in the smallest UL file (dom_AC and non_dom_AC will have the same number of rows)
    for data_idx in range(0, min(len(dom_counts), len(non_dom_counts))) : 
        
        # Progress interface
        if data_idx == 1:
            progress_new_step = True
        else:
            progress_new_step = False
        progress_data["interface"].after(0, update_progress, 0.5 + (data_idx / (min(len(dom_counts), len(non_dom_counts))))/2 , progress_data["bar"], progress_data["interface"], f"Calcul des métriques pour '{modality}' ...",  progress_data["message_label"], progress_data["progress_title"])
        

        # Get the date and hour of the activity count
        count_date = dom_counts["Timestamp"][data_idx].date()
        #/////////////////////////////////////////////////////////////////: Si les counts_date ne se suivent pas -> indiquer pas de données pour se jour (au cas ou il y ai des jours manquant)

        # Loop on the comparison modalities
        for time_lapse_name in time_comp[modality].keys():
            time_lapse = time_comp[modality][time_lapse_name]
            
            # Check that the day from the sensor is register in the info excel
            if count_date in time_lapse.keys():

                # Check if the time lapse for the day already exists
                if count_date not in AC_for_comp[modality][time_lapse_name].keys():
                        AC_for_comp[modality][time_lapse_name][count_date] =  {"dom_AC" : [],"non_dom_AC" : []} # //////////////////////// placé ici, il n'y a que la derniere comparaison qui est enregistrée

                # Get start_time and end_time of the recording from the day
                lst_start_time = time_lapse[count_date]["start_time"]
                lst_end_time = time_lapse[count_date]["end_time"] 

                if lst_start_time and lst_end_time != []:

                    # Loop on the timelapses of the excel info file
                    for idx_hour in range(0,len(lst_start_time)):

                        # Add the new AC 
                        if dom_counts["Timestamp"][data_idx].strftime("%H:%M:%S") >= lst_start_time[idx_hour] and dom_counts["Timestamp"][data_idx].strftime("%H:%M:%S") < lst_end_time[idx_hour]:
                            AC_for_comp[modality][time_lapse_name][count_date]["dom_AC"].append(dom_counts.loc[data_idx, "AC"])
                            AC_for_comp[modality][time_lapse_name][count_date]["non_dom_AC"].append(non_dom_counts.loc[data_idx, "AC"])

    """************************************************* Explore the AC lists for the different time laps to calculate the metrics ********************************************************"""
    dom_AC = []
    dom_non_AC = []
    # Explore the AC lists for the different time laps to calculate the metrics
    for comparison in AC_for_comp[modality]:
        idx_day = 1

        for day in AC_for_comp[modality][comparison]:
            dom_AC = AC_for_comp[modality][comparison][day]["dom_AC"]
            non_dom_AC = AC_for_comp[modality][comparison][day]["non_dom_AC"]

            if dom_AC != [] and non_dom_AC != []:

                #****************************** Metrics calculation for the selected time lapse ******************************
                dict_metrics = metrics(dom_AC, non_dom_AC)
                
                print(f"Dominant Active Duration for the day {count_date}: {dict_metrics['dom_AD']}")
                print(f"Non Dominant Active Duration for the day {count_date} : {dict_metrics['non_dom_AD']}\n")
                print(f"Metrics saved for the day {count_date}\n")

                
                output_file_path = input_folder + "/" + "Résultats_" + comparison + ".xlsx" 
                output_wb = openpyxl.load_workbook(output_file_path)

                #******************************* Save metrics in an excel file ***********************************************
                time_metrics = [dict_metrics['dom_AD'], dict_metrics['non_dom_AD'],dict_metrics['bimanual_AD'], dict_metrics['use_ratio_time']]
                intensity_metrics = [dict_metrics['dom_mean_AC'], dict_metrics['non_dom_mean_AC'], dict_metrics['mean_bilateral_magnitude'], dict_metrics['mean_magnitude_ratio'], dict_metrics['maui'], dict_metrics['baui']]
                record_time = len(dom_AC) / 60 # time in min
                write_in_file(output_wb, output_file_path, record_time, idx_day, day, time_metrics, intensity_metrics)
            
            #Update loop values
            idx_day += 1 

    # Notify the user if the recorded hours and the hours in the info file do not match 
    if dom_AC == []:
        messagebox.showinfo("Fin",f"Il y a une erreur : les dates ou les heures du fichier Info ne correspondent pas aux données des capteurs pour la modalité : {modality}" )
        print(f"Il y a une erreur : les dates ou les heures du fichier Info ne correspondent pas aux données des capteurs pour la modalité : {modality}")

    algo_end_time= datetime.now()
    print(f"L'algo dure : {algo_end_time-algo_start_time}")

# Notify the user that the calculations are finished
messagebox.showinfo("Fin", f"Les résultats sont disponnibles dans le dossier : {input_folder}")
