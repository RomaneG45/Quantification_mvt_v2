"""This file select the time interval to analyse depending on the modality and the therapy recorded (HABIT/PARTNER and daily_life center or daily life at home)"""

from datetime import datetime, time


def segment_time(modality, therapy, info_sheet):
    """This function segments a file, depending on the therapy modality and hours of activity. If record in center, the file is segmented from 8h to 20h. If at home, the file is segmented depending on the hours of activity (parent's annotations)
    :param modality : Str of the modality type ("Vie_quotidienne" or "Stage")
    :param therapy : Str of the therapy name ("HABIT" or "PARTNER")
    :param info_sheet : Workbook sheet that contains the start and end time of records
    :return record_date : list of the dates of records
    :return lst_record_start_time : list of lists, first list is the start times for 5h comparison, second list is the start times for 1h30 comparison
    :return lst_record_end_time : list of lists, first list is the end times for 5h comparison, second list is the end times for 1h30 comparison
    """

    # Lists that contain start time and end time in a specific time lapse (5h and 1h30)
    record_1h30_start_time = []
    record_1h30_end_time = []
    record_5h_start_time = []
    record_5h_end_time = []
    record_date = []

    # Lists that cointain the lists of start time and end time for a specific time lapse, thus the lists have all the timelapse
    lst_record_start_time = []
    lst_record_end_time = []

    # Variable insert once 9h (or 12h) in the start time for Stage 
    add_9h = True
    add_12h30 = True

    # Save dates
    for date in info_sheet["E"]: 
        # Choose only datetime value to remove the title line
        if date.value == None and type(date.value) != str :
            record_date.append(record_date[-1]) 
        elif type(date.value) != str :
            record_date.append(date.value) #date.value.strftime("%Y-%m-%d") #on peut peut etre juste prendre la valeur de la case

    print(modality)
    if modality == "Vie_quotidienne":
        lst_record_start_time.append(["08:00:00"])
        lst_record_end_time.append(["20:00:00"])

    elif modality == "Stage" :

        if therapy == "PARTNER":
            for start_time in info_sheet["I"]:
                # Choose only datetime value to remove the title line
                if isinstance(start_time.value, time): 
                    record_1h30_start_time.append(start_time.value.strftime("%H:%M:%S")) 
                    if start_time.value > datetime.strptime("09:00:00", "%H:%M:%S").time() and add_9h == True: 
                        record_5h_start_time.append("09:00:00") 
                        add_9h = False
                    record_5h_start_time.append(start_time.value.strftime("%H:%M:%S")) 
            lst_record_start_time.append(record_5h_start_time)
            lst_record_start_time.append(record_1h30_start_time)

            for end_time in info_sheet["J"] :
                # Choose only datetime value to remove the title line
                if isinstance(end_time.value, time): 
                    record_1h30_end_time.append(end_time.value.strftime("%H:%M:%S")) 
                    if end_time.value > datetime.strptime("12:30:00", "%H:%M:%S").time() and add_12h30 == True:
                        record_5h_end_time.append("12:30:00")
                        add_12h_30 = False
                    record_5h_end_time.append(end_time.value.strftime("%H:%M:%S")) 
            lst_record_end_time.append(record_5h_end_time)
            lst_record_end_time.append(record_1h30_end_time)

        elif therapy == "HABIT":
            # For 5h comparison
            lst_record_start_time.append(["09:00:00","14:30:00"])
            lst_record_end_time.append(["12:30:00","16:00:00"])   
            # For 1h30 comparison
            lst_record_start_time.append(["14:30:00"])  
            lst_record_end_time.append(["16:00:00"])

    return record_date, lst_record_start_time, lst_record_end_time    