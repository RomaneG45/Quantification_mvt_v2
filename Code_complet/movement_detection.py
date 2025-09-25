"""This file classify each second as a "movement" or a "non movement" depending on the selected method defined by the user. It then calculates dominant, non dominant, bilateral and unimanual active durations.
Called in metrics_calculation.py"""

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
    :param gyro_dom (dict) : dict of gyroscope data for the X, Y, and Z axes 
    :param gyro_non_dom (dict) : dict of gyroscope data for the X, Y, and Z axes 
    :return dom_AD (float) : Dominant active duration
    :return non_dom_AD (float) : Non dominant active duration
    :return bimanual_AD (float) : bimanual active duration 
    :return unimanual_dom_AD (float) : unimanual active duration for the dominant membre 
    :return unimanual_non_dom_AD (float) : unimanual active duration for the non dominant membre  
    """
    dom_AD = 0
    non_dom_AD = 0

    if selected_method == "AC > 0":
        dom_AD, non_dom_AD, bimanual_AD, unimanual_dom_AD, unimanual_non_dom_AD = zero_theshold(dom_AC, non_dom_AC)
    
    elif selected_method == "Random Forest":
        dom_AD, non_dom_AD, bimanual_AD, unimanual_dom_AD, unimanual_non_dom_AD = RF_theshold(dom_AC, non_dom_AC)

    elif selected_method == "Coley":
        dom_AD, non_dom_AD, bimanual_AD, unimanual_dom_AD, unimanual_non_dom_AD = coley_theshold(gyro_dom, gyro_non_dom)

    return dom_AD, non_dom_AD, bimanual_AD, unimanual_dom_AD, unimanual_non_dom_AD


def zero_theshold(dom_AC, non_dom_AC):
    """
    This functin calculates active duration by detecting an activity for an AC > 0.
    :param dom_AC (lst) : list of dominant activity counts
    :param non_dom_AC (lst) : list of non dominant activity counts
    :return dom_AD (float) : Dominant active duration
    :return non_dom_AD (float) : Non dominant active duration
    :return bimanual_AD (float) : Bimanual active duration
    :return unimanual_dom_AD (float) : unimanual active duration for the dominant membre 
    :return unimanual_non_dom_AD (float) : unimanual active duration for the non dominant membre 
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
    if len(dom_AC) != 0 :
        bimanual_AD = sum_bimanual_AD *100 / len(dom_AC)

    # Unimanual AD
    sum_unimanual_dom_AD = 0
    sum_unimanual_non_dom_AD = 0
    for idx_sec in range(0, len(dom_AC)):
        if dom_AC[idx_sec] > 0 and non_dom_AC[idx_sec] == 0:
            sum_unimanual_dom_AD += 1
        elif dom_AC[idx_sec] == 0 and non_dom_AC[idx_sec] > 0:
            sum_unimanual_non_dom_AD += 1
    
    if len(dom_AC) != 0 :
        unimanual_dom_AD = sum_unimanual_dom_AD *100 / len(dom_AC)
    if len(non_dom_AC) != 0 :
        unimanual_non_dom_AD = sum_unimanual_non_dom_AD *100 / len(non_dom_AC)

    
    print("len dom AC dans movement_detection: ", len(dom_AC))

    return dom_AD, non_dom_AD, bimanual_AD, unimanual_dom_AD, unimanual_non_dom_AD


def RF_theshold(dom_AC, non_dom_AC):
    """
    This functin calculates active duration by detecting an activity thanks to a pretrained Random Forest Classifier.
    :param dom_AC (lst) : list of dominant activity counts
    :param non_dom_AC (lst) : list of non dominant activity counts
    :return dom_AD (float) : Dominant active duration
    :return non_dom_AD (float) : Non dominant active duration
    :return bimanual_AD (float) : Bimanual active duration
    :return unimanual_dom_AD (float) : unimanual active duration for the dominant membre 
    :return unimanual_non_dom_AD (float) : unimanual active duration for the non dominant membre 
    """
    dom_AD = 0
    non_dom_AD = 0
    # Reshape dom_AC and non_dom_AC for random forest
    reshaped_dom_AC = np.vstack(np.array(dom_AC))
    reshaped_non_dom_AC = np.vstack(np.array(non_dom_AC))
    
    # Active duration
    RF_model_dom = load('RF_dom.joblib') # the model can be changed
    RF_model_non_dom = load('RF_non_dom.joblib') # the model can be changed
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
    if len(dom_AC) != 0 :
        bimanual_AD = sum_bimanual_AD *100 / len(dom_AC)

     # Unimanual AD
    sum_unimanual_dom_AD = 0
    sum_unimanual_non_dom_AD = 0
    for idx_sec in range(0, len(dom_AC)):
        if dom_mov_pred[idx_sec] == "mouvement" and non_dom_mov_pred[idx_sec] != "mouvement" :
            sum_unimanual_dom_AD += 1
        if dom_mov_pred[idx_sec] != "mouvement" and non_dom_mov_pred[idx_sec] == "mouvement" :
            sum_unimanual_non_dom_AD += 1
    
    if len(dom_AC) != 0 :
        unimanual_dom_AD = sum_unimanual_dom_AD *100 / len(dom_AC)
    if len(non_dom_AC) != 0 : 
        unimanual_non_dom_AD = sum_unimanual_non_dom_AD *100 / len(non_dom_AC)

    print("len dom AC dans movement_detection: ", len(dom_AC))

    return dom_AD, non_dom_AD, bimanual_AD, unimanual_dom_AD, unimanual_non_dom_AD


