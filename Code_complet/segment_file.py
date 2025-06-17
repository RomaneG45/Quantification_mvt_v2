"""This file select the time interval to analyse depending on the modality recorded (Therapy in center or daily life at home)"""

def segment(modality, segment_hours, dom_AC, non_dom_AC):
    """This function segments a file, depending on the therapy modality and hours of activity. If record in center, the file is segmented from 8h to 20h. If at home, the file is segmented depending on the hours of activity (parent's annotations)
    :param modality : Str of the modality type ("Center" or "Home")
    :param segment_hours : dict containing the start and end hours for one activity ( {start_record : [h1, h2...], end_record : [h1,h2...]} )
    :param dom_AC : list of non dominant arm activity counts
    :param non_dom_AC : list of non dominant arm activity counts
    return lst_segment : list containing the lists of AC segmented in activty time laps"""