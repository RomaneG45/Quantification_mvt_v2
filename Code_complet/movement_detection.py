"""This file classify each second as a "movement" or a "non movement" depending on the selected method defined by the user. It then calculates dominant and non dominant active durations."""

import numpy as np
from joblib import load
from scipy.signal import medfilt
from scipy.ndimage import maximum_filter1d

def active_duration_calculation(selected_method, dom_AC, non_dom_AC, gyro_dom, gyro_non_dom):
    """
    This function proposes 3 methods to detect movement periods.
    :param selected_method (str) : method selected by the user in the interface, to detect movements
    :param dom_AC (lst) : list of dominant activity counts
    :param non_dom_AC (lst) : list of non dominant activity counts
    :param gyro_dom : dict of gyroscope data for the X, Y, and Z axes
    :param gyro_non_dom : dict of gyroscope data for the X, Y, and Z axes
    :return dom_AD (float) : Dominant active duration
    :return non_dom_AD (float) : Non dominant active duration
    """
    dom_AD = 0
    non_dom_AD = 0

    if selected_method == "AC > 0":
        dom_AD, non_dom_AD, bimanual_AD = zero_theshold(dom_AC, non_dom_AC)
    
    elif selected_method == "Random Forest":
        dom_AD, non_dom_AD, bimanual_AD = RF_theshold(dom_AC, non_dom_AC)

    elif selected_method == "Coley":
        dom_AD, non_dom_AD, bimanual_AD = coley_theshold(dom_AC, non_dom_AC, gyro_dom, gyro_non_dom)

    return dom_AD, non_dom_AD, bimanual_AD


def zero_theshold(dom_AC, non_dom_AC):
    """
    This functin calculates active duration by detecting an activity for an AC > 0.
    :param dom_AC (lst) : list of dominant activity counts
    :param non_dom_AC (lst) : list of non dominant activity counts
    :return dom_AD (float) : Dominant active duration
    :return non_dom_AD (float) : Non dominant active duration
    :return bimanual_AD (float) : Bimanual active duration
    """
    # Active duration
    dom_AC_array = np.array(dom_AC)
    non_dom_AC_array = np.array(non_dom_AC)
    dom_AD = np.sum(dom_AC_array > 0) * 100 / len(dom_AC_array) 
    non_dom_AD = np.sum(non_dom_AC_array > 0) * 100 / len(non_dom_AC_array) 

    # Bimanual active duration
    sum_bimanual_AD = 0
    for idx_sec in range(0, len(dom_AC)):
        if dom_AC[idx_sec] > 0 and non_dom_AC[idx_sec] > 0:
            sum_bimanual_AD += 1
    bimanual_AD = sum_bimanual_AD *100 / len(dom_AC)


    return dom_AD, non_dom_AD, bimanual_AD


def RF_theshold(dom_AC, non_dom_AC):
    """
    This functin calculates active duration by detecting an activity thanks to a pretrained Random Forest Classifier.
    :param dom_AC (lst) : list of dominant activity counts
    :param non_dom_AC (lst) : list of non dominant activity counts
    :return dom_AD (float) : Dominant active duration
    :return non_dom_AD (float) : Non dominant active duration
    :return bimanual_AD (float) : Bimanual active duration
    """
    dom_AD = 0
    non_dom_AD = 0
    # Reshape dom_AC and non_dom_AC for random forest
    reshaped_dom_AC = np.vstack(np.array(dom_AC))
    reshaped_non_dom_AC = np.vstack(np.array(non_dom_AC))
    
    # Active duration
    RF_model_dom = load('Random_Forest_dom.joblib')
    RF_model_non_dom = load('Random_Forest_non_dom.joblib')
    # Movement predictions
    dom_mov_pred = RF_model_dom.predict(reshaped_dom_AC)
    non_dom_mov_pred = RF_model_non_dom.predict(reshaped_non_dom_AC)
    # Calculating active duration
    dom_AD = np.sum(dom_mov_pred == "mouvement") * 100 / len(dom_AC) 
    non_dom_AD = np.sum(non_dom_mov_pred == "mouvement") * 100 / len(non_dom_AC) 

    # Bimanual active duration
    sum_bimanual_AD = 0
    for idx_sec in range(0, min(len(dom_mov_pred), len(non_dom_mov_pred))):
        if dom_mov_pred[idx_sec] == "mouvement" and non_dom_mov_pred[idx_sec] == "mouvement" :
            sum_bimanual_AD += 1
    bimanual_AD = sum_bimanual_AD *100 / len(dom_AC)

    return dom_AD, non_dom_AD, bimanual_AD

