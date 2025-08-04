""" This file contains the functions to save the metrics in an Excel file.
It selects the output file, initializes the first column with metric names, and saves the metrics for each day."""

import numpy as np
import openpyxl
from openpyxl import Workbook
import os
from openpyxl.styles import PatternFill
from openpyxl.styles import Alignment


def select_output_file(file_path, ID, therapy_name):
    """
    Selects the output file to write the metrics. If the file exists, it loads the existing data. If the file does not exist, it creates a new file and initializes the first column with metric names and save the child info.
    :param file_path: Path to the output file.
    :param ID : Str ID of the child
    :param therapy_name: Str name of the therapy ("HABIT" ou "PARTNER").
    :return my_wb: Workbook object for the output file.
    :return my_sheet: Active sheet of the workbook.
    """
    # Select file
    if os.path.exists(file_path): 
        # If file exists, save existing data and add modifications
        my_wb = openpyxl.load_workbook(file_path)  
        print("File exists, loading existing data.")
    else:
        # Create file 
        my_wb = openpyxl.Workbook()
        print("File does not exist, creating a new file.")
    
    my_sheet = my_wb.active

    # Initialize column info : define one metrics per row
    lst_info_col = ["ID du patient","Groupe","Jours", "Durée d'enregistrement (en min)", "Métriques de temps","Dominant active duration (en %)","Non dominant active duration (en %)","Bilateral active duration (en %)", "Time use ratio","Métriques d'intensité","Dominant mean AC","Non dominant mean AC","Mean bilateral magnitude","Magnitude ratio","MAUI","BAUI", "Intensity Use ratio"]
    for idx in range(1, len(lst_info_col) + 1):
        cell = my_sheet.cell(row = idx, column = 1)
        cell.value = lst_info_col[idx-1]
        cell.alignment = Alignment(wrapText =True)

        # Adjust the width of the column
        my_sheet.column_dimensions["A"].width = 30
        
        # Save the child ID
        if cell.value == "ID du patient":
            cell_ID = cell_group = my_sheet.cell(row = idx , column = 2)
            cell_ID.value = ID
        # Save the therapy name of the child
        elif cell.value == "Groupe":
            cell_group = my_sheet.cell(row = idx , column = 2)
            cell_group.value = therapy_name

        # Color the specific cells 
        elif cell.value == "Métriques de temps" or cell.value == "Métriques d'intensité":
            cell.fill = PatternFill(start_color="f1b3a6", end_color="f1b3a6", fill_type="solid")
            my_sheet.merge_cells(start_row = idx, start_column = 1, end_row = idx, end_column = 11)
        elif cell.value == "Jours":
            cell.fill = PatternFill(start_color="be6a59", end_color="be6a59", fill_type="solid")

    my_wb.save(file_path)

    return my_wb

def write_in_file(my_wb, file_path, record_time, idx_day, day, lst_time_metrics, lst_intensity_metrics):
    """
    This function writes the metrics into an Excel file. It creates a new column for each child and fills it with the corresponding metrics.
    :param my_wb : Excel file to save data.
    :param file_path : Path to the output file.
    :param record_time : Int of the minutes of recorded time for 1 day.
    :param idx_day : Int of the day index (ex : 1 for day 1).
    :param day : Datetime date of the day.
    :param lst_time_metrics: List of time metrics to write in the file.
    :param lst_intensity_metrics: List of intensity metrics to write in the file.
    :return : Save the metrics from lst_time_metrics and lst_intensity_metrics in the excel file corresponding to my_wb.
    """
    my_sheet = my_wb.active

    """************************* Insert recording time of day  ****************************"""
    rectime_cell = my_sheet.cell(row = 4, column = idx_day + 1)
    rectime_cell.value = record_time

    """************************* Add a new day in the day row ****************************"""
    cell = my_sheet.cell(row = 3, column = idx_day + 1)
    cell.value = str(day) 
    cell.fill = PatternFill(start_color="be6a59", end_color="be6a59", fill_type="solid")
    cell.alignment = Alignment(wrapText =True)


    """************************* Filling the column with metric values ****************************"""
    for idx_row in range(6, len(lst_time_metrics) + 6):
        cell = my_sheet.cell(row = idx_row, column = idx_day + 1)
        cell.value = lst_time_metrics[idx_row - 6]
    
    for idx_row in range(11, len(lst_intensity_metrics) + 11):
        cell = my_sheet.cell(row = idx_row, column = idx_day + 1)
        cell.value = lst_intensity_metrics[idx_row - 11]


    """************************* Save the file with the therapy name ****************************"""
    my_wb.save(file_path)



