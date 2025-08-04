## Actinalyseur

### Pré requis
3.8 < python < 3.12
openpyxl==3.1.2
pandas==2.2.2
numpy==1.24.4
customtkinter==5.2.0
agcounts== 0.2.6 

### Guide d'installation
Téléchargez le dossier "Code_complet" puis executez la commande suivante dans le terminal de l'ordinateur "pyinstaller main.spec". Le fichier éxecutable se télécharge dans le dossier "dist" (dossier Code_complet), puis peut être directement utilisé en double cliquant sur l'icône.

### Structure des dossiers
Activity counts files : folder containing the backup files of the activity counts after preprocessing in the main program
  - dom_counts : AC of the dominant upper limb
  - non_dom_counts : AC of the non dominant upper limb

Code complet : Folder containing the current scripts
  -> agcounts_filter.py : preprocessing file to transform raw data into counted data (transformation into activity count)
  -> main.py : the main program, which successively uses the cutting of files (segment_file.py), the transformation into agcounts (agcounts_filter.py), then the calculation of metrics for each day (metrics_calculation.py) and finally the statistical analysis (statistics.py).
  -> metrics_calculation.py : processing file to calculate the metrics (mean and standard deviation)
  -> segment_file.py : preprocessing file to split a multi-day record file into multiple 1-day files.
  -> statistics.py : programme of statistical analysis to determine whether or not the significant difference between the two stages.
  -> UL_quantification.ipynb : Files containing processing agcounts (code in agcounts_filter.py) calculation and display of metrics (code in metrcis_calculation.py)

Fichiers tests : folder containing the test files that were used to write the current scripts