def coley_theshold(dom_AC, non_dom_AC, gyro_dom, gyro_non_dom):
    """
    This functin calculates active duration by detecting an activity with Coley algorithm (cf mindmaze protocol).
    :param dom_AC (lst) : list of dominant activity counts
    :param non_dom_AC (lst) : list of non dominant activity counts
    :return dom_AD (float) : Dominant active duration
    :return non_dom_AD (float) : Non dominant active duration 
    :return bimanual_AD (float) : Bimanual active duration
    """
    dom_AD = 0
    non_dom_AD = 0
    members_gyro = [gyro_dom, gyro_non_dom]
    mvt_pred = []
    # coley
    for gyro in members_gyro : 
        #-------------------------- Paramètres --------------------------
        sampling_rate =  30
        merge_window = int(1 * sampling_rate)  # 1 seconde
        gap_threshold = int(0.5 * sampling_rate)  # 0.5 seconde
        min_duration = int(1.5 * sampling_rate)  # 1.5 seconde

        #-------------------------- Extraire les 3 axes gyroscopiques --------------------------
        gyro_x = gyro["X"]
        gyro_y = gyro["Y"]
        gyro_z = gyro["Z"]

        #-------------------------- Détection des pics > 10°/s sur chaque axe --------------------------
        mask_x = np.abs(np.array(gyro_x)) > 10
        mask_y = np.abs(np.array(gyro_y)) > 10
        mask_z = np.abs(np.array(gyro_z)) > 10

        detected_x = np.abs(np.array(gyro_x)[mask_x])
        detected_y = np.abs(np.array(gyro_y)[mask_y])
        detected_z = np.abs(np.array(gyro_z)[mask_z])

        #-------------------------- Moyenne des pics par axe --------------------------
            
        mean_x = detected_x.mean() if len(detected_x) > 0 else np.inf
        mean_y = detected_y.mean() if len(detected_y) > 0 else np.inf
        mean_z = detected_z.mean() if len(detected_z) > 0 else np.inf

        #-------------------------- Seuil adaptatif = min des moyennes --------------------------
        adaptive_threshold = min(mean_x, mean_y, mean_z)
        print(f"Seuil adaptatif : {adaptive_threshold:.2f} °/s")

        #-------------------------- Détection brute : un mouvement si un axe dépasse le seuil --------------------------
        
        movement_raw = (
            (np.abs(gyro_x) > adaptive_threshold) |
            (np.abs(gyro_y) > adaptive_threshold) |
            (np.abs(gyro_z) > adaptive_threshold)
        ).astype(int)


        #-------------------------- Filtre max mobile (fusionner les mouvements séparés de < 0.5s) --------------------------
        movement_merged = maximum_filter1d(movement_raw, size = merge_window)

        #-------------------------- Filtre médian mobile (supprimer les mouvements < 1.5s) --------------------------
        movement_prediction = medfilt(movement_merged, kernel_size = min_duration | 1)  # kernel must be odd

        mvt_pred.append(movement_prediction)

    # Resample
    def downsample_to_1Hz(binary_array, sampling_rate=30):
        n_seconds = len(binary_array) // sampling_rate
        binary_array = binary_array[:n_seconds * sampling_rate]  # tronquer pour être multiple de 128
        reshaped = binary_array.reshape(n_seconds, sampling_rate) # Majorité : si au moins 64 échantillons sont actifs, on considère la seconde comme mouvement
        return (reshaped.sum(axis=1) >= (sampling_rate // 2)).astype(int)

    predicted_1Hz_dom = downsample_to_1Hz(mvt_pred[0])
    predicted_1Hz_non_dom = downsample_to_1Hz(mvt_pred[1])

    #dom_AD
    dom_AD = np.sum(predicted_1Hz_dom > 0) * 100 / len(predicted_1Hz_dom) 
    non_dom_AD = np.sum(predicted_1Hz_non_dom > 0) * 100 / len(predicted_1Hz_non_dom) 

    # Bimanual active duration
    sum_bimanual_AD = 0
    for idx_sec in range(0, min(len(predicted_1Hz_non_dom), len(predicted_1Hz_dom))):
        if predicted_1Hz_dom[idx_sec] == 1 and predicted_1Hz_non_dom[idx_sec] == 1 :
            sum_bimanual_AD += 1
    bimanual_AD = sum_bimanual_AD *100 / (len(gyro_dom['X'] ) / 30)

    return dom_AD, non_dom_AD, bimanual_AD