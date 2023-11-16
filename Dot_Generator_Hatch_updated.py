import ezdxf

import matplotlib.pyplot as plt
import numpy as np
import os
from datetime import datetime
import random
import math
import tkinter as tk
from tkinter import filedialog
import platform

from cad_to_shapely import dxf,utils
import shapely

PERCENT_COVERAGE = 0.425
ALLOWABLE_INTERSECTION = 1.1

RANDOMIZE_SPECKLE = False

if platform.system() == 'Windows':
    desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
else:
    desktop = os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop')
filepath = os.path.join(desktop, 'DIC PATTERN OUTPUTS')
# r"C:\Users\jbrzostowski\Desktop\Hinge Process"
if os.path.exists(filepath) == False:
    os.mkdir(filepath)
PARENT_DIRECTORY = filepath



def dxf2pattern(polygons,filename, dot_size_min: float, dot_size_max: float):

    dot_ave = (dot_size_min +dot_size_max)/2
    dot_area = math.pi *((dot_max/2)**2)
    # step = round(random.uniform(0,height),2)

    i = 0

    offset_polygons = []
    for p in polygons:
        buff = -1.5*(dot_size_max/2)
        offset_polygons.append(p.buffer(buff))
        x, y = p.exterior.xy

    new = utils.find_holes(polygons)
    new_offsets = utils.find_holes(offset_polygons)

    x, y = new.exterior.xy
    plt.plot(x, y, 'b')
    exterior_verts = []
    for idx, xal in enumerate(new.exterior.xy[0]):
        exterior_verts.append((new.exterior.xy[0][idx], new.exterior.xy[1][idx]))

    x, y = new_offsets.exterior.xy

    plt.plot(x, y, 'r')

    # plt.show()
    doc = ezdxf.new("R2018")
    hatch = doc.modelspace().add_hatch(
        color=1,
        dxfattribs={
            "hatch_style": ezdxf.const.HATCH_STYLE_NESTED,
            # 0 = nested: ezdxf.const.HATCH_STYLE_NESTED
            # 1 = outer: ezdxf.const.HATCH_STYLE_OUTERMOST
            # 2 = ignore: ezdxf.const.HATCH_STYLE_IGNORE
        },
    )
    hatch.paths.add_polyline_path(
        exterior_verts, is_closed=True,
        flags=ezdxf.const.BOUNDARY_PATH_EXTERNAL
    )

    for idx, hole in enumerate(new.interiors):
        interior_verts = []
        x, y = hole.xy
        plt.plot(x, y, 'b')

        x, y = new_offsets.interiors[idx].xy
        plt.plot(x, y, 'r')
        for idx, xal in enumerate(hole.xy[0]):
            interior_verts.append((hole.xy[0][idx], hole.xy[1][idx]))

        hatch.paths.add_polyline_path(
            interior_verts,
            is_closed=True,
            flags=ezdxf.const.BOUNDARY_PATH_OUTERMOST,
        )
    plt.show()
    edge_path = []

    num_dots = int((new_offsets.area / dot_area) * PERCENT_COVERAGE)
    new_polygon = None
    r_max = dot_size_max/2
    dots = None
    # interiors = list(new_offsets.interiors)
    while i < num_dots:
        try:
            if not RANDOMIZE_SPECKLE:
                # r = (round(random.uniform(dot_size_min,dot_size_max),3))/2
                r = round((dot_size_max / 2), 3)
            else:
                r = round((dot_size_max/2),3)
            p = utils.point_in_polygon(new_offsets,limit=1000000)
            x, y = p.xy

            x = round(x[0],5)
            y = round(y[0],5)
            if dots is None:
                dots = np.array([[x, y, r]])
                i += 1
                edge_path.append(hatch.paths.add_edge_path(flags=ezdxf.const.BOUNDARY_PATH_DEFAULT))
                edge_path[-1].add_arc(
                    center=(x, y),
                    radius=r,
                    start_angle=0,
                    end_angle=360
                )

                print(f'{i} out of {num_dots}')
                continue

            dx = x - dots[:,0]
            dy = y - dots[:,1]

            d = np.sqrt((np.square(dx)+np.square(dy)))
            diff = d + np.min(r+dots[:,2])


            if all(d>(ALLOWABLE_INTERSECTION*(r_max+r_max))):
                dots = np.vstack((dots, [x, y, r]))

                i += 1
                edge_path.append(hatch.paths.add_edge_path(flags=ezdxf.const.BOUNDARY_PATH_DEFAULT))
                edge_path[-1].add_arc(
                    center=(x, y),
                    radius=r,
                    start_angle=0,
                    end_angle=360
                )

                print(f'{i} out of {num_dots}')
        except KeyboardInterrupt:
            i = num_dots + 10


    filename = filename + '_' + date_time + '.dxf'
    file = os.path.join(PARENT_DIRECTORY,filename)
    doc.saveas(file)


def browseFile(dir=False, types=(('All Files', "*.*"),)):
    root = tk.Tk()

    root.withdraw()
    root.attributes("-topmost", True)

    if dir:
        file_path = filedialog.askdirectory(title="Test File Location")
    else:
        file_path = filedialog.askopenfilename(title="Select File", filetypes=types)
    return file_path


if __name__ == '__main__':


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


    choice =None

    while choice == None:
        choice = input('Are you loading an existing DXF outline? [y/n]')
        if choice in ['y','Y','yes']:
            choice = True
        elif choice in ['n','N','no']:
            choice = False
            doc = ezdxf.new("R12") ## R2018

        if choice:
            dxf_filepath = browseFile(False,types=(('DXF', "*.dxf*"),))
            # outline = ezdxf.readfile(outline_file)
            filename = os.path.basename(dxf_filepath)[:-4]
            my_dxf = dxf.DxfImporter(dxf_filepath)
            my_dxf.process(spline_delta=0.01)
            my_dxf.cleanup()

            polygons = my_dxf.polygons
            dxf2pattern(polygons,filename=filename,dot_size_max=dot_max,dot_size_min=dot_min)


        else:
            x_width = int(input("Enter the width of desired pattern in mm: "))
            y_height = int(input("Enter the height of desired pattern in mm: "))
            # rectangle = shapely.geometry.box(0, 0, x_width, y_height)
            rectangle = shapely.geometry.Polygon([(0, 0), (x_width, 0), (x_width, y_height),(0,y_height)])
            dxf2pattern([rectangle],filename= f'{measuring_volume}MV_{x_width}mmX{y_height}mm', dot_size_max=dot_max, dot_size_min=dot_min)







