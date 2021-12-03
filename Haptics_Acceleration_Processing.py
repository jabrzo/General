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


def clipData(data):
    start = np.argmax(abs(data)>1) - 50
    end = data.shape[0] - (np.argmax(abs(np.flip(data))>1) - 200)

    return start,end

# def checkConsecutive(data,value,num_consecutive):

def splitData(data):
    index = []
    index_array = []
    start = np.argmax(abs(data)>1)
    to_check = 'end'
    for ii in range(start,len(data)):
        if to_check == 'end':
            if all(abs(data[ii:ii+80])<0.4):
                end = ii
                if index_array == []:
                    index_array = np.array([[start-50,end+50]])
                else:
                    index_array = np.vstack((index_array,[start-50,end+50]))
                to_check = 'start'
        elif to_check == 'start':
            if abs(data[ii])>1:
                start = ii
                to_check = 'end'

    return index_array

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


    file_names = []
    for root, dirs_list, files_list in os.walk(folder):
        for file_name in files_list:
            if os.path.splitext(file_name)[-1] == '.dxd':
                file_names.append(file_name)
        pass

    for file in file_names:

        with dw.open(os.path.join(folder,file)) as dxd:
            main_acc = dxd['ACC_1'].dataframe()
            acc_x = dxd['ACC_2_X'].dataframe()
            acc_y = dxd['ACC_3_Y'].dataframe()
            acc_z = dxd['ACC_4_Z'].dataframe()
            time_series = main_acc.index.to_numpy(dtype=float)
            main_acc = main_acc.iloc[:,0].to_numpy(dtype=float)
            acc_x = acc_x.iloc[:,0].to_numpy(dtype=float)
            acc_y = acc_y.iloc[:,0].to_numpy(dtype=float)
            acc_z = acc_z.iloc[:,0].to_numpy(dtype=float)
            dxd.close()

        index_array = splitData(main_acc)
        fig =  plt.figure(1)
        ax = fig.add_subplot(111)
        plt.plot(time_series,main_acc)
        print(f'Filename:{file}  Pulses:{len(index_array)}\n')
        print(index_array)
        for x in index_array:
            ax.plot(time_series[x[0]:x[1]],main_acc[x[0]:x[1]], color='red')
        plt.show()



