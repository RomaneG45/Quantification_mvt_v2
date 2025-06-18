import struct
import numpy as np

with open("C:/Users/BEaCHILD3/Documents/Stage_Romane/ML/Données validation RCT2/Données validation RCT2/Protocole standardisé_Annotations_BIN_RCT2/Brest/02.10.02/21_9_2/0LW131.BIN", "rb") as file:
    binary_data = file.read()


# Exemple : Lire une suite d'entiers 32 bits
numbers = struct.unpack("I" * (len(binary_data) // 4), binary_data)
print(np.mean(numbers))

#print(numbers[0:10])
# Conversion des m/s en g
numbers_g = np.dot(numbers , 0.10197)
print(np.mean(numbers_g))

une_col = len(numbers) / 6 # 6 = nb de colonnes
duree_sec = une_col / 128 # 128 = freq d'échantillonage (dans doc CAP sur le drive) # une_col_une_sec = nombre de secondes dans l'enregistrement
duree_minute = duree_sec / 60
freq = une_col / 1480.32 #on obtient 105

#print(duree_sec) #1480 = nb de sec de l'enregistrement vidéo (sur excel)

#Une donnée correspond à l'accélération (unité?) pour 1/128 de sec. Il y a 6 catégories différentes : Accélération (X,Y,Z) et Gyroscope (X,Y,Z)