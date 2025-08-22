"""This file select the time interval to analyse depending on the modality and the therapy recorded (HABIT/PARTNER and daily_life center or daily life at home)
called in main.py"""

from datetime import datetime, time


def segment_time(modality, therapy, info_sheet):
    """This function segments a file, depending on the therapy modality and hours of activity. If record in center, the file is segmented from 8h to 20h. If at home, the file is segmented depending on the hours of activity (parent's annotations).
    :param modality (str) : the modality type ("Vie_quotidienne" or "Stage").
    :param therapy (str) : the therapy name ("HABIT" or "PARTNER").
    :param info_sheet (openpyxl.Workbook()) : sheet that contains the start and end time of records.
    :return comp_vie_quot (dict) : dict with the date as key and the start and end time of the activity as value.
    :return comp_1h30 (dict) : dict with the date as key and the start and end time of the activity as value.
    :return comp_5h (dict) : dict with the date as key and the start and end time of the activity as value.
    """
    comp_5h = {}
    comp_1h30 = {}
    comp_vie_quot = {}
    # Variable insert once 9h (or 12h) in the start time for Stage 
    add_9h = True
    add_12h30 = True
    
    for row in info_sheet.iter_rows(min_row=2):

        if modality == "Vie_quotidienne":

            if row[4].value is not None: #row[4] correspond to the E column = the date column
                row_date = row[4].value.date()
                comp_vie_quot[row_date] = {"start_time" : ["08:00:00"], "end_time" : ["20:00:00"]}

            # Get the date
            if row[4].value is not None:
                row_date = row[4].value.date()
                comp_5h[row_date] = {"start_time" : [], "end_time" : []}
                comp_1h30[row_date] = {"start_time" : [], "end_time" : []}

        elif therapy == "PARTNER":

            # Get the date
            if row[4].value is not None:
                # Create a new date key
                row_date = row[4].value.date()
                # //////////////////////////////////////////////////////////////////////: AJOUTER : si row_date not in comp_5h.keys() et comp_1h30.keys()
                if row_date not in comp_5h.keys():
                    comp_5h[row_date] = {"start_time" : [], "end_time" : []}
                if row_date not in comp_1h30.keys():
                    comp_1h30[row_date] = {"start_time" : [], "end_time" : []}

            # Get the start hours 
            if isinstance(row[8].value, time):
                comp_1h30[row_date]["start_time"].append(row[8].value.strftime("%H:%M:%S"))
                if row[8].value > datetime.strptime("09:00:00", "%H:%M:%S").time() and add_9h == True :
                    comp_5h[row_date]["start_time"].append("09:00:00") 
                    add_9h = False
                comp_5h[row_date]["start_time"].append(row[8].value.strftime("%H:%M:%S")) 

            # Get the end hours 
            if isinstance(row[9].value, time):
                comp_1h30[row_date]["end_time"].append(row[9].value.strftime("%H:%M:%S")) 
                if row[9].value > datetime.strptime("12:30:00", "%H:%M:%S").time() and add_12h30 == True: 
                    comp_5h[row_date]["end_time"].append("12:30:00")
                    add_12h30 = False
                comp_5h[row_date]["end_time"].append(row[9].value.strftime("%H:%M:%S")) 

            if row[4].value is not None: #row[4] correspond to the E column = the date column
                row_date = row[4].value.date()
                comp_vie_quot[row_date] = {"start_time" : ["08:00:00"], "end_time" : ["20:00:00"]}
        
        elif therapy == "HABIT":
            
            if row[4].value is not None:
                # Get the date
                row_date = row[4].value.date()
                comp_5h[row_date] = {"start_time" : ["09:00:00","14:30:00"], "end_time" : ["12:30:00","16:00:00"]}
                comp_1h30[row_date] = {"start_time" : ["14:30:00"], "end_time" : ["16:00:00"]}

            if row[4].value is not None: #row[4] correspond to the E column = the date column
                row_date = row[4].value.date()
                comp_vie_quot[row_date] = {"start_time" : ["08:00:00"], "end_time" : ["20:00:00"]}

    return comp_vie_quot, comp_1h30, comp_5h  