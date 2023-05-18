""" dataConsolidation.py

This script allows to combine multiple csv files from doordash and grubhub website into single dataframe
using glob package of python

This file can also be imported as a module and contains the following
functions:
    * main
    * consolidate_files
"""
import pandas as pd
import glob


def consolidate_files(path, filename):
    """
    consolidate_files function is used to merge all csv files into single single dataframe

    :param path: path for website based data collected in csv files
    :param filename: filename for the output file
    :return: None
    """
    all_csv_files = glob.glob(path + "/*.csv")
    df_files = (pd.read_csv(f) for f in all_csv_files)
    df = pd.concat(df_files, ignore_index=True)
    df.to_csv('C:/Users/14057/Documents/PYTHON/Online Food Industry/CLEANED DATA/' + filename, sep=',', index=False)


def main():
    """
    main function is used to call consolidate function with different paths and filenames

    :return: None
    """
    path = r'C:\Users\14057\Documents\PYTHON\Online Food Industry\SCRAPED DATA'
    consolidate_files(path, 'cleaned_data.csv')


if __name__ == "__main__":
    main()
