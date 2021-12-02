import pandas
import tkinter as tk
from tkinter import filedialog
import dwdatareader as dw
import os
import csv
from datetime import datetime
import sys
import numpy as np
from scipy.fft import fft, fftfreq
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('TkAgg')
from matplotlib import gridspec

SAMPLE_RATE = 20000

def splitData(data):
    indicies = []

    return indicies

def browseFile(path= "C:",title = 'Select File',types=(('All Files', "*.*"),),dir=False):
    root = tk.Tk()
    root.withdraw()
    if dir:
        title = 'Select Folder'
        file_path = filedialog.askdirectory(initialdir = path,title=title)
    else:
        file_path = filedialog.askopenfilename(initialdir = path,title=title, filetypes=types)
    return file_path


if __name__ == '__main__':
    desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
    filepath = os.path.join(desktop, 'Haptics_Processed')
    # r"C:\Users\jbrzostowski\Desktop\Hinge Process"
    if os.path.exists(filepath) == False:
        os.mkdir(filepath)

    folder_path = r'G:\Shared drives\AR DVE\AR ME DVE\Stage DVE\Builds\P1\Haptics\POE Devices\Accelerometer'
    folder = browseFile(folder_path,'Select Accelerometer Data Folder', types =(('Dewesoft Data File', "*.dxd"),),dir=True)

    print('Test')
    file_names = []
    for root, dirs_list, files_list in os.walk(folder):
        for file_name in files_list:
            if os.path.splitext(file_name)[-1] == '.dxd':
                file_names.append(file_name)
        pass