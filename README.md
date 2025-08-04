## Actinalyseur

### Pré requis
- 3.8 < python < 3.12
- openpyxl==3.1.2
- pandas==2.2.2
- numpy==1.24.4
- customtkinter==5.2.0
- agcounts== 0.2.6 

### Guide d'installation
Téléchargez le dossier "Code_complet" puis executez la commande suivante dans le terminal de l'ordinateur, à l'endroit où se trouve le dossier téléchargé : "pyinstaller main.spec". Le fichier éxecutable se télécharge dans le dossier "dist" (dossier Code_complet), puis peut être directement utilisé en double cliquant sur l'icône.

### Structure des dossiers
Code complet : Dossier contenant les scripts actuels
  - agcounts_filter.py : Fichier de traitement permettant de transformer les données brutes en activity count (transformation en activity count).
  - interface.py : Interface de l'application Actinalyseur, permettant aux utilisateurs de sélectionner un dossier et de lancer des calculs, d'afficher une barre de progression et d'être avertis lorsque les résultats sont disponibles.
  - main.py : Code principal, appelant successivement les fichiers de l'interface (interface.py), de séléction des heures (segment_file.py), de transformation des données brutes en activity counts (agcounts_filter.py), de calculs des métriques (metrics_calculation.py) et de sauvegarde des résultats dans les fichiers excel de sortie (save_metrics_in_excel.py).
  - metrics_calculation.py : Fichier de calcul des métriques.
  - save_metrics_in_excel.py : Fichier enregistrant les résultats des métriques dans les fichiers excel de sortie.
  - segment_file.py : Fichier permettant de diviser un fichier d'enregistrement couvrant plusieurs jours en plusieurs fichiers d'un jour, selon les dates spécifiées en entrée d'algorithme.
  - Activity counts files : Dossier contenant les fichiers de sauvegarde des activity counts après traitement des données brutes dans le programme principal.
      - dom_counts : AC du membre dominant
      - non_dom_counts : AC du membre atteint
  
Fichiers_tests : Dossier contenant les fichiers de test qui ont été utilisés pour écrire les scripts actuels.

Ex_arborescence : Dossier contenant des exemples de fichiers d'entrée. Utilisés pour tester le fonctionnement des scripts actuels.

## Entrée 
Doit se trouver au minimum dans le dossier d’entrée:
  - Stage_1_Droit.csv
  - Stage_1_Gauche.csv
  - Stage_Info.xlsx
  - Vie_quotidienne_1_Droit.csv
  - Vie_quotidienne_1_Gauche.csv
  - Vie_quotidienne_Info.xlsx

## Sortie
Les fichiers de sortie sont enregistrés dans le dossier sélectionné en entrée (l’adresse est indiquée dans la fenêtre de fin d’algorithme):
- Résultats_comp_1h30.xlsx 
- Résultats_comp_5h.xslx 
- Résultats_comp_daily_life.xlsx

