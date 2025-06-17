import numpy as np
import openpyxl
from openpyxl import Workbook

file_path = "C:/Users/BEaCHILD3/Documents/Stage_Romane/Fichiers_python/Code_complet/fichiers_entree/Info.xlsx"

my_wb = openpyxl.load_workbook(file_path) 
my_sheet = my_wb.active

for row_metric in my_sheet.iter_rows(min_row = 1, max_row = 5 , min_col = 1, max_col = 5, values_only=True):
    print(row_metric)