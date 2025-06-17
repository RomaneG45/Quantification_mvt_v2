import numpy as np
import openpyxl
from openpyxl import Workbook
import os
from openpyxl.styles import PatternFill
from openpyxl.styles import Alignment

def select_output_file(file_path, sheet_name):
    """
    Selects the output file to write the metrics. If the file exists, it loads the existing data. If the file does not exist, it creates a new file and initializes the first row with metric names.
    :param file_path: Path to the output file.
    :param sheet_name: Name of the sheet to write the metrics in (ex : "Day 1").
    :return my_wb: Workbook object for the output file.
    :return my_sheet: Active sheet of the workbook.
    """
    
    if os.path.exists(file_path): 
        # If file exists, save existing data and add modifications
        my_wb = openpyxl.load_workbook(file_path)  # Save existing data
        print("File exists, loading existing data.")
    else:
        # Create file 
        my_wb = openpyxl.Workbook()
        print("File does not exist, creating a new file.")
        #sheet = my_wb.active
        #sheet.title = "Day 1"
    
    #If sheet exists, load it
    if sheet_name in my_wb.sheetnames:
        my_sheet = my_wb[sheet_name]
        print("Sheet exists, adding data to it.")

    #If sheet does not exists, create a new sheet and initialize the first row with metric names.
    else:
        if "Sheet" in my_wb.sheetnames:
            #Delete the first sheet which is empty 
            my_wb.remove(my_wb["Sheet"])

        my_sheet = my_wb.create_sheet(sheet_name) 
        print("Sheet does not exist, creating a new sheet.")

        # Initialise the first row
        cell = my_sheet.cell(row = 1, column = 1)
        cell.value = "Metrics"
        
        # Save the metric names in the 1st column
        lst_name_metrics = ["Dominant Active Duration (%)", "Non Dominant Active Duration (%)", "Use ratio", "Dominant Mean AC", "Non Dominant Mean AC", "Mean Bilateral Magnitude",  "Mean Magnitude ratio", "MAUI", "BAUI"]
        for idx in range(2, len(lst_name_metrics) + 2):
            cell = my_sheet.cell(row = idx, column = 1)
            cell.value = lst_name_metrics[idx-2]
            cell.alignment = Alignment(wrapText =True)

    return my_wb, my_sheet

def write_in_file(file_path, sheet_name, idx_pair, therapy_name, lst_metrics):
    """
    This function writes the metrics into an Excel file. It creates a new column for each child and fills it with the corresponding metrics.
    :param file_path: Path to the output file.
    :param sheet_name: Name of the sheet to write the metrics in (ex : "Day 1").
    :param idx_pair : Int index of the pair of child (0 for first pair, 1 for second pair, etc.).
    :param therapy_name: Name of the therapy ("HABIT" ou "PARTNER").
    :param lst_metrics: List of metrics to write in the file.
    """
    """/////////////////////////////////////////////////////////////////FINIR LA DOCSTRING///////////////////////////////////////////////////////////////////////"""
    
    my_wb, my_sheet = select_output_file(file_path, sheet_name)
    idx_col = 100

    """****************************** Column header definition ****************************"""
    #/////////////////////////////////POSSIBILITE DE FAIRE UNE SEULE BOUCLE////////////////////////////////////////
    # Add a new child in the first row
    if therapy_name == "HABIT" or therapy_name == "HABIT-ILE": 
        # Add child name in the first column of the pair if therapy is HABIT-ILE
        idx_col = idx_pair*2
        cell = my_sheet.cell(row = 1, column = idx_col)
        cell.value = "Jour " + str(idx_pair) + " " + therapy_name #//////////////////////////a changer avec le nombre du jour////////////////////
        cell.alignment = Alignment(wrapText =True)
    elif therapy_name == "PARTNER" or therapy_name == "PARTNERSHIP": 
        # Add child name in the second column of the pair if therapy is PARTNERSHIP 
        idx_col = (idx_pair*2) + 1
        cell = my_sheet.cell(row = 1, column = idx_col)
        cell.value = "Jour " + str(idx_pair) + " " + therapy_name   #/////////////////////////a changer avec le nombre du jour////////////////////
        cell.alignment = Alignment(wrapText =True)
    else:
        print("Therapy name not recognized. Please use 'HABIT', 'HABIT-ILE', 'PARTNER' or 'PARTNERSHIP'.") 



    """************************* Filling the column with metric values ****************************"""

    for idx_row in range(2, len(lst_metrics) + 2):
        cell = my_sheet.cell(row = idx_row, column = idx_col)
        cell.value = lst_metrics[idx_row - 2]

    """************************* Save the file with the therapy name ****************************"""
    my_wb.save(file_path)

