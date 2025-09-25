""" This file contains the conversion of raw accelerometer data from a CSV file into activity counts.
It reads the CSV file, processes the accelerometer data, and returns a DataFrame with activity counts.
This code is extracted from github "https://github.com/actigraph/agcounts", and was published with the work of Neishabouri et al. (2022).
Called in main.py """

from agcounts.extract import get_counts
import pandas as pd
import numpy as np
from interface import update_progress

def get_counts_csv(
    file,
    freq: int,
    epoch: int,
    fast: bool = True,
    verbose: bool = False,
    time_column: str = None,
    progress_data: dict = None,
    progress_idx: int = 0,
    nb_file_to_read: int = 0,
    idx_interface: int =0
):
    if verbose:
        print("Reading in CSV", flush=True)
        # Interface
        progress_data["interface"].after(0, update_progress, progress_idx , progress_data["bar"], progress_data["interface"], f"Conversion des données brutes en array ...", progress_data["message_label"], progress_data["progress_title"])
    raw = pd.read_csv(file, skiprows=10,decimal=",") # skiprows = 0 if the file has no header, skiprows = n if the file has n header rows
    if time_column is not None:
        ts = raw[time_column]
        ts = pd.to_datetime(ts)
        time_freq = str(epoch) + "s"
        ts = ts.dt.round(time_freq)
        ts = ts.unique()
        ts = pd.DataFrame(ts, columns=[time_column])
    raw = raw[["Accelerometer X", "Accelerometer Y", "Accelerometer Z"]].astype(float)
    if verbose:
        print("Converting to array", flush=True)
        # Interface
        progress_data["interface"].after(0, update_progress, progress_idx +(1/12)*int(idx_interface)/nb_file_to_read, progress_data["bar"], progress_data["interface"], f"Conversion en Activity Counts ...", progress_data["message_label"],progress_data["progress_title"])
    raw = np.array(raw)
    if verbose:
        print("Getting Counts", flush=True)
        # Interface
        progress_data["interface"].after(0, update_progress, progress_idx +(2/12)*int(idx_interface)/nb_file_to_read, progress_data["bar"], progress_data["interface"], f"Conversion en Activity Counts ...", progress_data["message_label"],progress_data["progress_title"])
    counts = get_counts(raw, freq=freq, epoch=epoch, fast=fast)
    del raw
    counts = pd.DataFrame(counts, columns=["Axis1", "Axis2", "Axis3"])
    counts["AC"] = (
        counts["Axis1"] ** 2 + counts["Axis2"] ** 2 + counts["Axis3"] ** 2
    ) ** 0.5
    if time_column is not None:
        ts = ts[0 : counts.shape[0]]
        counts = pd.concat([ts, counts], axis=1)
    return counts


def convert_counts_csv(
    file,
    outfile,
    freq: int=30,
    epoch: int=1,
    verbose: bool = False,
    time_column: str = None,
    progress_data: dict = None,
    progress_idx: int = 0,
    nb_file_to_read: int = 0,
    idx_interface: int = 0,
):
    counts = get_counts_csv(
        file, freq=freq, epoch=epoch, verbose=verbose, time_column=time_column, progress_data=progress_data, progress_idx=progress_idx, nb_file_to_read=nb_file_to_read, idx_interface=idx_interface)
    counts.to_csv(outfile, index=False)
    return counts


def convert_AC(file_dom, file_non_dom,nb_file_to_read,idx_interface, progress_data=None,):

    dom_counts = get_counts_csv(file_dom, freq=30, epoch=1, progress_data=progress_data, progress_idx= 1/12 * (int(idx_interface) / nb_file_to_read), nb_file_to_read=nb_file_to_read, idx_interface=idx_interface)
    dom_counts = convert_counts_csv(
        file_dom,
        outfile="Activity_counts_files/dom_counts.csv",
        freq=30,
        epoch=1,
        verbose=True,
        time_column="Timestamp",
        progress_data=progress_data,
        progress_idx= int(idx_interface)/nb_file_to_read + (1/12)*1/nb_file_to_read ,
        nb_file_to_read=nb_file_to_read
    )

    non_dom_counts = get_counts_csv(file_non_dom, freq=30, epoch=1, progress_data=progress_data, progress_idx=4/12*int(idx_interface)/nb_file_to_read, nb_file_to_read=nb_file_to_read,idx_interface=idx_interface)
    non_dom_counts = convert_counts_csv(
        file_non_dom,
        outfile="Activity_counts_files/non_dom_counts.csv",
        freq=30,
        epoch=1,
        verbose=True,
        time_column="Timestamp",
        progress_data=progress_data,
        progress_idx=  int(idx_interface)/nb_file_to_read +(4/12)*1/nb_file_to_read,
        nb_file_to_read=nb_file_to_read
    )



    return dom_counts, non_dom_counts