import struct

with open("C:/Users/BEaCHILD3/Documents/Stage_Romane/ML/Données validation RCT2/Données validation RCT2/Protocole standardisé_Annotations_BIN_RCT2/Brest/02.10.02/21_9_2/0ST298.BIN", "rb") as file:
    binary_data = file.read()


# Exemple : Lire une suite d'entiers 32 bits
numbers = struct.unpack("I" * (len(binary_data) // 4), binary_data)
print(numbers)
