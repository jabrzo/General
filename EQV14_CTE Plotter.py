import pandas
import tkinter as tk
from tkinter import filedialog
import os
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('TkAgg')
from matplotlib import gridspec




def browseFile(path= "C:",title = 'Select File',types=(('All Files', "*.*"),),dir=False):
    root = tk.Tk()
    root.withdraw()
    if dir:
        title = 'Select Folder'
        file_path = filedialog.askdirectory(initialdir = path,title=title)
    else:
        file_path = filedialog.askopenfilename(initialdir = path,title=title, filetypes=types)
    return file_path

def getMaxMin(df):
    df_new = df
    index = df.index.to_numpy(dtype = str)
    for idx,x in enumerate(index):
        if 'F' in str(x):
            df_new = df_new.drop(labels = x,axis =0)
        if 'Temp' in str(x):
            df_new = df_new.drop(labels=x, axis=0)

    return np.nanmax(df_new.to_numpy(dtype =float)), np.nanmin(df_new.to_numpy(dtype =float))

def cleanDF(df):
    df = df.set_index('Element')
    a = df.index.to_numpy()
    for idx, x in enumerate(a):
        a[idx] = x.strip()
    df.index = a
    df = df.replace(to_replace='???', value=np.nan)
    for idx,x in enumerate(df.keys()):
        if 'Start' in x:
            df_new = df.drop(labels = df.keys()[:idx],axis =1)
            return df_new

