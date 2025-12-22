""""
This file contains the calculation of different metrics.
:import interface: program that contains the interface for the Actinalyseur application, allowing users to select a folder and initiate calculations.
:import agcounts_filter : program that filter program that pre-processes the raw data and returns it as counted data (acceleration into Activity Counts).
:import segment_file: program that segments the data depending on the therapy modality and hours of activity.
:import metrics_calculation : program that calculates the movement metrics from activity counts.
:import save_metrics_in_excel : program that saves the calculated metrics in an excel file.
:import test_error : program for error detection : a message is displayed if an error prevents calculations from being performed on the input files.
:import movement_detection : program that choose the selected threshold method and compute active durations.

:return excel files that contains mean value or value for the metrics for many days.
"""

""" ******************************************************************* Import ********************************************************************************************"""
import os
from datetime import datetime
import openpyxl
from tkinter import messagebox
import threading
import time 
import pandas as pd

#from segment_file import
from interface import create_window, create_progress_interface, update_progress
from agcounts_filter import convert_AC
from segment_file import segment_time
from metrics_calculation import metrics
from save_metrics_in_excel import select_output_file, write_in_file
from test_error import test_error


""" **************************************************************** Browse files **************************************************************************"""
algo_start_time= datetime.now()

output_dir = "Activity_counts_files"

# Create an activity count folder to register the ones created in agcounts_filter.py
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

""" ******************************************************** Selecting input folder **************************************************************************"""

modalities_list = ["Vie_quotidienne", "Stage"]
input_folder, threshold_selected = create_window()

# Register the dom and non dom AC for the different time lapse
AC_for_comp = {"Vie_quotidienne" : {"comp_daily_life" : {}},
               "Stage" : {"comp_5h" : {},
                        "comp_1h30" : {}}}

""" ******************************************************** Creation of progress interface **************************************************************************"""

# Start progress interface in a thread
idx_interface = 0
progress_data = {}
interface_thread = threading.Thread(target=create_progress_interface, args = (progress_data,))
interface_thread.daemon = True  # Close the interface with the main script
interface_thread.start()

""" ******************************************************** Checking if the input folder has no errors **************************************************************************"""
test_error(input_folder, modalities_list, threshold_selected)

""" ******************************************************** Getting info from input folder **************************************************************************"""
# Count the number of files to read in the input folder
nb_file_to_read = 0
for modality in modalities_list:
    # Initialize the index of record file for the modality (ex: Stage 1)
    idx_file_modality = 1
    # Browse files in the input folder
    for file in os.listdir(input_folder):
        # Count the number of files to read
        if file.startswith(modality) and file.endswith("_Droit.csv") or file.startswith(modality) and file.endswith("_Gauche.csv"):
            nb_file_to_read +=1

nb_file_to_read = int(nb_file_to_read / 2)

# Wait for the progress interface to be created
while "bar" not in progress_data or "interface" not in progress_data:
    time.sleep(3)

