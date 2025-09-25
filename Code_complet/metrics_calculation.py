"""This file contains the calculation of different metrics based on dominant and non-dominant arm activity counts.
Six time metrics : 
    - Dominant Active Duration
    - Non Dominant Active Duration
    - Bilateral Active Duration
    - Unilateral Dominant Active Duration
    - Unilateral Non Dominant Active Duration
    - Time Use Ratio
Five intensity metrics :
    - Mean Activity Counts
    - Bilateral Magnitude
    - Magnitude Ratio
    - MAUI (Mono Arm Use Index)
    - BAUI (Bilateral Arm Use Index)
    - Intensity Use Ratio
Called in main.py
"""

import numpy as np 
from movement_detection import active_duration_calculation

def sec_metrics(dom_AC, non_dom_AC):
    """ Calculate metrics (magnitude_ratio and bilateral_magnitude) per second from dominant and non-dominant arm activity counts.
    :param dom_AC (list) : dominant arm activity counts.
    :param non_dom_AC (list) : non dominant arm activity counts.
    :return magnitude_ratio (list) : magnitude ratio per second.
    :return bilateral_magnitude (list) : bilateral magnitude per second."""


    """*************************************************************************** SEC/SEC metrics ********************************************************************************************"""
    # Array to contain the metrics per seconds
    magnitude_ratio = []
    bilateral_magnitude = []

    for idx_sec in range(len(dom_AC)):

        # Magnitude Ratio 
        # *******Bailey RR 2014 calculation: +1 for each AC to avoid dividing by 0**********
        # if (non_dom_AC[idx_sec] != 0) & (dom_AC[idx_sec] != 0) :
        magnitude_ratio.append(np.log((non_dom_AC[idx_sec] + 1) / (dom_AC[idx_sec] + 1)))

        # Bilateral magnitude 
        bilateral_magnitude.append(non_dom_AC[idx_sec] + dom_AC[idx_sec])
    
    return magnitude_ratio, bilateral_magnitude


def maui_baui(dom_AC, non_dom_AC):
    """This function calculates the MAUI and BAUI metrics based on the dominant and non-dominant arm activity counts.
    :param dom_AC (list) : dominant arm activity counts.
    :param non_dom_AC (list) : non dominant arm activity counts.
    :return maui (float) : MAUI (Mono Arm Use Index).
    :return baui (float) : BAUI (Bilateral Arm Use Index).
    """

    """*************************************************************************** MAUI / BAUI ********************************************************************************************"""
    # Initializations
    dom_MAUI = []
    non_dom_MAUI = []
    dom_BAUI = []
    non_dom_BAUI = []

    for idx_sec in range(len(dom_AC)):
        # MAUI
        # Dominant mouvement intensities when non dominant arm is not moving
        if (non_dom_AC[idx_sec] == 0) & (dom_AC[idx_sec] != 0) :
            dom_MAUI.append(dom_AC[idx_sec])
        # Non dominant mouvement intensities when dominant arm is not moving
        elif (non_dom_AC[idx_sec] != 0) & (dom_AC[idx_sec] == 0) :
            non_dom_MAUI.append(non_dom_AC[idx_sec])

        # BAUI
        # Dominant and non dominant mouvement intensities when the other UL is also moving
        if (non_dom_AC[idx_sec] != 0) & (dom_AC[idx_sec] != 0) :
            dom_BAUI.append(dom_AC[idx_sec])
            non_dom_BAUI.append(non_dom_AC[idx_sec])

    # MAUI = sum(non dominant mvt when dominant UL is not moving) / sum(dominant mvt when non dominant UL is not moving)
    if dom_MAUI == []:
        maui = 404
    else:
        maui = np.sum(non_dom_MAUI) / np.sum(dom_MAUI)

    # BAUI = sum(non dominant mvt when dominant UL is also moving) / sum(dominant mvt when non dominant UL is also moving)
    if dom_BAUI == []:
        baui = 404 
    else:
        baui = np.sum(non_dom_BAUI) / np.sum(dom_BAUI)

    return maui, baui

    
