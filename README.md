## Actinalyseur

### Pré requis
- 3.8 < python < 3.12
- openpyxl==3.1.2
- pandas==2.2.2
- numpy==1.24.4
- customtkinter==5.2.0
- agcounts== 0.2.6 

### Guide d'installation
Téléchargez le dossier "Code_complet" puis exécutez la commande suivante dans le terminal de l'ordinateur, à l'endroit où se trouve le dossier téléchargé : "pyinstaller main.spec". Le fichier exécutable se télécharge dans le dossier "dist" (dossier Code_complet), puis peut être directement utilisé en double-cliquant sur l'icône.

### Structure des dossiers
Code complet : dossier contenant les scripts actuels
  - agcounts_filter.py : fichier de traitement permettant de transformer les données brutes en activity count (transformation en activity count). Détails : https://github.com/actigraph/agcounts.git
      - get_counts_csv() : récupération des données brutes dans les fichiers d'entrées.
      - convert_counts_csv() : conversion des données brutes en activity counts.
      - convert_AC() : méthode principale appelant gets_counts_csv() et convert_counts_csv().
        
  - interface.py : interface de l'application Actinalyseur, permettant aux utilisateurs de sélectionner un dossier et de lancer des calculs, d'afficher une barre de progression et d'être avertis lorsque les résultats sont disponibles.
      - choose_folder(window) : ouverture de la boîte de dialogue pour sélectionner un dossier et mettre à jour l'étiquette avec le chemin d'accès au dossier sélectionné. :param window :  ctk.CTK Fenêtre principale de l'application. :return : chemin d'accès au dossier sélectionné.
      - start_calculation(window): gestion de l'action lorsque l'utilisateur clique sur le bouton « Calcul des métriques ». :param window :  ctk.CTK Fenêtre principale de l'application.
      - create_window() : création la fenêtre principale de l'application avec une interface de sélection de dossiers. :return: chemin d'accès au dossier sélectionné.
      - update_progress(idx_interface,progress_bar, progress_interface, message, message_label, progress_title) : mise à jour de la barre de progression. :param idx_interface : entier représentant l'index actuel de la barre de progression. :param progress_bar :  ctk.CTkProgressBar Widget de la barre de progression. :param progress_interface : ctk.CTK fenêtre d'interface principale. :param message : str message à afficher dans la fenêtre d'interface. :param message_label : ctk.CTkLabel widget d'étiquette pour afficher le message.
      - create_progress_interface(progress_dict) : création d'une interface de barre de progression CustomTkinter. :param progress_dict : dictionnaire pour stocker les références à la barre de progression et à l'interface.
  
  - main.py : code principal, appelant successivement les fichiers de l'interface (interface.py), de sélection des heures (segment_file.py), de transformation des données brutes en activity counts (agcounts_filter.py), de calculs des métriques (metrics_calculation.py) et de sauvegarde des résultats dans les fichiers Excel de sortie (save_metrics_in_excel.py).
  
  - metrics_calculation.py : fichier de calcul des métriques.
      - sec_metrics(dom_AC, non_dom_AC) : calcul des mesures (magnitude_ratio et bilateral_magnitude) par seconde à partir du nombre d'activités du bras dominant et non-dominant. :param dom_AC : liste du nombre d'activités du bras dominant. :param non_dom_AC : liste du nombre d'activités du bras non-dominant. :return magnitude_ratio : liste du rapport de magnitude par seconde. :return bilateral_magnitude : liste de la magnitude bilatérale par seconde.
      - maui_baui(dom_AC, non_dom_AC) : calcul des mesures MAUI et BAUI en fonction du nombre d'activités effectuées par le bras dominant et le bras non-dominant. :param dom_AC : liste du nombre d'activités effectuées par le bras dominant. :param non_dom_AC : liste du nombre d'activités effectuées par le bras non-dominant. :return maui : float de MAUI (indice d'utilisation du bras unique). :return baui : float de BAUI (indice d'utilisation des deux bras).
      - mean_metrics(dom_AC, non_dom_AC, magnitude_ratio, bilateral_magnitude) : calcul des métriques moyennes basées sur les activity counts des bras dominant et non-dominant, et les mesures par seconde. :param dom_AC : liste du nombre d'activités du bras dominant. :param non_dom_AC : liste du nombre d'activités du bras non-dominant. :param magnitude_ratio : liste des ratios de magnitude par seconde. :param bilateral magnitude : liste des magnitudes bilatérales par seconde. :return dom_AD : nombre flottant représentant la durée d'activité dominante. :return non_dom_AD : nombre flottant représentant la durée d'activité non-dominante. :return bimanual_AD : nombre flottant représentant la durée d'activité bi-manuelle. :return use_ratio_time : nombre flottant représentant le temps d'utilisation. :return use_ratio_intensity : nombre flottant représentant l'intensité du ratio d'utilisation. :return dom_mean_AC : nombre flottant représentant le nombre moyen d'activités dominantes par seconde. :return non_dom_mean_AC : nombre flottant représentant le nombre moyen d'activités non-dominantes par seconde. :return mean_bilateral_magnitude : nombre flottant représentant l'amplitude bilatérale moyenne. :return mean_magnitude_ratio : nombre flottant représentant le ratio d'amplitude moyen.
      - metrics(dom_AC, non_dom_AC) : calcul de divers indicateurs basés sur les activity counts des bras dominant et non-dominant. :param dom_AC : liste du nombre d'activités du bras dominant. :param non_dom_AC : liste du nombre d'activités du bras non-dominant. :return df_metrics : dictionnaire contenant les indicateurs.
  
  - save_metrics_in_excel.py : fichier enregistrant les résultats des métriques dans les fichiers Excel de sortie.
      - select_output_file(file_path, ID, therapy_name) : sélection du fichier de sortie dans lequel écrire les métriques. Si le fichier existe, il charge les données existantes. Si le fichier n'existe pas, il crée un nouveau fichier et initialise la première colonne avec les noms des métriques, puis enregistre les informations sur l'enfant. :param file_path : chemin d'accès au fichier de sortie. :param ID : str de l(ID de l'enfant. :param therapy_name : str du nom de la thérapie (« HABIT » ou « PARTNER »). :return my_wb : workbook pour le fichier de sortie. :return my_sheet : feuille active du classeur.
      - write_in_file(my_wb, file_path, record_time, idx_day, day, lst_time_metrics, lst_intensity_metrics) : écriture des métriques dans un fichier Excel. Il crée une nouvelle colonne pour chaque enfant et la remplit avec les métriques correspondantes. :param my_wb : fichier Excel dans lequel enregistrer les données.  :param file_path : chemin d'accès au fichier de sortie. :param record_time : entier représentant le nombre de minutes enregistrées pour 1 jour.  :param idx_day : entier représentant l'index du jour (Ex : 1 pour le jour 1). :param day : date et heure du jour. :param lst_time_metrics : liste des métriques de temps à écrire dans le fichier. :param lst_intensity_metrics : liste des métriques d'intensité à écrire dans le fichier. :return : enregistre les métriques de lst_time_metrics et lst_intensity_metrics dans le fichier Excel correspondant à my_wb.
  
  - segment_file.py : fichier permettant de diviser un fichier d'enregistrement couvrant plusieurs jours en plusieurs fichiers d'un jour, selon les dates spécifiées en entrée d'algorithme.
      - segment_time(modality, therapy, info_sheet) : segmentation d'un fichier, en fonction de la modalité thérapeutique et des heures d'activité. Si l'enregistrement est effectué au centre, le fichier est segmenté de 8h à 20h. Si l'enregistrement est effectué à domicile, le fichier est segmenté en fonction des heures d'activité (annotations des parents). :param modality : str correspondant au type de modalité (« Vie_quotidienne » ou « Stage »). :param therapy : str correspondant au nom de la thérapie (« HABIT » ou « PARTNER »). :param info_sheet : feuille du classeur contenant l'heure de début et de fin des enregistrements. :return comp_vie_quot : dictionnaire avec la date comme clé et l'heure de début et de fin de l'activité comme valeur. :return comp_1h30 : dictionnaire avec la date comme clé et l'heure de début et de fin de l'activité comme valeur. :return comp_5h : dictionnaire avec la date comme clé et l'heure de début et de fin de l'activité comme valeur.
  
  - Activity counts files : dossier contenant les fichiers de sauvegarde des activity counts après traitement des données brutes dans le programme principal.
      - dom_counts : AC du membre dominant
      - non_dom_counts : AC du membre atteint
  
Fichiers_tests : dossier contenant les fichiers de test qui ont été utilisés pour écrire les scripts actuels.

Ex_arborescence : dossier contenant des exemples de fichiers d'entrée. Utilisés pour tester le fonctionnement des scripts actuels.

## Entrée 
Doit se trouver au minimum dans le dossier d’entrée :
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

