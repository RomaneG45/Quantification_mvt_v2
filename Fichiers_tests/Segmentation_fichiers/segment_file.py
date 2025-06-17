

"""This file needs an existing "Data_files" folder in the same directory as the script to save the output files."""

import pandas as pd
from pandas import DataFrame

def segment(path_dom, path_non_dom,therapy_name, output_folder):
    """
    This function segments the data from two files (dominant and non-dominant limb) into multiple files, each containing data for a single day.
    It extracts data between specified time intervals (from 08:00 to 20:00) and saves the segmented data into new CSV files (one per day).
    :param path_dom: Path to the file containing data from the dominant limb.
    :param path_non_dom: Path to the file containing data from the non-dominant limb.   
    :param therapy_name: Name of the therapy for which the data is being processed.
    :param output_folder: Folder where the segmented files will be saved.
    
    """
    #Names for the new files
    names = ["dom", "non_dom"]
    
    #Time interval to be cut
    min_time = "08:00.0000000"
    max_time = "20:00.0000000"

    #Recording of useful data only
    data_dom = pd.read_csv(path_dom, header = 10, usecols = ['Timestamp','Accelerometer X', 'Accelerometer Y', 'Accelerometer Z'])
    data_non_dom = pd.read_csv(path_non_dom, header = 10, usecols = ['Timestamp','Accelerometer X', 'Accelerometer Y', 'Accelerometer Z'])
    path_dom_non_dom = [data_dom, data_non_dom]

    #Creating design from new database
    df_dom = {'Timestamp': [],
    'Accelerometer X': [],
    'Accelerometer Y': [],
    'Accelerometer Z': [],
    }
    df_non_dom = {'Timestamp': [],
    'Accelerometer X': [], 
    'Accelerometer Y': [],
    'Accelerometer Z': [],
    }
    df_dom_non_dom = [df_dom, df_non_dom]

    print(data_dom.loc[0, "Timestamp"][-14:-1])
    #Selecting the data to copy
    valid = None 
    #Loop on the dom [0] and non dom [1] data (idx for path, df and names)
    for limb in [0,1]:
        #initialize the day counter
        day = 1

        #loop on the nuMber of epoches
        for data_idx in range(0,len(path_dom_non_dom[limb])) : 
            if path_dom_non_dom[limb].loc[data_idx, "Timestamp"][-14:-1] != min_time and path_dom_non_dom[limb].loc[data_idx, "Timestamp"][-14:-1]  != max_time and valid == True: 
                #Convertion of commas to dots to allow convertion of str data to float data
                df_dom_non_dom[limb]['Timestamp'].append(path_dom_non_dom[limb].loc[data_idx, "Timestamp"])
                df_dom_non_dom[limb]['Accelerometer X'].append(path_dom_non_dom[limb].loc[data_idx, "Accelerometer X"])
                df_dom_non_dom[limb]['Accelerometer Y'].append(path_dom_non_dom[limb].loc[data_idx, "Accelerometer Y"])
                df_dom_non_dom[limb]['Accelerometer Z'].append(path_dom_non_dom[limb].loc[data_idx, "Accelerometer Z"])

            elif path_dom_non_dom[limb].loc[data_idx, "Timestamp"][-14:-1] == min_time: 
                valid = True
            elif path_dom_non_dom[limb].loc[data_idx, "Timestamp"][-14:-1] == max_time: 
                valid = None 
                """**************************Changer le fichier à chaque fois***************************"""
                #Save the data copy in a csv
                donnees = DataFrame(df_dom_non_dom[limb], columns= ['Timestamp', 'Accelerometer X', 'Accelerometer Y', 'Accelerometer Z'])
                file_name = "Day" + str(day) + "_" + therapy_name + "_" + names[limb] + ".csv"
                export_csv = donnees.to_csv(output_folder + "/" + file_name, index = None, header=True, encoding='utf-8', sep=',')
                print("File save")

                #Reset the design for the next day
                df_dom_non_dom[limb] = {'Timestamp': [],
                'Accelerometer X': [], 
                'Accelerometer Y': [],
                'Accelerometer Z': [],
                }

                #Next day 
                day += 1


path_dom =  "C:/Users/BEaCHILD3/Documents/Stage_Romane/Donnees_actilife/Enregistrement_15_04_2025/TAS1D48140076_(2025-04-16)-IMU-Copie.csv" 
path_non_dom = "C:/Users/BEaCHILD3/Documents/Stage_Romane/Donnees_actilife/Enregistrement_15_04_2025/TAS1H46190449_(2025-04-16)-IMU-Copie.csv"
therapy_name = "HABIT"
segment(path_dom, path_non_dom,therapy_name)




"""{'Gyroscope X':[],'Gyroscope Y':[],'Gyroscope Z':[]}"""


