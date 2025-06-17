""""
COPY OF MAIN BEFORE CHANGING THE HOURS SELECTION CRITERIA (SELECTION EN DATETIME ET EN STR ET EN CONVERSION EN SECONDES)

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
from datetime import datetime

#from segment_file import
from interface import select_input_file
from agcounts_filter import convert_AC
from metrics_calculation import metrics
from save_metrics_in_excel import select_output_file, write_in_file, mean_std

#/////////////////////////AJOUTER UNE BOUCLE POUR PARCOURIR TOUS LES FICHIERS D'UN DOSSIER = AVOIR LES DONNEES DOM NON DOM DE PLUSIEURS ENFANTS//////////////////////////////
"""Pour lister les fichiers contenus dans un dossier :
files_data= os.list("Chemin du dossier contenant les fichiers")
"""
start_time= datetime.now()
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
non_dom_UL = str(info_sheet["C2"].value)
# /////////////////////////////////////////////////////// A CHANGER //////////////////////////////////////////////
dom_UL = "Droit"

# Create the output file
output_file_path = input_folder + "/" + "Test_outcome.xlsx"
output_wb = select_output_file(output_file_path, child_id, therapy)

""" ****************************************************** Getting AC ********************************************************************************************"""

file_dom = input_folder + "/" + dom_UL + ".csv"
file_non_dom = input_folder + "/" + non_dom_UL + ".csv"
print("Converting raw data into Activity Counts")
dom_counts, non_dom_counts = convert_AC(file_dom, file_non_dom)
#file_dom = "C:/Users/BEaCHILD3/Documents/Stage_Romane/Fichiers_python/Ex_arborescence/Paire 1/dom_HABIT.csv" 
#file_non_dom = "C:/Users/BEaCHILD3/Documents/Stage_Romane/Fichiers_python/Ex_arborescence/Paire 1/non_dom_HABIT.csv" 

""" ***************************************************** Segmenting the data **************************************************************************"""
print("Segmenting data")
# Time interval to be cut
#////////////////////////////// CHANGER LE TEMPS EN HEURE (ICI EN MINUTES) ////////////////////////////////
#////////////////////////////// Creer un dict pour indiquer les créneaux à garder par jour /////////////////////////
"""A GARDER POUR APRES
min_time = "08:00:00"
max_time = "20:00:00"
"""
min_time = "10:00:00"  #datetime.strptime("09:00:00", "%H:%M:%S").time()#
max_time = "11:00:00"  #datetime.strptime("16:00:00", "%H:%M:%S").time()#
#Converting HH : MM : SS time into seconds
h, m, s = map(int, min_time.split(":"))
min_time = h * 3600 + m * 60 + s
h, m, s = map(int, max_time.split(":"))
max_time = h * 3600 + m * 60 + s

# Initialize the condition to register data between 8h and 20h
valid = None 
# Initialize the day counter
day = 1

dom_AC = []
non_dom_AC = []

# Loop on the number of epoches in the smallest file (dom_AC and non_dom_AC will have the same number of rows)
for data_idx in range(0, min(len(dom_counts), len(non_dom_counts))) : 
    #Converting time to second
    h, m, s = map(int, dom_counts["Timestamp"][data_idx].strftime('%H:%M:%S').split(":"))
    sec_count = h * 3600 + m * 60 + s

    if (min_time <= sec_count < max_time) and sec_count != min(len(dom_counts), len(non_dom_counts)) - 1:
    #Data between 8h and 20h
    #if dom_counts["Timestamp"].dt.time[data_idx] != min_time and dom_counts["Timestamp"].dt.time[data_idx] != max_time and valid == True: 
    # LIGNE POUR LE TEST    
    #if dom_counts["Timestamp"][data_idx].strftime('%H:%M:%S') != min_time and dom_counts["Timestamp"][data_idx].strftime('%H:%M:%S') != max_time and valid == True: 
        #/////////////////////////////////////////// SELECTION DES DONNEES ENTRE 8H ET 20H ///////////////////////////////////////////
       # time_count = dom_counts["Timestamp"].dt.time[data_idx]

        #COMPARAISON EN DATETIME ET PAS EN STR
    #if (min_time <= time_count < max_time) and time_count != min(len(dom_counts), len(non_dom_counts)) - 1: 
        dom_AC.append(dom_counts.loc[data_idx, "AC"])
        non_dom_AC.append(non_dom_counts.loc[data_idx, "AC"])

    
        """Mettre  min_tim =< data < max_time à la place de > min_time au cas ou l'enregistrement commence après 8h"""
        
        """# Data reaching the min_time (8h)
        elif dom_counts["Timestamp"][data_idx].strftime('%H:%M:%S')  == min_time: 
            valid = True
            #Reset the lists for the next day
            dom_AC = []
            non_dom_AC = []
        """
        

    # Data reaching the max_time (20h)
    #///////////////////////////////////// OU SI PLUS DE BATTERIE : CA DEPEND COMBIEN DE TEMPS MIN ON GARDE ////////////////////////////////////////
    #elif dom_counts["Timestamp"][data_idx].strftime('%H:%M:%S')  == max_time: 
    #elif time_count == max_time or ((min_time <= time_count < max_time) & (time_count == min(len(dom_counts), len(non_dom_counts)) - 1)):
    #SECONDS
    elif sec_count == max_time or ((min_time <= sec_count < max_time) & (sec_count == min(len(dom_counts), len(non_dom_counts)) - 1)) :
        # Day is finished
        print("Calculating metrics")
        valid = None 
        """****************************** Metrics calculation for the selected time lapse ******************************"""
        dict_metrics = metrics(dom_AC,non_dom_AC)
        print(f"Dominant Active Duration for the day {day}: {dict_metrics['dom_AD']}")
        print(f"Non Dominant Active Duration for the day {day} : {dict_metrics['non_dom_AD']}\n")
        print(f"Metrics saved for the day {day}\n")

        """****************************** Save metrics in an excel file ******************************"""
        time_metrics = [dict_metrics['dom_AD'], dict_metrics['non_dom_AD'],dict_metrics['bimanual_AD'], dict_metrics['use_ratio_time']]
        intensity_metrics = [  dict_metrics['dom_mean_AC'], dict_metrics['non_dom_mean_AC'], dict_metrics['mean_bilateral_magnitude'], dict_metrics['mean_magnitude_ratio'], dict_metrics['maui'], dict_metrics['baui']]
        record_time = len(dom_AC) / 60 # time in min
        write_in_file(output_wb, output_file_path, record_time, day, time_metrics, intensity_metrics)

        #//////////////////////////////////////////////CHANGER LE NB DE PAIRES D'ENFANTS (2e PARAMETRE)//////////////////////////////////////////////
        #mean_std("Test_outcome.xlsx",2)
        #print(f"Mean and standard deviation saved for the day {day}\n")

        # For next day 
        dom_AC = []
        noon_dom_AC = []
        day += 1

        
end_time = datetime.now()


process_time = end_time - start_time 
print(process_time)