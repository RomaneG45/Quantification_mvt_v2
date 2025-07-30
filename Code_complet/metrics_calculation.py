"""This file contains the calculation of different metrics based on dominant and non-dominant arm activity counts.
Two time metrics : 
    - Active Duration
    - Use Ratio
Five intensity metrics :
    - Mean Activity Counts
    - Bilateral Magnitude
    - Magnitude Ratio
    - MAUI (Mono Arm Use Index)
    - BAUI (Bilateral Arm Use Index)
"""

import numpy as np 

def sec_metrics(dom_AC, non_dom_AC):
    """ Calculate metrics (magnitude_ratio and bilateral_magnitude) per second from dominant and non-dominant arm activity counts.
    :param dom_AC : lsit of dominant arm activity counts
    :param non_dom_AC : list of non dominant arm activity counts
    :return magnitude_ratio : list of magnitude ratio per second
    :return bilateral_magnitude : list of bilateral magnitude per second"""


    """*************************************************************************** SEC/SEC metrics ********************************************************************************************"""
    #Array to contain the metrics per seconds
    magnitude_ratio = []
    bilateral_magnitude = []

    for idx_sec in range(len(dom_AC)):

        #Magnitude Ratio 
        #*******Bailey RR 2014 calculation: +1 for each AC to avoid dividing by 0**********
        #if (non_dom_AC[idx_sec] != 0) & (dom_AC[idx_sec] != 0) :
        magnitude_ratio.append(np.log((non_dom_AC[idx_sec] + 1) / (dom_AC[idx_sec] + 1)))

        #Bilateral magnitude 
        bilateral_magnitude.append(non_dom_AC[idx_sec] + dom_AC[idx_sec])
    
    return magnitude_ratio, bilateral_magnitude


def maui_baui(dom_AC, non_dom_AC):
    """This function calculates the MAUI and BAUI metrics based on the dominant and non-dominant arm activity counts.
    :param dom_AC : list of dominant arm activity counts
    :param non_dom_AC : list of non dominant arm activity counts
    :return maui : float of MAUI (Mono Arm Use Index)
    :return baui : float of BAUI (Bilateral Arm Use Index)
    """

    """*************************************************************************** MAUI / BAUI ********************************************************************************************"""
    #Initializations
    dom_MAUI = []
    non_dom_MAUI = []
    dom_BAUI = []
    non_dom_BAUI = []

    for idx_sec in range(len(dom_AC)):
        #MAUI
        #Dominant mouvement intensities when non dominant arm is not moving
        if (non_dom_AC[idx_sec] == 0) & (dom_AC[idx_sec] != 0) :
            dom_MAUI.append(dom_AC[idx_sec])
        #Non dominant mouvement intensities when dominant arm is not moving
        elif (non_dom_AC[idx_sec] != 0) & (dom_AC[idx_sec] == 0) :
            non_dom_MAUI.append(non_dom_AC[idx_sec])

        #BAUI
        #Dominant and non dominant mouvement intensities when the other UL is also moving
        if (non_dom_AC[idx_sec] != 0) & (dom_AC[idx_sec] != 0) :
            dom_BAUI.append(dom_AC[idx_sec])
            non_dom_BAUI.append(non_dom_AC[idx_sec])

    #MAUI = sum(non dominant mvt when dominant UL is not moving) / sum(dominant mvt when non dominant UL is not moving)
    if dom_MAUI == []:
        maui = 404
    else:
        maui = np.sum(non_dom_MAUI) / np.sum(dom_MAUI)

    #BAUI = sum(non dominant mvt when dominant UL is also moving) / sum(dominant mvt when non dominant UL is also moving)
    if dom_BAUI == []:
        baui = 404 
    else:
        baui = np.sum(non_dom_BAUI) / np.sum(dom_BAUI)

    return maui, baui

    
