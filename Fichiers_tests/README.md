# quantification_mvt

:file "Metric_calculation.ipynb" :
Main files of the repository containing a guide line to load, process the data and calculate metrics

:file "Compression_comparison.ipynb" :
Comparison of 3 methods of compression (transformation of a 100Hz signal into a 1Hz signal).
    1. Compression with numpy
    2. Compression with pandas
    3. Compression from scratch

:file "Data_processing_method1.ipynb" :
In this file data are processed following steps :
    1. Band pass filter to remove outliers : Each of the three signals (x, y and z) from the 2 sensors (left and right) is filtered with a passband filter separately
    2. Compression of the 100Hz signal in 1Hz signal
    3. Calculation of the euclidian norm (VM) (sqrt(x² + y² + z²) for each 1s epoch) as activity counts

:file "Data_processing_method2.ipynb" :
In this file data are processed following Poitras et al. article steps (after resample 100Hz in 30Hz signal) :
    1. Resampling 100Hz in 30Hz signal
    2. Band pass filter to remove outliers : Each of the three signals (x, y and z) from teh 2 sensors (left and right) is filtered with a passband filter 
    3. Compression of the 30Hz signal in 1Hz signal
    4. Calculation of the euclidian norm (sqrt(x² + y² + z²) for each 1s epoch) as activity counts


:file "Metric_calculation - Copie.ipynb" : Copy of the guide line

:file "Test_activity_count.ipynb" :
Method to calculate activity count and active duration from scratch on raw data

:file "Cut_files.py" :
Programm to cut large csv files in short selected segment. Usefull to reduce calculation time