for modality in modalities_list:
    # Initialize the index of record file for the modality (ex: Stage 1)
    idx_file_modality = 1

    # Initialize the gyroscope data 
    gyro_dom = {'X': [], 'Y': [], 'Z': []} 
    gyro_non_dom = {'X': [], 'Y': [], 'Z': []}

    # Browse files in the input folder
    for file in os.listdir(input_folder):  

        # Check if the file correspond to the modality
        if file.startswith(modality + "_" + str(idx_file_modality)) :
            
            # Declare that calculs for the modality are done
            never_read = False

            # Select the Info file in the input folder
            input_info_file = input_folder + "/" + modality + "_Info.xlsx" #///////////////////////////////////////////////////////// Pour mettre un nom d'enfant dans le nom du fichier

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
                messagebox.showinfo("Information manquante", f"L'identifiant de l'enfant n'est pas renseigné dans le fichier {modality}_{idx_file_modality}_Info.xlsx.")

            # Define dominant UL
            ul_list = ["Droit", "Gauche"]
            ul_list.remove(non_dom_UL)
            dom_UL = ul_list[0]

            # Define date, start time and end time of the record to analyse
            comp_daily_life, comp_1h30, comp_5h = segment_time(modality, therapy, info_sheet) 
            time_comp = {"Vie_quotidienne" : {"comp_daily_life" : comp_daily_life}, 
                        "Stage":{"comp_1h30" : comp_1h30, "comp_5h" : comp_5h}}
            
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
            # Define the file path for the dom and non dom files
            file_dom = input_folder + "/" + modality +  "_" + str(idx_file_modality) + "_" + dom_UL + ".csv"
            file_non_dom = input_folder + "/" + modality + "_" + str(idx_file_modality) + "_" + non_dom_UL + ".csv"
           
            # Update the progress bar
            progress_data["interface"].after(0, update_progress, int(idx_interface) / nb_file_to_read , progress_data["bar"], progress_data["interface"], f"Lecture des données des capteurs de '{modality}_{idx_file_modality}' ...", progress_data["message_label"],progress_data["progress_title"])
            
            # Convert the raw data into Activity Counts
            print("Converting raw data into Activity Counts")
            dom_counts, non_dom_counts = convert_AC(file_dom, file_non_dom, nb_file_to_read, idx_interface, progress_data) 

            """****************************************************** Getting gyroscope data ********************************************************************************************"""
            # Get the gyroscope data
            non_dom_data_file =   pd.read_csv(file_non_dom , header = 10, names = ["Timestamp","Accelerometer X","Accelerometer Y","Accelerometer Z","Temperature","Gyroscope X","Gyroscope Y","Gyroscope Z","Magnetometer X","Magnetometer Y","Magnetometer Z"]) 
            dom_data_file = pd.read_csv(file_dom , header = 10, names = ["Timestamp","Accelerometer X","Accelerometer Y","Accelerometer Z","Temperature","Gyroscope X","Gyroscope Y","Gyroscope Z","Magnetometer X","Magnetometer Y","Magnetometer Z"])   
            
            # Dominant
            gyro_dom['X'].extend(dom_data_file["Gyroscope X"].values.tolist())
            gyro_dom['Y'].extend(dom_data_file["Gyroscope Y"].values.tolist()) 
            gyro_dom['Z'].extend(dom_data_file["Gyroscope Z"].values.tolist()) 
            # Non dominant
            gyro_non_dom['X'].extend(non_dom_data_file["Gyroscope X"].values.tolist()) 
            gyro_non_dom['Y'].extend(non_dom_data_file["Gyroscope Y"].values.tolist()) 
            gyro_non_dom['Z'].extend(non_dom_data_file["Gyroscope Z"].values.tolist())


            """***************************************************** Selecting the AC from the time wanted intervals **************************************************************************"""            
            # Loop on the number of epoches in the smallest UL file (dom_AC and non_dom_AC will have the same number of rows)
            for data_idx in range(0, min(len(dom_counts), len(non_dom_counts))) : 
                
                # Interface
                # first param of update_progress : begining of the progress of the file + the progress of calculating metrics is the 2nd half of the file process + progression at each iteration of the loop
                progress_data["interface"].after(0, update_progress, (int(idx_interface) / nb_file_to_read) + 1/(2*nb_file_to_read) + (data_idx / (min(len(dom_counts), len(non_dom_counts))))/(nb_file_to_read*2) , progress_data["bar"], progress_data["interface"], f"Calcul des métriques pour '{modality}_{idx_file_modality}' ...",  progress_data["message_label"], progress_data["progress_title"])
                
                # Get the date and hour of the activity count
                count_date = dom_counts["Timestamp"][data_idx].date()

                # Loop on the comparison modalities
                for time_lapse_name in time_comp[modality].keys():
                    time_lapse = time_comp[modality][time_lapse_name]
                    
                    # Check that the day from the sensor is register in the info excel
                    if count_date in time_lapse.keys():

                        # Check if the date for the day already exists
                        if count_date not in AC_for_comp[modality][time_lapse_name].keys():
                            AC_for_comp[modality][time_lapse_name][count_date] =  {"dom_AC" : [],"non_dom_AC" : [], "dom_gyro" : {'X': [], 'Y': [], 'Z': []}, "non_dom_gyro" : {'X': [], 'Y': [], 'Z': []}}
                        
                        # Get start_time and end_time of the recording from the day
                        lst_start_time = time_lapse[count_date]["start_time"]
                        lst_end_time = time_lapse[count_date]["end_time"] 

                        
                        # Compare the time of the activity count with the start and end time of the activity
                        # For Stage, there can be several time lapses for the same day (ex: 9h-12h30 and 14h-16h) (need a loop)
                        if lst_start_time != [] and lst_end_time != [] and modality == "Stage":
                            # Loop on the timelapses of the excel info file (several timelapses for PARTNER)
                            for idx_hour in range(0,len(lst_start_time)):
                                # Add the new AC 
                                lst_start_time[idx_hour]
                                if dom_counts["Timestamp"][data_idx].strftime("%H:%M:%S") >= lst_start_time[idx_hour] and dom_counts["Timestamp"][data_idx].strftime("%H:%M:%S") < lst_end_time[idx_hour]:
                                    
                                    # Add AC
                                    AC_for_comp[modality][time_lapse_name][count_date]["dom_AC"].append(dom_counts.loc[data_idx, "AC"])
                                    AC_for_comp[modality][time_lapse_name][count_date]["non_dom_AC"].append(non_dom_counts.loc[data_idx, "AC"])

                                    # Add gyroscope data
                                    for considering_30Hz in range(30):
                                        # Dominant
                                        AC_for_comp[modality][time_lapse_name][count_date]["dom_gyro"]['X'].append(gyro_dom['X'][data_idx*30 + considering_30Hz])
                                        AC_for_comp[modality][time_lapse_name][count_date]["dom_gyro"]['Y'].append(gyro_dom['Y'][data_idx*30 + considering_30Hz])
                                        AC_for_comp[modality][time_lapse_name][count_date]["dom_gyro"]['Z'].append(gyro_dom['Z'][data_idx*30 + considering_30Hz])
                                        # Non dominant
                                        AC_for_comp[modality][time_lapse_name][count_date]["non_dom_gyro"]['X'].append(gyro_non_dom['X'][data_idx*30 + considering_30Hz]) 
                                        AC_for_comp[modality][time_lapse_name][count_date]["non_dom_gyro"]['Y'].append(gyro_non_dom['Y'][data_idx*30 + considering_30Hz])
                                        AC_for_comp[modality][time_lapse_name][count_date]["non_dom_gyro"]['Z'].append(gyro_non_dom['Z'][data_idx*30 + considering_30Hz])
                       
                       # Compare the time of the activity count with the start and end time of the activity
                       # For Vie_quotidienne, there is only one time lapse for the day, time can be saved by not calling the loop
                        elif lst_start_time != [] and lst_end_time != [] and modality == "Vie_quotidienne":
                            # Add the new AC and gyroscope data of selected time lapses
                            if dom_counts["Timestamp"][data_idx].strftime("%H:%M:%S") >= lst_start_time[0] and dom_counts["Timestamp"][data_idx].strftime("%H:%M:%S") < lst_end_time[0]:
                                
                                # Add AC
                                AC_for_comp[modality][time_lapse_name][count_date]["dom_AC"].append(dom_counts.loc[data_idx, "AC"])
                                AC_for_comp[modality][time_lapse_name][count_date]["non_dom_AC"].append(non_dom_counts.loc[data_idx, "AC"])
                                
                                # Add gyroscope data
                                for considering_30Hz in range(0,30):
                                    # Dominant
                                    AC_for_comp[modality][time_lapse_name][count_date]["dom_gyro"]['X'].append(gyro_dom['X'][data_idx*30 + considering_30Hz]) 
                                    AC_for_comp[modality][time_lapse_name][count_date]["dom_gyro"]['Y'].append(gyro_dom['Y'][data_idx*30 + considering_30Hz])
                                    AC_for_comp[modality][time_lapse_name][count_date]["dom_gyro"]['Z'].append(gyro_dom['Z'][data_idx*30 + considering_30Hz])
                                    # Non dominant
                                    AC_for_comp[modality][time_lapse_name][count_date]["non_dom_gyro"]['X'].append(gyro_non_dom['X'][data_idx*30 + considering_30Hz]) 
                                    AC_for_comp[modality][time_lapse_name][count_date]["non_dom_gyro"]['Y'].append(gyro_non_dom['Y'][data_idx*30 + considering_30Hz])
                                    AC_for_comp[modality][time_lapse_name][count_date]["non_dom_gyro"]['Z'].append(gyro_non_dom['Z'][data_idx*30 + considering_30Hz])
            
            """************************************************* Explore the AC lists for the different time laps to calculate the metrics ********************************************************"""
            #Initialize the activity count data
            dom_AC = []
            dom_non_AC = []
            # Initialize the gyroscope data 
            gyro_dom = {'X': [], 'Y': [], 'Z':[]}
            gyro_non_dom = {'X': [], 'Y': [], 'Z':[]}

            # Explore the AC lists for the different time laps to calculate the metrics
            for comparison in AC_for_comp[modality]:
                idx_day = 1

                for day in AC_for_comp[modality][comparison]:
                    # Declaration of the AC and gyroscope data, for the selected time lapses
                    dom_AC = AC_for_comp[modality][comparison][day]["dom_AC"]
                    non_dom_AC = AC_for_comp[modality][comparison][day]["non_dom_AC"]
                    dom_gyro = AC_for_comp[modality][comparison][day]["dom_gyro"]
                    non_dom_gyro = AC_for_comp[modality][comparison][day]["non_dom_gyro"]

                    if dom_AC != [] and non_dom_AC != []:
                        """****************************** Metrics calculation for the selected time lapse ******************************"""
                        dict_metrics = metrics(dom_AC, non_dom_AC, threshold_selected, dom_gyro, non_dom_gyro)
                        
                        print(f"Dominant Active Duration for the day {count_date}: {dict_metrics['dom_AD']}")
                        print(f"Non Dominant Active Duration for the day {count_date} : {dict_metrics['non_dom_AD']}\n")
                        print(f"Metrics saved for the day {count_date}\n")

                        # Open the output file corresponding to the comparison
                        output_file_path = input_folder + "/" + "Résultats_" + comparison + ".xlsx" 
                        output_wb = openpyxl.load_workbook(output_file_path)

                        """******************************* Save metrics in an excel file ***********************************************"""
                        time_metrics = [dict_metrics['dom_AD'], dict_metrics['non_dom_AD'],dict_metrics['bimanual_AD'],dict_metrics['unimanual_dom_AD'], dict_metrics['unimanual_non_dom_AD'], dict_metrics['use_ratio_time']]
                        intensity_metrics = [dict_metrics['dom_mean_AC'], dict_metrics['non_dom_mean_AC'], dict_metrics['mean_bilateral_magnitude'], dict_metrics['mean_magnitude_ratio'], dict_metrics['maui'], dict_metrics['baui'], dict_metrics['use_ratio_intensity']]
                        record_time = len(dom_AC) / 60 # time in min
                        write_in_file(output_wb, output_file_path, record_time, idx_day, day, time_metrics, intensity_metrics)
                    
                    # Update loop values
                    idx_day += 1 
                
                # Notify the user if the recorded hours and the hours in the info file do not match 
                if dom_AC == []:
                    messagebox.showwarning("Attention",f"Il y a une erreur : les dates ou les heures du fichier Info ne correspondent pas aux données des capteurs pour la modalité : {modality}_{idx_file_modality}_{comparison}" )
                    print(f"Il y a une erreur : les dates ou les heures du fichier Info ne correspondent pas aux données des capteurs pour la modalité : {modality}_{idx_file_modality}_{comparison}")

            # Print the algorithme calculation time
            algo_end_time= datetime.now()
            print(f"L'algo dure : {algo_end_time-algo_start_time}")

            # Update the index of record file for the modality (ex: Stage 1)
            idx_file_modality += 1

            # Update the index of the file currently read
            idx_interface += 1

# Notify the user that the calculations are finished
messagebox.showinfo("Fin", f"Les résultats sont disponibles dans le dossier : {input_folder}")

