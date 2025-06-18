""""
HOURS SELECTION IN DATETIME AND IN STR AND CONVERSION IN SECONDES
FILE COMPUTING METRICS FOR THE HOURS WRITTEN IN EXCEL ( = VIE QUOTIDIENNE OU PARTNER DOMICILE)

This file contains the calculation of different metrics.
:import segment_file : program that cuts 1 file of N days into N file of 1 day (from 8h to 20h).
:import agcounts_filter : program that filter program that pre-processes the raw data and returns it as counted data (acceleration into Activity Counts).
:import metrics_calculation : program that program that calculates the movement metrics from activity counts.

:return excel files that contains mean value or value for 8 metrics.
"""

""" ******************************************************************* Import ********************************************************************************************"""
#import pandas as pd
#import numpy as np
#from agcounts.extract import get_counts
#import matplotlib.pyplot as plt
import openpyxl
#from openpyxl import Workbook
#import os
from datetime import datetime, time

#from segment_file import
from interface import select_input_file
from agcounts_filter import convert_AC
from metrics_calculation import metrics
from save_metrics_in_excel import select_output_file, write_in_file, mean_std

#/////////////////////////AJOUTER UNE BOUCLE POUR PARCOURIR TOUS LES FICHIERS D'UN DOSSIER = AVOIR LES DONNEES DOM NON DOM DE PLUSIEURS ENFANTS//////////////////////////////
"""Pour lister les fichiers contenus dans un dossier :
files_data= os.list("Chemin du dossier contenant les fichiers")
"""
algo_start_time= datetime.now()
""" ***************************************************** Getting info from input folder **************************************************************************"""
# Ask input folder
input_folder = select_input_file()
input_info_file = input_folder + "/" + "Info.xlsx"

# Load excel file containing the information
info_wb = openpyxl.load_workbook(input_info_file)
# Select the sheet 
info_sheet = info_wb.active

# Define the important information (selecting info from info_input_file)
child_id = str(info_sheet["A2"].value)
therapy = str(info_sheet["B2"].value)
modality = str(info_sheet["C2"].value)
non_dom_UL = str(info_sheet["D2"].value)
#//////////////////////////////////// AJOUTER LA MODALITE : VIE QUOT OU STAGE //////////////////////////

#////////////////////////////////////////////// TIME //////////////////////////////////////////////////////////////
record_start_time = []
record_end_time = []
record_date = []
"""
Comparaison 1h30
PARTNER : on recupère la date et l'heure dans le fichier excel
HABIT : 8h 20h tous les jours et 

Comparaison 5h:
PARTNER et HABIT : 
"""
for date in info_sheet["E"]: 
    # Choose only datetime value to remove the title line
    if date.value == None and type(date.value) != str :
        record_date.append(record_date[-1]) 
    elif type(date.value) != str :
        record_date.append(date.value) #date.value.strftime("%Y-%m-%d") #on peut peut etre juste prendre la valeur de la case

for start_time in info_sheet["I"]:
    # Choose only datetime value to remove the title line
    if isinstance(start_time.value, time): 
        record_start_time.append(start_time.value.strftime("%H:%M:%S")) 

for end_time in info_sheet["J"] :
    # Choose only datetime value to remove the title line
    if isinstance(end_time.value, time): 
        record_end_time.append(end_time.value.strftime("%H:%M:%S")) 

print(f"record start time {record_start_time}")
print(f"record end time {record_end_time}")
print(f"record date {record_date}")
# /////////////////////////////////////////////////////// A CHANGER //////////////////////////////////////////////
dom_UL = "Droit"


# Create the output file
output_file_path = input_folder + "/" + "Test_outcome.xlsx"
output_wb = select_output_file(output_file_path, child_id, therapy)

""" #****************************************************** Getting AC ********************************************************************************************"""


file_dom = input_folder + "/" + dom_UL + ".csv"
file_non_dom = input_folder + "/" + non_dom_UL + ".csv"
print("Converting raw data into Activity Counts")
dom_counts, non_dom_counts = convert_AC(file_dom, file_non_dom)
#file_dom = "C:/Users/BEaCHILD3/Documents/Stage_Romane/Fichiers_python/Ex_arborescence/Paire 1/dom_HABIT.csv" 
#file_non_dom = "C:/Users/BEaCHILD3/Documents/Stage_Romane/Fichiers_python/Ex_arborescence/Paire 1/non_dom_HABIT.csv" 