def coley_theshold(gyro_dom, gyro_non_dom):
    """
    This function calculates active duration by detecting an activity with Coley algorithm (cf mindmaze protocol).
    :param gyro_dom (dict) : dict gyroscope data for the X, Y, and Z axes
    :param gyro_non_dom : dict of gyroscope data for the X, Y, and Z axes
    :return dom_AD (float) : Dominant active duration
    :return non_dom_AD (float) : Non dominant active duration 
    :return bimanual_AD (float) : Bimanual active duration
    :return unimanual_dom_AD (float) : unimanual active duration for the dominant membre 
    :return unimanual_non_dom_AD (float) : unimanual active duration for the non dominant membre 
    """
    dom_AD = 0
    non_dom_AD = 0
    members_gyro = [gyro_dom, gyro_non_dom]
    mvt_pred = []
    # Coley
    for gyro in members_gyro : 
        #-------------------------- Parameters --------------------------
        sampling_rate =  30
        merge_window = int(1 * sampling_rate)  # 1 second
        gap_threshold = int(0.5 * sampling_rate)  # 0.5 second
        min_duration = int(1.5 * sampling_rate)  # 1.5 second

        #-------------------------- Extraction of the 3 gyroscopic axes --------------------------
        # Replace , by . in the number values and transform str into int
        gyro_x = np.array([s.replace(',', '.') for s in gyro["X"]], dtype=float)
        gyro_y = np.array([s.replace(',', '.') for s in gyro["Y"]], dtype=float)
        gyro_z = np.array([s.replace(',', '.') for s in gyro["Z"]], dtype=float)

        #-------------------------- Detection of peaks > 10°/s on each axis --------------------------
        mask_x = np.abs(np.array(gyro_x)) > 10
        mask_y = np.abs(np.array(gyro_y)) > 10
        mask_z = np.abs(np.array(gyro_z)) > 10

        detected_x = np.abs(np.array(gyro_x)[mask_x])
        detected_y = np.abs(np.array(gyro_y)[mask_y])
        detected_z = np.abs(np.array(gyro_z)[mask_z])

        #-------------------------- Mean of peaks per axis --------------------------
            
        mean_x = detected_x.mean() if len(detected_x) > 0 else np.inf
        mean_y = detected_y.mean() if len(detected_y) > 0 else np.inf
        mean_z = detected_z.mean() if len(detected_z) > 0 else np.inf

        #-------------------------- Adaptative threshold = minimum of the means --------------------------
        adaptive_threshold = min(mean_x, mean_y, mean_z)
        print(f"Seuil adaptatif : {adaptive_threshold:.2f} °/s")

        #-------------------------- Raw detection: movement if an axis exceeds the threshold --------------------------
        
        movement_raw = (
            (np.abs(gyro_x) > adaptive_threshold) |
            (np.abs(gyro_y) > adaptive_threshold) |
            (np.abs(gyro_z) > adaptive_threshold)
        ).astype(int)


        #-------------------------- Maximum moving filter (merge separate movements of < 0.5s) --------------------------
        movement_merged = maximum_filter1d(movement_raw, size = merge_window)

        #-------------------------- Moving median filter (remove movements < 1.5s) --------------------------
        movement_prediction = medfilt(movement_merged, kernel_size = min_duration | 1)  # kernel must be odd

        mvt_pred.append(movement_prediction)

    # Resample
    def downsample_to_1Hz(binary_array, sampling_rate=30):
        n_seconds = len(binary_array) // sampling_rate
        binary_array = binary_array[:n_seconds * sampling_rate]  # Truncate to be a multiple of 30
        reshaped = binary_array.reshape(n_seconds, sampling_rate) # Majority: if at least 15 samples are active, the second is considered a movement.
        return (reshaped.sum(axis=1) >= (sampling_rate // 2)).astype(int)

    predicted_1Hz_dom = downsample_to_1Hz(mvt_pred[0])
    predicted_1Hz_non_dom = downsample_to_1Hz(mvt_pred[1])

    # dom_AD
    dom_AD = np.sum(predicted_1Hz_dom > 0) * 100 / len(predicted_1Hz_dom) 
    non_dom_AD = np.sum(predicted_1Hz_non_dom > 0) * 100 / len(predicted_1Hz_non_dom) 

    # Bimanual active duration
    sum_bimanual_AD = 0
    for idx_sec in range(0, min(len(predicted_1Hz_non_dom), len(predicted_1Hz_dom))):
        if predicted_1Hz_dom[idx_sec] == 1 and predicted_1Hz_non_dom[idx_sec] == 1 :
            sum_bimanual_AD += 1

    if len(predicted_1Hz_non_dom) != 0 :
        bimanual_AD = sum_bimanual_AD *100 / len(predicted_1Hz_non_dom) 

     # Unimanual AD
    sum_unimanual_dom_AD = 0
    sum_unimanual_non_dom_AD = 0
    for idx_sec in range(0, min(len(predicted_1Hz_non_dom), len(predicted_1Hz_dom))):
        if predicted_1Hz_dom[idx_sec] == 1 and predicted_1Hz_non_dom[idx_sec] != 1 :
            sum_unimanual_dom_AD += 1
        if predicted_1Hz_dom[idx_sec] != 1 and predicted_1Hz_non_dom[idx_sec] == 1  :
            sum_unimanual_non_dom_AD += 1

    if len(predicted_1Hz_dom) != 0 :
        unimanual_dom_AD = sum_unimanual_dom_AD *100 / len(predicted_1Hz_dom)
    if len(predicted_1Hz_non_dom) != 0 :
        unimanual_non_dom_AD = sum_unimanual_non_dom_AD *100 / len(predicted_1Hz_non_dom)

    print("len predicted_1Hz_dom: ", len(predicted_1Hz_dom))

    return dom_AD, non_dom_AD, bimanual_AD, unimanual_dom_AD, unimanual_non_dom_AD