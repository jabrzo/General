import pandas
import tkinter as tk
from tkinter import filedialog

import os
import csv
from datetime import datetime
import sys
import numpy as np

def browseFile(dir=False):
    root = tk.Tk()
    root.withdraw()
    if dir:
        file_path = filedialog.askdirectory(title="Test File Location")
    else:
        file_path = filedialog.askopenfilename(title="Select File",filetypes=(("csv", "*.csv"),
                                           ("All files", "*.*")))
    return file_path


if __name__ == '__main__':
    dir = r'D:\EQV14-CTE'
    os.chdir(dir)
    print(os.curdir)
    seqFile = browseFile()
    file_path = os.path.split(seqFile)[0]
    file_name = os.path.split(seqFile)[-1][:-4] +'_formatted.csv'
    df = pandas.read_csv(seqFile)

    temp_names = []
    temp_idx = []
    element_names = []
    element_idx =[]

    for ii in range(df.shape[0]):
        if 'Temp' not in df.iloc[ii,1]:
            element_names.append(df.iloc[ii,0])
            element_idx.append(ii)
        else:
            temp_names.append(df.iloc[ii,0])
            temp_idx.append(ii)

    headers = df.columns.to_numpy(dtype=str)
    start_col_index = 0
    for idx,x in enumerate(headers):
        if "Start" in x:
            start_col_index = idx
            break

    file = os.path.join(file_path,file_name)
    DUT = file_name.split("_")[3]
    fixture = file_name.split("_")[0]
    temp = file_name.split("_")[1]
    with open(file, mode='w',newline='') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_header = ['Element','DUT','Stage','Displacement (um)','Fixturing','Test Temp'] + temp_names
        csv_writer.writerow(csv_header)

        for x in range(start_col_index,len(headers)):
            for idx,y in enumerate(element_names):
                temps = []
                for jj in temp_idx:
                    temps.append(df.iloc[jj,x])
                data_list = [y,DUT,headers[x],df.iloc[idx,x],fixture,temp] + temps
                print(data_list)
                csv_writer.writerow(data_list)

    text = "start EXCEL.EXE " + file