def mean_std(file_path, nb_pair_child):
    """
    This function calculates the mean and standard deviation of the metrics for a given therapy.
    :param file_path: Path to the output file.
    :param nb_pair_child: Number of pair of children in the study (used to determine the column where the mean and standard deviation will be written).
    """
    my_wb = openpyxl.load_workbook(file_path) 
    name_col_lst = ["Mean Habit", "Standard Deviation Habit", "Mean Partner", "Standard Deviation Partner"]
    
    # Loop through each worksheet in the workbook
    for my_sheet in my_wb.worksheets:
        """****************************** Column header definition ****************************"""
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

            """****************************** Saving all children values for a specific metric from a specific therapy ****************************"""
            # Initialize a dict to store the distribution of values for the current metric
            distrib_therapy_dict = {"distribution HABIT": [], "distribution PARTNER": []}
            """////////// ENLEVER LE CAS OU LA VALEUR EST = 404 (PROBLEME DE DIVISION PAR 0 DANS MAUI BAUI ET UR) //////////"""
            # Loop through each value in the metric row
            for idx_col in range(1, nb_pair_child*2 + 1, 2):
                if row_metric[idx_col - 1] is not None:
                    distrib_therapy_dict["distribution HABIT"].append(row_metric[idx_col - 1]) 
            for idx_col in range(2, nb_pair_child*2 + 1, 2):
                if row_metric[idx_col - 1] is not None:
                    distrib_therapy_dict["distribution PARTNER"].append(row_metric[idx_col - 1]) 
            
            """****************************** Writing mean and std values in excel ****************************"""
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


"""************************* Example of use ****************************"""

lst_metrics = [2,2,2,2,2,2,2,2,2]
file_path = "C:/Users/BEaCHILD3/Documents/Stage_Romane/Fichiers_python/test_outcome.xlsx"
idx_pair = 1
therapy_name = "HABIT"
sheet_name = "Day 2"
write_in_file(file_path, sheet_name, idx_pair, therapy_name, lst_metrics)

lst_metrics = [2,2,2,2,2,2,2,2,2]
file_path = "C:/Users/BEaCHILD3/Documents/Stage_Romane/Fichiers_python/test_outcome.xlsx"
idx_pair = 2
therapy_name = "HABIT"
write_in_file(file_path, sheet_name, idx_pair, therapy_name, lst_metrics)

lst_metrics = [3,3,3,3,3,3,3,3,3]
file_path = "C:/Users/BEaCHILD3/Documents/Stage_Romane/Fichiers_python/test_outcome.xlsx"
idx_pair = 1
therapy_name = "PARTNER"

write_in_file(file_path, sheet_name, idx_pair, therapy_name, lst_metrics)

lst_metrics = [3,3,3,3,3,3,3,3,3]
file_path = "C:/Users/BEaCHILD3/Documents/Stage_Romane/Fichiers_python/test_outcome.xlsx"
idx_pair = 2
therapy_name = "PARTNER"

write_in_file(file_path, sheet_name, idx_pair, therapy_name, lst_metrics)
mean_std("Test_outcome.xlsx", 2)