if __name__ == '__main__':

    slice_1_names = ['Distance 20', 'Distance 21', 'Distance 22', 'Distance 23', 'Distance 24','Distance 25',
                     'Distance 00', 'Distance 08', 'Distance 07', 'Distance 06', 'Distance 05']

    slice_1_ticks = ['P20', 'P21', 'P22', 'P23', 'P24', 'P25', 'P00', 'P08', 'P07', 'P06', 'P05']

    slice_2_names = ['Distance 26', 'Distance 27', 'Distance 28', 'Distance 00', 'Distance 13','Distance 12',
                     'Distance 11', 'Distance 10', 'Distance 09']

    slice_2_ticks = ['P26', 'P27', 'P28', 'P00', 'P13', 'P12', 'P11', 'P10', 'P09']

    slice_3_names = ['Distance 14', 'Distance 15', 'Distance 16', 'Distance 17', 'Distance 18',
                     'Distance 19','Distance 00', 'Distance 04', 'Distance 03', 'Distance 02', 'Distance 01']

    slice_3_ticks = ['P14', 'P15', 'P16', 'P17', 'P18', 'P19', 'P00', 'P04', 'P03', 'P02', 'P01']
    # slice_1_names = ['Distance F11', 'Distance 20', 'Distance 21', 'Distance 22', 'Distance 23', 'Distance 24',
    #                  'Distance 25',
    #                  'Distance 00', 'Distance 08', 'Distance 07', 'Distance 06', 'Distance 05', 'Distance F04']
    #
    # slice_1_ticks = ['Frame1', 'P1', 'P2', 'P3', 'P4', 'P5', 'P6', 'P7', 'P8', 'P9', 'P10', 'P11', 'Frame2']
    #
    # slice_2_names = ['Distance F01', 'Distance 26', 'Distance 27', 'Distance 28', 'Distance 00', 'Distance 13',
    #                  'Distance 12',
    #                  'Distance 11', 'Distance 10', 'Distance 09', 'Distance F07']
    #
    # slice_2_ticks = ['Frame1', 'P1', 'P2', 'P3', 'P4', 'P5', 'P6', 'P7', 'P8', 'P9', 'Frame2']
    #
    # slice_3_names = ['Distance F09', 'Distance 14', 'Distance 15', 'Distance 16', 'Distance 17', 'Distance 18',
    #                  'Distance 19',
    #                  'Distance 00', 'Distance 04', 'Distance 03', 'Distance 02', 'Distance 01', 'Distance F03']
    #
    # slice_3_ticks = ['Frame1', 'P1', 'P2', 'P3', 'P4', 'P5', 'P6', 'P7', 'P8', 'P9', 'P10', 'P11', 'Frame2']

    dir = r'D:\EQV14-CTE'
    os.chdir(dir)
    file_1 = browseFile(path = dir, title='Select First Summary File',types = (('csv',"*.csv"),('All Files','*.*'),))
    file_2 = browseFile(path = dir, title='Select Second Summary File',types=(('csv', "*.csv"), ('All Files', '*.*'),))


    df_1 = pandas.read_csv(file_1)
    df_1 = cleanDF(df_1)
    temps_1 = df_1.loc['Temp'].to_numpy(dtype = float).round(decimals = 2)
    temp_indices_1 = [0, 1]
    ii = 0
    for idx,temp in enumerate(temps_1[2:]):
        if temp == temps_1[-1]:
            temp_indices_1.append(idx+2)
            break
        if abs(temps_1[ii+1]) - abs(temp) >=5:
            temp_indices_1.append(idx+2)
            ii =idx+1

    df_1_max,df_1_min = getMaxMin(df_1)
    slice_11 = df_1.loc[slice_1_names].to_numpy(dtype = float).round(decimals = 2)
    slice_21 = df_1.loc[slice_2_names].to_numpy(dtype = float).round(decimals = 2)
    slice_31 = df_1.loc[slice_3_names].to_numpy(dtype = float).round(decimals = 2)

    if file_2 != "":
        df_2 = pandas.read_csv(file_2)
        df_2 = cleanDF(df_2)
        temps_2 = df_2.loc['Temp'].to_numpy(dtype = float).round(decimals = 2)
        temp_indices_2 = [0, 1]
        ii = 0
        for idx, temp in enumerate(temps_2[2:]):
            if temp == temps_2[-1]:
                temp_indices_2.append(idx + 2)
                break
            if abs(temps_2[ii + 1] - temp) >= 5:
                temp_indices_2.append(idx + 2)
                ii = idx + 1

        slice_12 = df_2.loc[slice_1_names].to_numpy(dtype = float).round(decimals = 2)
        slice_22 = df_2.loc[slice_2_names].to_numpy(dtype = float).round(decimals = 2)
        slice_32 = df_2.loc[slice_3_names].to_numpy(dtype = float).round(decimals = 2)
        df_2_max, df_2_min = getMaxMin(df_2)

        # y_max = max(df_2_max,df_1_max)
        # y_min = max(df_2_min, df_1_min)
        y_max = df_1_max
        y_min = df_1_min

        colors = ['tab:blue',
                  'tab:orange',
                  'tab:green',
                  'tab:red',
                  'tab:purple',
                  'tab:brown',
                  'tab:pink',
                  'tab:gray',
                  'tab:olive',
                  'tab:cyan']

    image_1 = plt.imread(r'D:\EQV14-CTE\Slice_A.png')
    image_2 = plt.imread(r'D:\EQV14-CTE\Slice_B.png')
    image_3 = plt.imread(r'D:\EQV14-CTE\Slice_C.png')
    fig= plt.figure(figsize=(16, 8))
    fig.suptitle('Un-Constrained - S01')
    fig.tight_layout()
    gs = gridspec.GridSpec(3, 3, width_ratios=[.3, 1, 1])
    ax11 = plt.subplot(gs[0, 1])
    ax12 = plt.subplot(gs[0, 2])
    ax21 = plt.subplot(gs[1, 1])
    ax22 = plt.subplot(gs[1, 2])
    ax31 = plt.subplot(gs[2, 1])
    ax32 = plt.subplot(gs[2, 2])
    im1 = plt.subplot(gs[0, 0])
    im2 = plt.subplot(gs[1, 0])
    im3 = plt.subplot(gs[2, 0])
    im1.axis('off')
    im2.axis('off')
    im3.axis('off')
    im1.imshow(image_1)
    im2.imshow(image_2)
    im3.imshow(image_3)
    plt.subplots_adjust(hspace =0.3)

    for idx, kk in enumerate(temp_indices_1):
        plotted_color = colors[idx]
        linestyle = '-'
        if idx+1 == len(temp_indices_1):
            plotted_color = colors[0]
            linestyle = '--'

        ax11.plot(slice_1_ticks,slice_11[:,kk],label = str(temps_1[kk]),linestyle=linestyle,color = plotted_color)
        ax21.plot(slice_2_ticks,slice_21[:,kk], label=str(temps_1[kk]),linestyle=linestyle,color = plotted_color)
        ax31.plot(slice_3_ticks,slice_31[:,kk], label=str(temps_1[kk]),linestyle=linestyle,color = plotted_color)
    ax11.set_ylim([.95*y_min,1.02*y_max])
    ax21.set_ylim([.95*y_min,1.02*y_max])
    ax31.set_ylim([.95*y_min,1.02*y_max])
    ax11.invert_yaxis()
    ax21.invert_yaxis()
    ax31.invert_yaxis()
    ax11.set_title('Slice A - High Temp')
    ax21.set_title('Slice B - High Temp')
    ax31.set_title('Slice C - High Temp')
    ax11.set_ylabel(r'$\mu$m')
    ax21.set_ylabel(r'$\mu$m')
    ax31.set_ylabel(r'$\mu$m')
    ax31.legend(title='Temp (C)',loc='upper center', bbox_to_anchor=(0.5, -0.15),
                ncol=6, handleheight=2, labelspacing=0.01,prop={'size': 8})



    for idx, kk in enumerate(temp_indices_2):
        plotted_color = colors[idx]
        linestyle = '-'
        if idx + 1 == len(temp_indices_2):
            plotted_color = colors[0]
            linestyle = '--'

        ax12.plot(slice_1_ticks, slice_12[:, kk], label=str(temps_2[kk]), linestyle=linestyle, color=plotted_color)
        ax22.plot(slice_2_ticks, slice_22[:, kk], label=str(temps_2[kk]), linestyle=linestyle, color=plotted_color)
        ax32.plot(slice_3_ticks, slice_32[:, kk], label=str(temps_2[kk]), linestyle=linestyle, color=plotted_color)
    ax12.set_ylim([.95*y_min,1.02*y_max])
    ax22.set_ylim([.95*y_min,1.02*y_max])
    ax32.set_ylim([.95*y_min,1.02*y_max])
    ax12.invert_yaxis()
    ax22.invert_yaxis()
    ax32.invert_yaxis()
    ax12.set_title('Slice A - Low Temp')
    ax22.set_title('Slice B - Low Temp')
    ax32.set_title('Slice C - Low Temp')
    ax12.set_ylabel(r'$\mu$m')
    ax22.set_ylabel(r'$\mu$m')
    ax32.set_ylabel(r'$\mu$m')
    ax32.legend(title='Temp (C)',loc='upper center', bbox_to_anchor=(0.5, -0.15),
                ncol=6, handleheight=2, labelspacing=0.01,prop={'size': 8})

    plt.show()