def mean_metrics(dom_AC, non_dom_AC, magnitude_ratio, bilateral_magnitude):
    """ This function calculates the mean metrics based on the dominant and non-dominant arm activity counts, and the metrics per seconds. 
    :param dom_AC : list of dominant arm activity counts
    :param non_dom_AC : list of non dominant arm activity counts
    :param magnitude_ratio : list of magnitude ratio per seconde
    :param bilateral magnitude : list of bilateral magnitude per seconde
    :return dom_AD : float of dominant active duration
    :return non_dom_AD : float of non dominant active duration
    return bimanual_AD : float of bimanual active duration
    :return use_ratio_time : float of use ratio time
    :return dom_mean_AC : float of dominant mean activity counts per second
    :return non_dom_mean_AC : float of non dominant mean activity counts per second
    :return mean_bilateral_magnitude : float of mean bilateral magnitude
    :return mean_magnitude_ratio : float of mean magnitude ratio
    """
    #Calculate Active Counts (AC) per 2 seconds epoch (to satisfy threshold of 75.0)
    two_sec_dom_AC = []
    two_sec_non_dom_AC = []

    for idx_sec in range(0, len(dom_AC) - 1, 2):
        two_sec_dom_AC.append(dom_AC[idx_sec] + dom_AC[idx_sec+1])
    two_sec_dom_AC = np.array(two_sec_dom_AC)
    for idx_sec in range(0, len(non_dom_AC) - 1, 2):
        two_sec_non_dom_AC.append(non_dom_AC[idx_sec] + non_dom_AC[idx_sec+1])
    two_sec_non_dom_AC = np.array(two_sec_non_dom_AC)

    #Active duration
    """if len(two_sec_dom_AC) == 0 :
        dom_AD = 404
    else:
        dom_AD = np.sum(two_sec_dom_AC > 75.0) *100 / len(two_sec_dom_AC) 
    if len(two_sec_non_dom_AC) == 0 :
        non_dom_AD = 404      
    else:
        non_dom_AD = np.sum(two_sec_non_dom_AC > 75.0) *100 / len(two_sec_non_dom_AC) """
    dom_AD = "Méthode non définie"
    non_dom_AD = "Méthode non définie"


    #Bimanual active duration
    """sum_bimanual_AD = 0
    for idx_sec in range(0, len(two_sec_dom_AC)):
        if two_sec_dom_AC[idx_sec] > 75 and two_sec_non_dom_AC[idx_sec] > 75:
            sum_bimanual_AD += 1
    bimanual_AD = sum_bimanual_AD *100 / len(two_sec_dom_AC)"""
    bimanual_AD = "Méthode non définie"


    use_ratio_time = "Méthode non définie"
    #Use ratio with Active Duration
    """if dom_AD == 0:
        use_ratio_time = 404
    else:
        use_ratio_time = non_dom_AD / dom_AD"""

    #Mean AC 
    dom_mean_AC = np.mean(dom_AC)
    non_dom_mean_AC = np.mean(non_dom_AC) 

    #Mean Bilateral Magnitude
    mean_bilateral_magnitude = np.mean(bilateral_magnitude)

    #Mean Magnitude Ratio 
    mean_magnitude_ratio = np.mean(magnitude_ratio)

    return dom_AD, non_dom_AD, bimanual_AD, use_ratio_time, dom_mean_AC, non_dom_mean_AC, mean_bilateral_magnitude, mean_magnitude_ratio


def metrics(dom_AC, non_dom_AC):
    """ This function calculates various metrics based on the dominant and non-dominant arm activity counts.
    :param dom_AC : list of dominant arm activity counts
    :param non_dom_AC : list of non dominant arm activity counts
    :return df_metrics : dict containing the metrics
    """
    magnitude_ratio, bilateral_magnitude = sec_metrics(dom_AC, non_dom_AC)
    maui, baui = maui_baui(dom_AC, non_dom_AC)
    dom_AD, non_dom_AD, bimanual_AD, use_ratio_time, dom_mean_AC, non_dom_mean_AC, mean_bilateral_magnitude, mean_magnitude_ratio = mean_metrics(dom_AC, non_dom_AC, magnitude_ratio, bilateral_magnitude)

    df_metrics = {
        "dom_AD": dom_AD,
        "non_dom_AD": non_dom_AD,
        "bimanual_AD" : bimanual_AD,
        "use_ratio_time": use_ratio_time,
        "dom_mean_AC": dom_mean_AC,
        "non_dom_mean_AC": non_dom_mean_AC,
        "mean_bilateral_magnitude": mean_bilateral_magnitude,
        "mean_magnitude_ratio": mean_magnitude_ratio,
        "maui": maui,
        "baui": baui
    }
    return df_metrics 