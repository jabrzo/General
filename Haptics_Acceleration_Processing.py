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
from scipy.signal import find_peaks
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('TkAgg')
from scipy.optimize import curve_fit
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
    start = np.argmax(abs(data)>.75)
    to_check = 'end'
    for ii in range(start,len(data)):
        if to_check == 'end':
            if all(abs(data[ii:ii+80])<0.4):
                end = ii
                if index_array == []:
                    index_array = np.array([[start-50,end+50]])
                else:
                    index_array = np.vstack((index_array,[start-50,end+100]))
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
            start,end = clipData(main_acc)
            acc_x = acc_x.iloc[:,0].to_numpy(dtype=float)
            acc_y = acc_y.iloc[:,0].to_numpy(dtype=float)
            acc_z = acc_z.iloc[:,0].to_numpy(dtype=float)
            dxd.close()

        index_array = splitData(main_acc)
        time_series = time_series*1000
        main_acc = main_acc/9.81
        acc_x = acc_x/9.81
        acc_y = acc_y/9.81
        acc_z = acc_z/9.81
        plt.style.use('dark_background')

        # plt.plot(time_series[start:end],main_acc[start:end], color = '#83C8C0')
        print(f'Filename:{os.path.splitext(file)[0]}  Pulses:{len(index_array)}\n')
        print(index_array)
        name_topLevel = os.path.splitext(file)[0]
        device = name_topLevel.split('_')[0]
        if len(name_topLevel.split('_')) == 2:
            location = ''
        else:
            location = ' Location: ' + name_topLevel.split('_')[1] + ' |'

        profile = name_topLevel.split('_')[-1]

        for idx,x in enumerate(index_array):
            peaks = []
            peaks, _ = find_peaks(main_acc[x[0]:x[1]], height = .02, distance = 30,width=10)
            peaks_x, _ = find_peaks(acc_x[x[0]:x[1]], height=.02, distance=30, width=10)
            peaks_y, _ = find_peaks(acc_y[x[0]:x[1]], height=.02, distance=30, width=10)
            peaks_z, _ = find_peaks(acc_z[x[0]:x[1]], height=.02, distance=30, width=10)
            peaks = peaks + x[0]
            peaks_x = peaks_x + x[0]
            peaks_y = peaks_y + x[0]
            peaks_z = peaks_z + x[0]
            # gs = gridspec.GridSpec(3, 1,
            #                        width_ratios=[1, 2],
            #                        height_ratios=[4, 1]
            #
            axs = [None,None,None,None]
            fig = plt.figure()
            gs = fig.add_gridspec(3, 2)
            # fig, axs = plt.subplots(3)
            fig.tight_layout()
            axs[0] = fig.add_subplot(gs[0, :])
            axs[1] = fig.add_subplot(gs[1, :])
            axs[2] = fig.add_subplot(gs[2, 0])
            axs[3] = fig.add_subplot(gs[2, 1])
            axs[3].axis('off')


            fig.subplots_adjust(hspace=.3)
            fig.set_size_inches(24, 11)
            fig.suptitle(f'Device: {device} |{location} Profile: {profile} | Pulse:{idx+1}/{len(index_array)}')
            axs[0].set(xlabel='Time (ms)', ylabel='Acceleration (G)')
            axs[1].set(xlabel = 'Time (ms)', ylabel = 'Acceleration (G)')

            axs[1].set_xticks(np.arange(int(time_series[x[0]]), int(time_series[x[1]]), 5))
            axs[2].set(xlabel='Frequency (Hz)', ylabel='Amplitude', title = 'FFT')
            axs[2].set_xlim(0, 2000)
            axs[2].set_xticks(np.arange(0, 2000, 200))

            N = len(time_series[x[0]:x[1]])
            T = 1/SAMPLE_RATE
            xf = fftfreq(N, T)[:N//2]
            # xf = fftfreq(len(time_series[x[0]:x[1]]),1/SAMPLE_RATE)
            yf = fft(main_acc[x[0]:x[1]])
            yf_x = fft(acc_x[x[0]:x[1]])
            yf_y = fft(acc_y[x[0]:x[1]])
            yf_z = fft(acc_z[x[0]:x[1]])

            yf_freq = round(xf[1:N // 2][np.argmax(np.abs(yf[1:N//2]))],1)
            yfx_freq = round(xf[1:N // 2][np.argmax(np.abs(yf_x[1:N // 2]))], 1)
            yfy_freq = round(xf[1:N // 2][np.argmax(np.abs(yf_y[1:N // 2]))], 1)
            yfz_freq = round(xf[1:N // 2][np.argmax(np.abs(yf_z[1:N // 2]))], 1)

            main_acc_peak = round(np.max(abs(main_acc[x[0]:x[1]])),2)
            accx_peak = round(np.max(abs(acc_x[x[0]:x[1]])), 2)
            accy_peak = round(np.max(abs(acc_y[x[0]:x[1]])), 2)
            accz_peak = round(np.max(abs(acc_z[x[0]:x[1]])), 2)

            main_acc_peak_loc = np.argmax(abs(main_acc[x[0]:x[1]]))
            accx_peak_loc = np.argmax(abs(acc_x[x[0]:x[1]]))
            accy_peak_loc = np.argmax(abs(acc_y[x[0]:x[1]]))
            accz_peak_loc = np.argmax(abs(acc_z[x[0]:x[1]]))

            main_acc_90_rise =  round(time_series[x[0]:x[1]][np.argmax(np.abs(main_acc[x[0]:x[1]])>= 0.9*main_acc_peak)] - time_series[x[0]+50],3)
            accx_90_rise = round(time_series[x[0]:x[1]][np.argmax(np.abs(acc_x[x[0]:x[1]])>= 0.9*accx_peak)] - time_series[x[0]+50],3)
            accy_90_rise = round(time_series[x[0]:x[1]][np.argmax(np.abs(acc_y[x[0]:x[1]])>= 0.9*accy_peak)] - time_series[x[0]+50],3)
            accz_90_rise = round(time_series[x[0]:x[1]][np.argmax(np.abs(acc_z[x[0]:x[1]])>= 0.9*accz_peak)] - time_series[x[0]+50],3)
            length = len(time_series[x[0] + main_acc_peak_loc:x[1]])
            main_acc_90_fall = -1* round(time_series[x[0]+main_acc_peak_loc:x[1]][np.argmax(
                np.abs(main_acc[x[0]+main_acc_peak_loc:x[1]])<= 0.9*main_acc_peak)] -
                                     time_series[x[1] - np.argmax(np.abs(np.flip(main_acc[x[0]:x[1]]))>= 0.1*main_acc_peak)],3)

                # -1* round(time_series[x[0]+main_acc_peak_loc] - time_series[x[1]-(np.argmax(
                # np.abs(np.flip(main_acc[x[0]+main_acc_peak_loc:x[1]]))>= 0.9*main_acc_peak))],3)

            accx_90_fall = -1* round(time_series[x[0]+accx_peak_loc:x[1]][np.argmax(
                np.abs(acc_x[x[0]+accx_peak_loc:x[1]])<= 0.9*accx_peak)] -
                                     time_series[x[1] - np.argmax(np.abs(np.flip(acc_x[x[0]:x[1]]))>= 0.1*accx_peak)],3)

            accy_90_fall = -1* round(time_series[x[0]+accy_peak_loc:x[1]][np.argmax(
                np.abs(acc_y[x[0]+accy_peak_loc:x[1]])<= 0.9*accy_peak)] -
                                     time_series[x[1] - np.argmax(np.abs(np.flip(acc_y[x[0]:x[1]]))>= 0.1*accy_peak)],3)

            accz_90_fall = -1* round(time_series[x[0]+accz_peak_loc:x[1]][np.argmax(
                np.abs(acc_z[x[0]+accz_peak_loc:x[1]])<= 0.9*accz_peak)] -
                                     time_series[x[1] - np.argmax(np.abs(np.flip(acc_z[x[0]:x[1]]))>= 0.1*accz_peak)],3)


            data = [
                [f'{str(yf_freq)} Hz',f'{str(yfx_freq)} Hz',f'{str(yfy_freq)} Hz',f'{str(yfz_freq)} Hz'],
                [f'{str(main_acc_peak)} G', f'{str(accx_peak)} G',f'{str(accy_peak)} G', f'{str(accz_peak)} G'],
                [f'{str(main_acc_90_rise)} ms', f'{str(accx_90_rise)} ms', f'{str(accy_90_rise)} ms',
                 f'{str(accz_90_rise)} ms'],
                [f'{str(main_acc_90_fall)} ms', f'{str(accx_90_fall)} ms', f'{str(accy_90_fall)} ms',
                 f'{str(accz_90_fall)} ms']
            ]
            columns = ['ROI','Opposite X','Opposite Y','Opposite Z']
            row_labels = ['Frequency','Peak Acceleration','90% Rise Time','90% Fall Time']
            table = axs[3].table(cellText=data,colLabels = columns,rowLabels = row_labels,loc='center',
                                 colColours=['#DC373C','#419BD7','#55B473','#9B69AA'],cellLoc='center')
            table.set_fontsize(10)
            for key, cell in table.get_celld().items():
                # cell.set_edgecolor('#FFFFFF')
                # cell.set_facecolor('#636363')
                cell._text.set_color('black')
            if location == 'South':
                label = 'ROI X'
            else:
                label = 'ROI Z'
            axs[0].plot(time_series[start:end], main_acc[start:end], color='#83C8C0')
            axs[0].plot(time_series[x[0]:x[1]], main_acc[x[0]:x[1]], color='#FFDE89')


            axs[1].plot(time_series[x[0]:x[1]],main_acc[x[0]:x[1]], color='#DC373C',label = label)
            axs[1].plot(time_series[x[0]:x[1]], acc_x[x[0]:x[1]], color='#419BD7', label='Opposite X')
            axs[1].plot(time_series[x[0]:x[1]], acc_y[x[0]:x[1]], color='#55B473', label='Opposite Y')
            axs[1].plot(time_series[x[0]:x[1]], acc_z[x[0]:x[1]], color='#9B69AA', label='Opposite Z')
            axs[1].legend()
            axs[1].scatter(time_series[peaks], main_acc[peaks], color='#DC373C',marker = "o")
            axs[1].scatter(time_series[peaks_x], acc_x[peaks_x], color='#419BD7', marker="o")
            axs[1].scatter(time_series[peaks_y], acc_y[peaks_y], color='#55B473', marker="o")
            axs[1].scatter(time_series[peaks_z], acc_z[peaks_z], color='#9B69AA', marker="o")


            axs[2].plot(xf[1:N//2], np.abs(yf[1:N//2]), color='#DC373C')
            axs[2].plot(xf[1:N // 2], np.abs(yf_x[1:N // 2]), color='#419BD7')
            axs[2].plot(xf[1:N // 2], np.abs(yf_y[1:N // 2]), color='#55B473')
            axs[2].plot(xf[1:N // 2], np.abs(yf_z[1:N // 2]), color='#9B69AA')

            # mng = plt.get_current_fig_manager()
            # ### works on Ubuntu??? >> did NOT working on windows
            # # mng.resize(*mng.window.maxsize())
            # mng.window.state('zoomed')
            # ax.plot(time_series[x[0]:x[1]],main_acc[x[0]:x[1]], color='#DC373C')
            save_file = os.path.join(folder,'processed',f'{name_topLevel}.png')
            plt.savefig(save_file, bbox_inches='tight',dpi=100)
            # plt.show()




