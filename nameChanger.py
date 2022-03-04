import pandas
import tkinter as tk
from tkinter import filedialog
import numpy as np
import os
import csv
import pandas
from datetime import datetime
import time

def browseFile(dir=False):
    root = tk.Tk()
    root.withdraw()
    if dir:
        file_path = filedialog.askdirectory(title="Test File Location")
    else:
        file_path = filedialog.askopenfilename(title="Select File",filetypes=(("csv", "*.csv"),
                                           ("All files", "*.*") ))
    return file_path

folder = r"D:\New folder\L148_R096"

csv_files = []

def browseFile(dir=False):
    root = tk.Tk()
    root.withdraw()
    if dir:
        file_path = filedialog.askdirectory(title="Test File Location")
    else:
        file_path = filedialog.askopenfilename(title="Select File",filetypes=(("csv", "*.csv"),
                                           ("All files", "*.*") ))
    return file_path

locations = ['Loc_80','Loc_100','Loc_120']
case_file = r"G:\Shared drives\AR DVE\AR ME DVE\Delphi DVE\Builds\P0\EQVs\EQV12\Scripts\EQV12_Case_Names.csv"


if __name__ == '__main__':
    value = '0'
    while True:
        while value not in ['1','2']:
            value = input("Enter:\n(1) To change Labview Data Files\n(2) To append DIC filenames\n->")
            loc = None
            if value not in ['1','2']:
                print("Input not recognized. Please select again.\n")

            while loc is None:
                loc = input("Enter:\n(1) For Loc_80\n(2) For Loc_100\n(3) For Loc_120\n->")
                if loc in ['1', '2', '3']:
                    location = locations[int(loc) - 1]
                    print(f'\nPlease Select folder containing {location} dataset\n')
                    df = pandas.read_csv(case_file)
                    case_names = df[location].to_numpy(dtype=str)


        time.sleep(.5)
        folder = browseFile(True)
        filenames = []
        time_stamps = []

        log_files = []
        log_file_times = []
        sorted_log_files_idx = []

        if value == '1':
            for root, dirs, files in os.walk(folder):
               for name in files:
                  if ".csv" in name :
                      try:
                          a = datetime.strptime(name[0:19], "%Y-%m-%d %H-%M-%S").timestamp()
                          time_stamps.append(a)
                          filenames.append(name)
                      except:
                          if 'EQV12 Measurement' in name:
                              log_file_times.append(datetime.strptime(name[18:-5], "%Y-%m-%d %H-%M-%S").timestamp())
                              log_files.append(name)

               break
            sorted_log_files_idx = np.argsort(log_file_times)
            sorted_timestamp_idx= np.argsort(time_stamps)
            case_names = []
            for x in sorted_log_files_idx:
                df = pandas.read_csv(os.path.join(folder,log_files[x]))
                case_names = case_names + list(df['Test_Case'])

            for idx,x in enumerate(sorted_timestamp_idx):
                # new_name = case_names[x] + '_' + filenames[x]
                new_name = case_names[idx] + '_'+ datetime.fromtimestamp(time_stamps[x]).strftime("%Y-%m-%d %H-%M-%S") + '_SN.csv'
                print(f"Re-Named {filenames[x]} to ->{new_name}")
                os.rename(os.path.join(folder, filenames[x]), os.path.join(root, new_name))

        if value == '2':
            for root, dirs, files in os.walk(folder):
                for name in files:
                    if ".csv" in name:
                        if name[-5] in ['1','2'] and name[-6] == ' ':
                            if f'Reference_{location}' not in name:
                                new_name = f'Reference_{location}_{name}'
                                os.rename(os.path.join(folder, name), os.path.join(folder, new_name))
                        else:
                            if location not in name:
                                new_name = f'{location}_{name}'
                                os.rename(os.path.join(folder, name), os.path.join(folder, new_name))
                        # time_stamps.append(a)
                        # filenames.append(name)
                break
            # sorted_timestamp_idx = np.argsort(time_stamps)
            # for x in sorted_timestamp_idx:
            #     new_name = case_names[x] + '_' + filenames[x]
            #     print(f"Re-Named {filenames[x]} to ->{new_name}")
            #     os.rename(os.path.join(folder, filenames[x]), os.path.join(root, new_name))
        value = '0'
