from ezdxf.addons.drawing.matplotlib import MatplotlibBackend
from ezdxf.addons.drawing import Frontend, RenderContext
import ezdxf
import dxf2svg
import numpy as np
import os
from datetime import datetime
import random
import math
import tkinter as tk
from tkinter import filedialog

import matplotlib.pyplot as plt
import matplotlib as mpl

def checkArea():
    pass


def circleGenerator(width: float,height: float, dot_size_min: float,dot_size_max: float):
    area = height*width
    dot_ave = (dot_size_min +dot_size_max)/2

    dot_area = math.pi *((dot_ave/2)*(dot_ave/2))
    step = round(random.uniform(0,height),2)
    row = step
    num_dots = (area/dot_area)*0.45
    dots = None
    i = 0
    run = 0

    x_bins = np.linspace(0,width,num=20)
    y_bins = np.linspace(0, height, num=20)

    x_min = 0
    y_min = 0
    x_max = width
    y_max = height
    allowable_intersection = .9
    while True:

        r = (round(random.uniform(dot_size_min,dot_size_max),4))/2
        y = round(random.uniform(y_min,y_max),2)
        x = round(random.uniform(x_min,x_max), 2)

        two_r = 2 * r

        # if i > num_dots*.75:
        #     allowable_intersection = 1.01
        if i >num_dots:
            run = 1

        if dots is not None:

            dx = x - dots[:,0]
            dy = y - dots[:,1]

            d = np.sqrt((np.square(dx)+np.square(dy)))
            diff = d + np.min(r+dots[:,2])
            # dx = (x-point[0])
            # dy = (y-point[1])
            # d = math.sqrt((dy*dy)+(dx*dx))

            if not np.argmin(d>(allowable_intersection*(r+dots[:,2]))):
                print(f'Percent of Dots: {(i / num_dots) * 100}%')
                dots = np.vstack((dots,[x, y, r]))
                i+=1

                yield run, f'\n\tM {x}, {y}\n\tm -{r}, 0 a {r},{r} 0 1,0 {two_r},0\n\ta {r},{r} 0 1,0 -{two_r},0\n'
            else:
                yield -1, f'\n\tM {x}, {y}\n\tm -{r}, 0 a {r},{r} 0 1,0 {two_r},0\n\ta {r},{r} 0 1,0 -{two_r},0\n'
        else:
            dots = np.array([[x, y, r]])
            i += 1
            yield run, f'\n\tM {x}, {y}\n\tm -{r}, 0 a {r},{r} 0 1,0 {two_r},0\n\ta {r},{r} 0 1,0 -{two_r},0\n'
        # f'<circle cx="{x}mm" cy="{y}mm" r="{r}mm" />\n'
        # f'<path\n\td="\n\tM {x}, {y}\n\tm -{r}, 0 a {r},{r} 0 1,0 {two_r},0\n\ta {r},{r} 0 1,0 -{two_r},0\n"\n/>'


def browseFile(dir=False, types=(('All Files', "*.*"),)):
    root = tk.Tk()
    root.withdraw()
    if dir:
        file_path = filedialog.askdirectory(title="Test File Location")
    else:
        file_path = filedialog.askopenfilename(title="Select File", filetypes=types)
    return file_path


if __name__ == '__main__':
    # doc = ezdxf.readfile(r'C:\Users\jbrzostowski\Desktop\Cardif_heatsink_Etch_outline.dxf')
    # msp = doc.modelspace()
    # auditor = doc.audit()
    # fig = plt.figure()
    # ax = fig.add_axes([0, 0, 1, 1])
    # ctx = RenderContext(doc)
    # ctx.set_current_layout(msp)
    # # ctx.current_layout.set_colors(bg='#FFFFFF')
    #
    # out = MatplotlibBackend(ax)
    # Frontend(ctx, out).draw_layout(msp, finalize=True)
    #
    # plt.show()

    sensors = ['1M','2M','12M']
    desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
    filepath = os.path.join(desktop, 'DIC Pattern Outputs')
    # r"C:\Users\jbrzostowski\Desktop\Hinge Process"
    if os.path.exists(filepath) == False:
        os.mkdir(filepath)

    now = datetime.now()
    date_time = now.strftime("%Y_%m_%d_%H_%M_%S")
    #
    sensor = None
    while sensor is None:
        sensor = input("Enter Sensor Size:\n(1) 1M (S-Series)\n(2) 2M (R-Series)\n(3) 12M (Aramis)\n>> ")
        if sensor not in ['1','2','3','1M','2M','12M']:
            print('Input not valid. Please select again')

    height = 43
    width = 42
    if sensor == "3":
        sensor_width = 4096
        sensor_height = 3000
    elif sensor == '1':
        sensor_width = 1024
        sensor_height = 1024
    elif sensor == '2':
        sensor_width = 2048
        sensor_height = 2048

    measuring_volume = None
    measuring_volume = int(input("Enter Measuring Volume in mm\n>> "))

    dot_max = 5 * (measuring_volume/sensor_width)
    dot_min = 3 * (measuring_volume/sensor_width)
    # dot_max = .5
    # dot_min = .3
    filename = f'{sensors[int(sensor)-1]}_{measuring_volume}mm_measuring_volume_' + date_time + '.svg'
    file = os.path.join(filepath,filename)
    with open(file,'a') as f:
        # f.writelines('<?xml version="1.0" standalone="no"?>\n'
        #               '<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN"\n "">\n'
        #               f'<svg width="{width}mm" height="{height}mm" version="1.1"\n'
        #               'xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">"\n<path\nd="')
        f.writelines('<?xml version="1.0" standalone="no"?>\n'
                      '<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN"\n "">\n'
                      f'<svg width="{measuring_volume}mm" height="{measuring_volume}mm" viewBox="{0} {0} {measuring_volume} {measuring_volume}"\n'
                      'xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">"\n<path\nd="')
        gen = circleGenerator(measuring_volume,measuring_volume,dot_min,dot_max)

        for run, string in gen:
            if run == 0:
                f.writelines(string)
            elif run == -1:
                pass
            else:
               gen.close()
        f.writelines('"/>\n</svg>')