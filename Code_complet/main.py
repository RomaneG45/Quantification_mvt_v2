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
import openpyxl
from datetime import datetime
from tkinter import messagebox
import pandas as pd

#from segment_file import
from interface import create_window
from agcounts_filter import convert_AC
from segment_file import segment_time
from metrics_calculation import metrics
from save_metrics_in_excel import select_output_file, write_in_file


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
""" ******************************************************** Getting info from input folder **************************************************************************"""

modalities_list = ["Vie_quotidienne", "Stage"]
input_folder = create_window()

# ---Nouveau code (16/07/25)
# Dict that register the dom and non dom AC for the different time lapse
"""AC_for_comp = {"comp_daily_life" : {},
                "comp_5h" : {},
                "comp_1h30" : {}}"""
AC_for_comp = {"Vie_quotidienne" : {"comp_daily_life" : {}},
               "Stage" : {"comp_5h" : {},
                        "comp_1h30" : {}}}


for modality in modalities_list:
    # Select the Info file in the input folder
    if  modality + "_Info.xlsx" not in os.listdir(input_folder):
        # Notify the user that there is no info file in the inupt folder
        messagebox.showinfo("Finish", f"There is no file {modality + '_Info.xlsx'} in the selected folder")
    input_info_file = input_folder + "/" + modality + "_Info.xlsx"

    # Load excel file containing the information
    info_wb = openpyxl.load_workbook(input_info_file)
    # Select the sheet 
    info_sheet = info_wb.active

    # Define the important information (selecting info from info_input_file)
    child_id = str(info_sheet["A2"].value)
    therapy = str(info_sheet["B2"].value)
    non_dom_UL = str(info_sheet["D2"].value)

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
        output_comp_5h_file_path = input_folder + "/" + "Test_output_comp_5h.xlsx"
        output_comp_5h_wb = select_output_file(output_comp_5h_file_path, child_id, therapy)

        # Create the output file for the 1h30 comparison
        output_comp_1h30_file_path = input_folder + "/" + "Test_output_comp_1h30.xlsx"
        output_comp_1h30_wb = select_output_file(output_comp_1h30_file_path, child_id, therapy)

    elif modality == "Vie_quotidienne":
        # Create the output file for the daily life comparison
        output_daily_file_path = input_folder + "/" + "Test_output_comp_daily_life.xlsx"
        output_daily_wb = select_output_file(output_daily_file_path, child_id, therapy)


    #****************************************************** Getting AC ********************************************************************************************

    if  modality + "_" + dom_UL + ".csv" not in os.listdir(input_folder):
        # Notify the user that there is no dom file in the inupt folder
        messagebox.showinfo("Finish", f"There is no file {modality + '_' + dom_UL + '.csv'} in the selected folder")
    if  modality + "_" + non_dom_UL + ".csv" not in os.listdir(input_folder):
        # Notify the user that there is no non_dom file in the inupt folder
        messagebox.showinfo("Finish", f"There is no file {modality + '_' + non_dom_UL + '.csv'} in the selected folder")

    file_dom = input_folder + "/" + modality + "_" + dom_UL + ".csv"
    file_non_dom = input_folder + "/" + modality + "_" + non_dom_UL + ".csv"

    

    # ////////////////////////////////////////////////////////////////////////////////////////// TROP LONG : PEUT ETRE DECOUPER LES FICHIERS AVANT
    #/ /////////////////////////////////////////////// IDEE : AU LIEU DE GARDER LES LIGNE QUE L'ON VEUT? ON SUPPRIME AVEC PANDAS CELLES QUE L'ON NE VEUT PAS, COMME CA ON GARDE UN FICHEIR DONNABLE A AGCOUNTS ET C'EST UN FICHIER PLUS PETIT
    # /////////////////////////////////////////////////////// -> VERIFIER SI C'EST POSSIBLE EN CONSIDERANT LES AUTRES FICHIERS (SAVE METRIC IN EXCEL ...)
    print("Converting raw data into Activity Counts")
    dom_counts, non_dom_counts = convert_AC(file_dom, file_non_dom) 
    
    #***************************************************** Selecting time intervals to be analyzed **************************************************************************

    # Loop on the number of epoches in the smallest UL file (dom_AC and non_dom_AC will have the same number of rows)
    for data_idx in range(0, min(len(dom_counts), len(non_dom_counts))) : 
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

                
                output_file_path = input_folder + "/" + "Test_output_" + comparison + ".xlsx" 
                output_wb = openpyxl.load_workbook(output_file_path)

                #******************************* Save metrics in an excel file ******************************
                time_metrics = [dict_metrics['dom_AD'], dict_metrics['non_dom_AD'],dict_metrics['bimanual_AD'], dict_metrics['use_ratio_time']]
                intensity_metrics = [dict_metrics['dom_mean_AC'], dict_metrics['non_dom_mean_AC'], dict_metrics['mean_bilateral_magnitude'], dict_metrics['mean_magnitude_ratio'], dict_metrics['maui'], dict_metrics['baui']]
                record_time = len(dom_AC) / 60 # time in min
                write_in_file(output_wb, output_file_path, record_time, idx_day, day, time_metrics, intensity_metrics)
            idx_day += 1 

    #Vérification
    
    if dom_AC != []:
        print(f"longueur heure de début : {len(non_dom_AC)}")
        print(f"longueur heure de fin : {len(non_dom_AC)}")
    else:
        messagebox.showinfo("Finish",f"Il y a une erreur : les dates des capteurs et du fichier Info ne correspondent pas pour la modalité : {modality}" )
        print(f"Il y a une erreur : les dates des capteurs et du fichier Info ne correspondent pas pour la modalité : {modality}")

    algo_end_time= datetime.now()
    print(f"L'algo dure : {algo_end_time-algo_start_time}")
    

    #***************************************************** Segmenting the data **************************************************************************
    """
        # Record's end : Data reaching the max_time (20h) or dead battery 
        elif (sec_count == max_time[idx_record] or ((min_time[idx_record] <= sec_count < max_time[idx_record]) and (sec_count == min(len(dom_counts), len(non_dom_counts)) - 1))): # and count_date == record_date[idx_record] : MARCHE PAS CAR SI LA 1E LIGNE A UNE MAUVAISE DATE IDX_RECORD N'AUGMENTE JAMAIS
            # Day is finished
            print("Calculating metrics")
    """

# Notify the user that the calculations are finished
messagebox.showinfo("Finish", f"The results are available in the folder : {input_folder}")
