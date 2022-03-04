import pandas
import tkinter as tk
from tkinter import filedialog

import os
from datetime import datetime
import sys


def startCase(case_name:str,delay_ms:int):
    string = f"\nPriority Msg >> MainUI >> Test Case Description >> {case_name}\n" \
             f"Wait >> {delay_ms}\n" \
             "Priority Msg >> MainUI >> Data: Save Measurement\n" \
             "Break\n"\
             'Priority Msg >> MainUI >> UI: Set Plot >> Start\n' \
             'Priority Msg >> MainUI >> UI: Continuous Plot\n'

    return string

def gearedMotionProfile(x_dist:float,y_dist:float,z_dist:float,rate:float,delay_ms:int):
    script = "\nAcquire Target Positions\n" \
             f"Wait >> {delay_ms}\n" \
             f"Geared Motion >> X,{x_dist},{rate},R\n" \
             f"Geared Motion >> Y,{y_dist},{rate},S\n" \
             f"Geared Motion >> Z,{z_dist},{rate},S\n" \
             f"Wait >> 750\n" \
             "Delay >> 120000, MOTOR_X_Status, 2, Int, 2\n" \
             "Delay >> 120000, MOTOR_Y_Status, 2, Int, 2\n" \
             "Delay >> 120000, MOTOR_Z_Status, 2, Int, 2\n" \
             "Delay >> 120000, MOTOR_A_Status, 2, Int, 2\n" \
             "Delay >> 120000, MOTOR_C_Status, 2, Int, 2\n" \
             "Delay >> 120000, MOTOR_B_Status, 2, Int, 2\n" \

    return script


def motorizedBaffle(delay_ms:int):

    script = "\nAcquire Target Positions\n" \
             'Priority Msg >> MainUI >> DAQ >> EQV12_DO >> DO Port >> 0, 0, 1, 1\n' \
             f"Wait >> {delay_ms}\n" \
             'Priority Msg >> MainUI >> DAQ >> EQV12_DO >> DO Port >> 0, 0, 0, 1\n' \
             f"Wait >> {delay_ms}\n" \
             'Priority Msg >> MainUI >> DAQ >> EQV12_DO >> DO Port >> 0, 0, 0, 0\n' \
             f"Wait >> {500}\n"

    return script

def initializeMeasurement():
    string = '\nPriority Msg >> MainUI >> Measurement File >> EQV12 Measurement\n' \
             'Priority Msg >> MainUI >> Data: Save Measurement >> Header\n' \
             'Break\n'

    return string
def saveMeasurementData(delay_ms,test_case):
    # test_case = test_case+'.csv'
    string = '\n// Save Measurement data\n' \
             'Priority Msg >> MainUI >> Data: Save Measurement\n' \
             'Break\n' \
             '// Save time-based data, capture screen and clear waveform\n' \
             'Priority Msg >> MainUI >> Save Data \n' \
             'Priority Msg >> MainUI >> Screen Shot\n' \
             'Priority Msg >> MainUI >> UI: Set Plot >> Stop\n' \
             'Priority Msg >> MainUI >> UI: Clear Waveform\n' \
             f'Wait >> {delay_ms}\n'
    # f"Priority Msg >> MainUI >> Data:Save Raw >> {test_case}"\
         # f"Priority Msg >> MainUI >> UI:Screenshot >> {test_case}"\
         # 'Priority Msg >> MainUI >> UI: Set Plot >> Stop\n'\
         # 'Priority Msg >> MainUI >> UI: Clear Waveform\n' \
         # f'Wait >> {delay_ms}\n'
         # f'Priority Msg >> MainUI >> Save Data >> {test_case}\n' \

    return string

def addDelay(delay_ms:int):
    return f'Wait >> {delay_ms}\n'

def setSpeed(rate:float):
    string = f'\nSet Speed >> {rate} >> 1\n'\
             f'Set Speed >> {rate} >> 2\n'\
             f'Set Speed >> {rate} >> 3\n'\
             f'Set Speed >> {rate} >> 4\n'\
             f'Set Speed >> {rate} >> 5\n'\
             f'Set Speed >> {rate} >> 6\n'

    return string

def takeDICImage(wait_time_ms:int):
    string = '\n// Turn on lights\n'\
             'Priority Msg >> MainUI >> DAQ >> EQV12_DO >> DO Port >> 0, 1, 0, 0\n' \
             f'Wait >> {wait_time_ms}\n' \
             '// Take Image\n' \
             'Priority Msg >> MainUI >> DAQ >> EQV12_DO >> DO Port >> 1, 1, 0, 0\n' \
             f'Wait >> {wait_time_ms}\n' \
             '// Turn off lights and reset image trigger\n' \
             'Priority Msg >> MainUI >> DAQ >> EQV12_DO >> DO Port >> 0, 0, 0, 0\n' \

    return string


def browseFile():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(title="Open Test Script File",filetypes=(("csv", "*.csv"),
                                       ("All files", "*.*") ))

    return file_path


if __name__ == '__main__':

    initial_string = 'UI: Clear Waveform\n' \
                     'Motor Macro\n' \
                     'Single Axis >> False\n' \
                     '// Check motors faults\n' \
                     'Check Faults\n' \
                     '// Example to check all axes home status, abort test if any one of axes was not homed\n' \
                     'Check Home\n' \
                     '\n' \
                     '\n' \
                     '\n'

    end_string = '\nPriority Msg >> MainUI >> Start >> Stop\n' \
                 'Priority Msg >> MainUI >> UI: Clear Waveform\n' \
                 '\nMotor Macro End\n' \
                 'Motor >> Run Script\n'

    seqFile = browseFile()
    filename = os.path.split(seqFile)[-1][:-14]
    df = pandas.read_csv(seqFile)
    case_names = df.iloc[2:,1].to_numpy()
    displacementVals_X = df.iloc[2:, 8].to_numpy(dtype=float)
    displacementVals_y = df.iloc[2:, 9].to_numpy(dtype=float)
    displacementVals_z = df.iloc[2:, 10].to_numpy(dtype=float)

    desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
    filepath = os.path.join(desktop, 'EQV12_Scripts')
    case_file = r"G:\Shared drives\AR DVE\AR ME DVE\Delphi DVE\Builds\P0\EQVs\EQV12\Scripts"
    # r"C:\Users\jbrzostowski\Desktop\Hinge Process"
    if os.path.exists(case_file) == False:
        if os.path.exists(filepath) == False:
            os.mkdir(filepath)
    else:
        filepath = case_file
    # filepath = r"C:\Users\jbrzostowski\Documents\EQV12 Scripts"
    # os.makedirs(filepath, exist_ok=True)
    now = datetime.now()
    date_time = now.strftime("%Y_%m_%d_%H_%M_%S")
    filename = filename + date_time +'.txt'

    file = os.path.join(filepath,filename)
    # string = takeDICImage(1000)
    with open(file,'a') as f:
        f.writelines(initial_string)
        f.writelines(initializeMeasurement())
        f.writelines(takeDICImage(1000))
        for idx,case in enumerate(case_names):
            f.write(startCase(case,100))
            f.writelines(gearedMotionProfile(displacementVals_X[idx],displacementVals_y[idx],displacementVals_z[idx],
                                          30.0,500))
            f.writelines(addDelay(1500))
            f.writelines(motorizedBaffle(5000))
            f.writelines(saveMeasurementData(1000,case))
            f.writelines(takeDICImage(750))

        f.writelines(end_string)
    print(f'\n\nCreated Sequence with {len(case_names)} cases\n')