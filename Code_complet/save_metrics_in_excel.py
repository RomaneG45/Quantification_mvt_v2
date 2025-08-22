""" This file contains the functions to save the metrics in an Excel file.
It selects the output file, initializes the first column with metric names, and saves the metrics for each day.
Called in main.py"""

import openpyxl
from openpyxl import Workbook
import os
from openpyxl.styles import PatternFill
from openpyxl.styles import Alignment


def select_output_file(file_path, ID, therapy_name):
    """
    Selects the output file to write the metrics. If the file exists, it loads the existing data. If the file does not exist, it creates a new file and initializes the first column with metric names and save the child info.
    :param file_path (str) : path to the output file.
    :param ID (str) : ID of the child.
    :param therapy_name (str) : name of the therapy ("HABIT" ou "PARTNER").
    :return my_wb (openpyxl.Workbook()) : workbook object for the output file.
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
    :param my_wb (openpyxl.Workbook()) : excel file to save data.
    :param file_path (str) : path to the output file.
    :param record_time (int) : minutes of recorded time for 1 day.
    :param idx_day (int) : day index (ex : 1 for day 1).
    :param day (datetime.date()) : date of the day.
    :param lst_time_metrics (list) : time metrics to write in the file.
    :param lst_intensity_metrics (list): intensity metrics to write in the file.
    :return : save the metrics from lst_time_metrics and lst_intensity_metrics in the excel file corresponding to my_wb.
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