def mean_metrics(dom_AC, non_dom_AC, magnitude_ratio, bilateral_magnitude, threshold_method, gyro_dom, gyro_non_dom):
    """ This function calculates the mean metrics based on the dominant and non-dominant arm activity counts, and the metrics per seconds. 
    :param dom_AC (lst) : dominant arm activity counts.
    :param non_dom_AC (lst) : non dominant arm activity counts.
    :param magnitude_ratio (lst) : magnitude ratio per seconde.
    :param bilateral magnitude (lst) : bilateral magnitude per seconde.
    :param threshold_method (str) : selected threshold method to detect a movement
    :param gyro_dom (dict) : dict of gyroscope data for the X, Y, and Z axes
    :param gyro_dom (dict) : dict of gyroscope data for the X, Y, and Z axes 
    :return dom_AD (float) : dominant active duration.
    :return non_dom_AD (float) : non dominant active duration.
    :return bimanual_AD (float) : bimanual active duration.
    :return unimanual_dom_AD (float) : unimanual active duration for the dominant UL.
    :return unimanual_non_dom_AD (float) : unimanual active duration for the non dominant UL.
    :return use_ratio_time (float) : use ratio time.
    :return use_ratio_intensity (float) : use ratio intensity.
    :return dom_mean_AC (float) : dominant mean activity counts per second.
    :return non_dom_mean_AC (float) : non dominant mean activity counts per second.
    :return mean_bilateral_magnitude (float) : mean bilateral magnitude.
    :return mean_magnitude_ratio (float) : mean magnitude ratio.
    """
    # Active duration and bimanual active duration
    dom_AD, non_dom_AD, bimanual_AD, unimanual_dom_AD, unimanual_non_dom_AD = active_duration_calculation(threshold_method, dom_AC, non_dom_AC, gyro_dom, gyro_non_dom)

    if dom_AD != 0:
        use_ratio_time = non_dom_AD / dom_AD
    else :
        use_ratio_time = 0

    # Mean AC 
    dom_mean_AC = np.mean(dom_AC)
    non_dom_mean_AC = np.mean(non_dom_AC) 

    # Use ratio with Mean AC
    if dom_mean_AC != 0 :
        use_ratio_intensity = non_dom_mean_AC / dom_mean_AC
    else :
        use_ratio_intensity = 0

    # Mean Bilateral Magnitude
    mean_bilateral_magnitude = np.mean(bilateral_magnitude)

    # Mean Magnitude Ratio 
    mean_magnitude_ratio = np.mean(magnitude_ratio)

    return dom_AD, non_dom_AD, bimanual_AD, unimanual_dom_AD, unimanual_non_dom_AD, use_ratio_time, use_ratio_intensity, dom_mean_AC, non_dom_mean_AC, mean_bilateral_magnitude, mean_magnitude_ratio


def metrics(dom_AC, non_dom_AC, threshold_method, gyro_dom, gyro_non_dom):
    """ This function calculates various metrics based on the dominant and non-dominant arm activity counts.
    :param dom_AC (list) : dominant arm activity counts.
    :param non_dom_AC (list) : non dominant arm activity counts.
    :param threshold_method (str) : selected threshold method to detect a movement
    :param gyro_dom (dict) : dict of gyroscope data for the X, Y, and Z axes
    :param gyro_non_dom (dict) : dict of gyroscope data for the X, Y, and Z axes
    :return df_metrics (dict) : dict containing the metrics.
    """
    magnitude_ratio, bilateral_magnitude = sec_metrics(dom_AC, non_dom_AC)
    maui, baui = maui_baui(dom_AC, non_dom_AC)
    dom_AD, non_dom_AD, bimanual_AD, unimanual_dom_AD, unimanual_non_dom_AD, use_ratio_time, use_ratio_intensity, dom_mean_AC, non_dom_mean_AC, mean_bilateral_magnitude, mean_magnitude_ratio = mean_metrics(dom_AC, non_dom_AC, magnitude_ratio, bilateral_magnitude, threshold_method, gyro_dom, gyro_non_dom)

    df_metrics = {
        "dom_AD": dom_AD,
        "non_dom_AD": non_dom_AD,
        "bimanual_AD" : bimanual_AD,
        "unimanual_dom_AD" : unimanual_dom_AD,
        "unimanual_non_dom_AD" : unimanual_non_dom_AD,
        "use_ratio_time": use_ratio_time,
        "use_ratio_intensity": use_ratio_intensity,
        "dom_mean_AC": dom_mean_AC,
        "non_dom_mean_AC": non_dom_mean_AC,
        "mean_bilateral_magnitude": mean_bilateral_magnitude,
        "mean_magnitude_ratio": mean_magnitude_ratio,
        "maui": maui,
        "baui": baui
    }
    return df_metrics 