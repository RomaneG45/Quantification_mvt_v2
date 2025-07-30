"""Ce fichier a pour but de selectionner les passages utiles dans les fichiers d'enregistrement, et de supprimer le reste"""

import pandas as pd
from pandas import DataFrame

#-----------------------------------------------------------A COMPLETER---------------------------------------------------------------------------------

#Time interval to be cut
min_time = "2024-12-05T09:00:00.0000000Z"
max_time = "2024-12-05T11:00:00.0000000Z"
#Files paths
path_left_wrist = "C:/Users/roman/Documents/BEaCHILD/Quantification_mvt_v3/Quantification_mvt_v3/Ex_arborescence/Enfant 1/Vie_quotidienne_Droit.csv" 
path_right_wrist = "C:/Users/roman/Documents/BEaCHILD/Quantification_mvt_v3/Quantification_mvt_v3/Ex_arborescence/Enfant 1/Vie_quotidienne_Gauche.csv"
#New name : indicate the path
new_name_left ="C:/Users/roman/Documents/BEaCHILD/Quantification_mvt_v3/Quantification_mvt_v3/Ex_arborescence/Enfant 2/Vie_quotidienne_Droit_.csv" 
new_name_right = "C:/Users/roman/Documents/BEaCHILD/Quantification_mvt_v3/Quantification_mvt_v3/Ex_arborescence/Enfant 2/Vie_quotidienne_Gauche_.csv"

#-------------------------------------------------------------------------------------------------------------------------------------------------------


#Recording of useful data only
data_left_wrist = pd.read_csv(path_left_wrist, header = 10, usecols = ['Timestamp','Accelerometer X', 'Accelerometer Y', 'Accelerometer Z'])
data_right_wrist = pd.read_csv(path_right_wrist, header = 10, usecols = ['Timestamp','Accelerometer X', 'Accelerometer Y', 'Accelerometer Z'])


#Creating design from new database
df_left = {'Timestamp': [],
'Accelerometer X': [],
'Accelerometer Y': [],
'Accelerometer Z': [],
}

#Selecting the data to copy
valid = None 
for data_idx in range(len(data_left_wrist)) : 
    if data_left_wrist.loc[data_idx, "Timestamp"] != min_time and data_left_wrist.loc[data_idx, "Timestamp"]  != max_time and valid == True: 
        #Convertion of commas to dots to allow convertion of str data to float data
        df_left['Timestamp'].append(data_left_wrist.loc[data_idx, "Timestamp"])
        df_left['Accelerometer X'].append(data_left_wrist.loc[data_idx, "Accelerometer X"])
        df_left['Accelerometer Y'].append(data_left_wrist.loc[data_idx, "Accelerometer Y"])
        df_left['Accelerometer Z'].append(data_left_wrist.loc[data_idx, "Accelerometer Z"])

    elif data_left_wrist.loc[data_idx, "Timestamp"] == min_time: 
        valid = True
    elif data_left_wrist.loc[data_idx, "Timestamp"] == max_time: 
        valid = None 

#Save the data copy in a csv
donnees = DataFrame(df_left, columns= ['Timestamp', 'Accelerometer X', 'Accelerometer Y', 'Accelerometer Z'])
export_csv = donnees.to_csv(new_name_left, index = None, header=True, encoding='utf-8', sep=',')



#Creating design from new database
df_right = {'Timestamp': [],
'Accelerometer X': [],
'Accelerometer Y': [],
'Accelerometer Z': [],
}

#Selecting the data to copy
valid = None
for data_idx in range(len(data_right_wrist)) : 
    if data_right_wrist.loc[data_idx, "Timestamp"] != min_time and data_right_wrist.loc[data_idx, "Timestamp"]  != max_time and valid == True: 
        #Convertion of commas to dots to allow convertion of str data to float data
        df_right['Timestamp'].append(data_right_wrist.loc[data_idx, "Timestamp"])
        df_right['Accelerometer X'].append(str(data_right_wrist.loc[data_idx, "Accelerometer X"]))
        df_right['Accelerometer Y'].append(str(data_right_wrist.loc[data_idx, "Accelerometer Y"]))
        df_right['Accelerometer Z'].append(str(data_right_wrist.loc[data_idx, "Accelerometer Z"]))
    elif data_right_wrist.loc[data_idx, "Timestamp"] == min_time: 
        valid = True
    elif data_right_wrist.loc[data_idx, "Timestamp"] == max_time: 
        valid = None 

#Save the data copy in a csv
donnees = DataFrame(df_right, columns= ['Timestamp', 'Accelerometer X', 'Accelerometer Y', 'Accelerometer Z'])
export_csv = donnees.to_csv(new_name_right, index = None, header=True, encoding='utf-8', sep=',')