#def mean_std(file_path, nb_pair_child):
    """
    This function calculates the mean and standard deviation of the metrics for a given therapy.
    :param file_path: Path to the output file.
    :param nb_pair_child: Number of pair of children in the study (used to determine the column where the mean and standard deviation will be written).
    """
    """my_wb = openpyxl.load_workbook(file_path) 
    name_col_lst = ["Mean Habit", "Standard Deviation Habit", "Mean Partner", "Standard Deviation Partner"]
    
    # Loop through each worksheet in the workbook
    for my_sheet in my_wb.worksheets:
        ""****************************** Column header definition ****************************""
        #Initialize the first row with the mean and standard deviation column names
        lst_idx_col = 3 
        for name_col in name_col_lst:
            cell = my_sheet.cell(row = 1, column = nb_pair_child*2 + lst_idx_col) # /////////////// REMPLACER lst_idx_col PAR mean_std_dict.keys().index(name_col) ///////////////
            cell.value = name_col 
            cell.alignment = Alignment(wrapText =True)
            lst_idx_col += 1

        # Initialize the row index for writing mean and standard deviation
        idx_row = 2
        # Loop through each metric row (from the second row to the tenth row, assuming the metrics are in the first 10 rows)
        for row_metric in my_sheet.iter_rows(min_row = 2, max_row = 10 , min_col = 2, max_col = nb_pair_child*2 + 1, values_only=True):

            ""****************************** Saving all children values for a specific metric from a specific therapy ****************************""
            # Initialize a dict to store the distribution of values for the current metric
            distrib_therapy_dict = {"distribution HABIT": [], "distribution PARTNER": []}
            ""////////// ENLEVER LE CAS OU LA VALEUR EST = 404 (PROBLEME DE DIVISION PAR 0 DANS MAUI BAUI ET UR) //////////""
            # Loop through each value in the metric row
            for idx_col in range(1, nb_pair_child*2 + 1, 2):
                if row_metric[idx_col - 1] is not None:
                    distrib_therapy_dict["distribution HABIT"].append(row_metric[idx_col - 1]) 
            for idx_col in range(2, nb_pair_child*2 + 1, 2):
                if row_metric[idx_col - 1] is not None:
                    distrib_therapy_dict["distribution PARTNER"].append(row_metric[idx_col - 1]) 
            
            ""****************************** Writing mean and std values in excel ****************************""
            idx_col = 3
            # Loop through each value in the metric row and distribute them into the corresponding therapy list
            for therapy in distrib_therapy_dict.keys():
                if distrib_therapy_dict[therapy] != []:
                    # Write mean and standard deviation in the corresponding cells
                    cell_mean = my_sheet.cell(row = idx_row , column = nb_pair_child*2 + idx_col)
                    cell_mean.value = np.mean(distrib_therapy_dict[therapy])        
                    cell_std = my_sheet.cell(row = idx_row, column =  nb_pair_child*2 + idx_col + 1)
                    cell_std.value = np.std(distrib_therapy_dict[therapy])
                idx_col += 2

            idx_row += 1

    my_wb.save(file_path)
"""

"""************************* Example of use ****************************"""

"""lst_time_metrics = [1,1,1,1]
lst_intensity_metrics = [2,2,2,2,2,2]
record_time = 65"""
#write_in_file("test_outcome.xlsx",120, 1,lst_time_metrics,lst_intensity_metrics)