""" #***************************************************** Selecting time intervals to be analyzed **************************************************************************"""
#////////////////////////////// Creer un dict pour indiquer les créneaux à garder par jour /////////////////////////
# Time interval to be cut
#min_time = "10:00:00"  
#max_time = "11:00:00"  

if therapy == "HABIT":
    min_time = ["09:00:00"]
    max_time = ["16:00:00"]
elif therapy == "PARTNER":
    min_time = record_start_time # temps renseigné + 9h (attention à l'ordre)
    max_time = record_end_time # temps renseigné + 12h30 (attention à l'ordre) 9h et 12h30 doivent etre à la meme place
else:
    print("Therapie non reconnue")

for time in range(len(min_time)) :
    # Converting HH : MM : SS time into seconds
    h, m, s = map(int, min_time[time-1].split(":"))
    min_time[time-1] = h * 3600 + m * 60 + s

for time in range(len(max_time)) : 
    h, m, s = map(int, max_time[time-1].split(":"))
    max_time[time-1] = h * 3600 + m * 60 + s

print(record_date)
print("*********************")

""" #***************************************************** Segmenting the data **************************************************************************"""
print("Segmenting data")

# Initialize the day counter
day = 1
idx_record = 0

# Initialize the lists of AC for dominant and non dominant ULs 
dom_AC = []
non_dom_AC = []

# Loop on the number of epoches in the smallest UL file (dom_AC and non_dom_AC will have the same number of rows)
for data_idx in range(0, min(len(dom_counts), len(non_dom_counts))) : 
    # Converting count time to second
    h, m, s = map(int, dom_counts["Timestamp"][data_idx].strftime('%H:%M:%S').split(":"))
    sec_count = h * 3600 + m * 60 + s
    count_date = dom_counts["Timestamp"][data_idx].strftime("%Y-%m-%d")

    # Saving Data between max_time and min_time for the metrics calculation
    if (min_time[idx_record] <= sec_count < max_time[idx_record]) and (sec_count != min(len(dom_counts), len(non_dom_counts)) - 1): # and count_date == record_date[idx_record] : # et dates correspondantes :
        dom_AC.append(dom_counts.loc[data_idx, "AC"])
        non_dom_AC.append(non_dom_counts.loc[data_idx, "AC"])

    
    # Record's end : Data reaching the max_time (20h) or dead battery 
    elif (sec_count == max_time[idx_record] or ((min_time[idx_record] <= sec_count < max_time[idx_record]) and (sec_count == min(len(dom_counts), len(non_dom_counts)) - 1))): # and count_date == record_date[idx_record] : MARCHE PAS CAR SI LA 1E LIGNE A UNE MAUVAISE DATE IDX_RECORD N'AUGMENTE JAMAIS
        # Day is finished
        print("Calculating metrics")
        """#****************************** Metrics calculation for the selected time lapse ******************************"""
        dict_metrics = metrics(dom_AC,non_dom_AC)
        print(f"Dominant Active Duration for the day {day}: {dict_metrics['dom_AD']}")
        print(f"Non Dominant Active Duration for the day {day} : {dict_metrics['non_dom_AD']}\n")
        print(f"Metrics saved for the day {day}\n")

        """#****************************** Save metrics in an excel file ******************************"""
        time_metrics = [dict_metrics['dom_AD'], dict_metrics['non_dom_AD'],dict_metrics['bimanual_AD'], dict_metrics['use_ratio_time']]
        intensity_metrics = [dict_metrics['dom_mean_AC'], dict_metrics['non_dom_mean_AC'], dict_metrics['mean_bilateral_magnitude'], dict_metrics['mean_magnitude_ratio'], dict_metrics['maui'], dict_metrics['baui']]
        record_time = len(dom_AC) / 60 # time in min
        write_in_file(output_wb, output_file_path, record_time, day, time_metrics, intensity_metrics)

        # Check that the recording is not the last one (if so, it is not necessary to update for the next one)
        if idx_record != (len(max_time) - 1):
        # Update of the records index (if new end time) and the days index (if current record date is different from next record date)
            if record_date[idx_record] != record_date[idx_record + 1]:
                # For next day 
                dom_AC = []
                non_dom_AC = []
                day += 1
            idx_record += 1

        # Maintain the start and end times in list format to coincide with the data of the PARTNER internship at home
        if therapy == "HABIT":
            min_time.append(min_time[0])
            max_time.append(min_time[0])
    


        
algo_end_time = datetime.now()


process_time = algo_end_time - algo_start_time 
print(f"Processing time : {process_time}")
