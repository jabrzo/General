import ezdxf
from ezdxf import bbox
from ezdxf.addons.drawing.matplotlib import MatplotlibBackend
from ezdxf.addons.drawing import Frontend, RenderContext
import matplotlib.pyplot as plt
import numpy as np
import os
from datetime import datetime
import random
import math
import tkinter as tk
from tkinter import filedialog
import matplotlib.path as mpltPath
from ezdxf.addons import Importer

PERCENT_COVERAGE = 0.45
ALLOWABLE_INTERSECTION = .95
PARENT_DIRECTORY =r'G:\Shared drives\AR DVE\AR ME DVE\VR DVE\Cardiff\DIC\Patterns'

def checkArea():
    pass

def generateEdgePaths(hatch,width: float,height: float, dot_size_min: float,dot_size_max: float):

    area = height*width
    dot_ave = (dot_size_min +dot_size_max)/2
    dot_area = math.pi * ((dot_ave / 2) * (dot_ave / 2))
    step = round(random.uniform(0, height), 2)
    num_dots =(area/dot_area)*0.40


    return

# def circleGenerator(width: float,height: float, dot_size_min: float,dot_size_max: float):
def circleGenerator(x_min: float, x_max: float,y_min: float, y_max: float, dot_size_min: float, dot_size_max: float):
    width = x_max - x_min
    height = y_max - y_min
    area = height*width
    dot_ave = (dot_size_min +dot_size_max)/2

    dot_area = math.pi *((dot_ave/2)*(dot_ave/2))
    step = round(random.uniform(0,height),2)
    row = step
    num_dots = int((area/dot_area)*PERCENT_COVERAGE)
    dots = None
    i = 0
    run = 0

    x_bins = np.linspace(0,width,num=20)
    y_bins = np.linspace(0, height, num=20)

    x_min = x_min + (dot_max)*1.05
    y_min = y_min + dot_max*1.05
    x_max = x_max -(dot_max*1.05)
    y_max = y_max-(dot_max**1.05)


    while True:
        try:
            r = (round(random.uniform(dot_size_min,dot_size_max),2))/2
            y = round(random.uniform(y_min,y_max),2)
            x = round(random.uniform(x_min,x_max), 2)

            two_r = 2 * r

            # if i > num_dots*.75:
            #     ALLOWABLE_INTERSECTION = 1.01
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

                if not np.argmin(d>(ALLOWABLE_INTERSECTION*(r+dots[:,2]))):
                    print(f'Percent of Dots: {round((i / num_dots) * 100,1)}%')
                    dots = np.vstack((dots,[x, y, r]))
                    i+=1

                    yield run,i, x, y, r
                else:
                    yield -1,i, x, y, r
            else:
                dots = np.array([[x, y, r]])
                i += 1


        except KeyboardInterrupt:
            break
        yield run, i, x, y, r
        # f'<circle cx="{x}mm" cy="{y}mm" r="{r}mm" />\n'
        # f'<path\n\td="\n\tM {x}, {y}\n\tm -{r}, 0 a {r},{r} 0 1,0 {two_r},0\n\ta {r},{r} 0 1,0 -{two_r},0\n"\n/>'


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


    choice =None
    doc = ezdxf.new("R2018")

    while choice == None:
        choice = input('Are you loading an existing DXF outline or hatch? [y/n]')
        if choice in ['y','Y','yes']:
            choice = True
        elif choice in ['n','N','no']:
            choice = False

        if choice:
            outline_file = browseFile(False,types=(('DXF', "*.dxf*"),))
            outline = ezdxf.readfile(outline_file)

            auditor = outline.audit()
            fig = plt.figure()
            ax = fig.add_axes([0, 0, 1, 1])
            ctx = RenderContext(outline)
            ctx.set_current_layout(outline.modelspace())
            # ctx.current_layout.set_colors(bg='#FFFFFF')


            out = MatplotlibBackend(ax)
            Frontend(ctx, out).draw_layout(outline.modelspace(), finalize=True)

            plt.show()
            bounding_box = bbox.extents(outline.modelspace())
            x_min = bounding_box.extmin[0]
            x_max = bounding_box.extmax[0]
            y_min = bounding_box.extmin[1]
            y_max = bounding_box.extmax[1]

            # query source entities
            if outline.modelspace().query("HATCH").entities != []:
                importer = Importer(outline, doc)
                importer.import_modelspace()
                tblock = doc.blocks.new('SOURCE_ENTS')
                ents = outline.modelspace().query("HATCH")

                importer.import_entities(ents, tblock)

                hatch = doc.modelspace().query("HATCH").entities[0]
                hatch.dxf.hatch_style = ezdxf.const.HATCH_STYLE_NESTED

            else:
                tblock = doc.blocks.new('SOURCE_ENTS')
                ents = outline.modelspace().query("LINE ARC CIRCLE")
                lines = outline.modelspace().query("LINE").entities
                arcs = outline.modelspace().query("ARC").entities
                circles = outline.modelspace().query("CIRCLE").entities
                # edge_path = []
                hatch = doc.modelspace().add_hatch(
                    color=7,
                    dxfattribs={
                        "hatch_style": ezdxf.const.HATCH_STYLE_NESTED,
                        # 0 = nested: ezdxf.const.HATCH_STYLE_NESTED
                        # 1 = outer: ezdxf.const.HATCH_STYLE_OUTERMOST
                        # 2 = ignore: ezdxf.const.HATCH_STYLE_IGNORE
                    },
                )

                bound_path = (hatch.paths.add_edge_path(flags=ezdxf.const.BOUNDARY_PATH_DEFAULT))

                for x in lines:
                    start_x = x.dxf.start[0]
                    start_y = x.dxf.start[1]
                    end_x = x.dxf.end[0]
                    end_y = x.dxf.end[1]

                    bound_path.add_line(
                        start=(start_x, start_y),
                        end=(end_x, end_y)
                    )

                for x in arcs:
                    center_x = x.dxf.center[0]
                    center_y = x.dxf.center[1]

                    bound_path.add_arc(
                        center=(center_x, center_y),
                        radius=x.dxf.radius,
                        start_angle=x.dxf.start_angle,
                        end_angle=x.dxf.end_angle

                    )

                for x in circles:
                    center_x = x.dxf.center[0]
                    center_y = x.dxf.center[1]

                    bound_path.add_arc(
                        center=(center_x, center_y),
                        radius=x.dxf.radius,
                        start_angle=0,
                        end_angle=360

                    )
        else:
            x_width = int(input("Enter the width of desired pattern in mm: "))
            y_height = int(input("Enter the height of desired pattern in mm: "))
            hatch = doc.modelspace().add_hatch(
                color=7,
                dxfattribs={
                    "hatch_style": ezdxf.const.HATCH_STYLE_NESTED,
                    # 0 = nested: ezdxf.const.HATCH_STYLE_NESTED
                    # 1 = outer: ezdxf.const.HATCH_STYLE_OUTERMOST
                    # 2 = ignore: ezdxf.const.HATCH_STYLE_IGNORE
                },
            )

            hatch.paths.add_polyline_path(
                [(0, 0), (x_width, 0), (x_width, y_height), (0, y_height)],
                is_closed=True,
                flags=ezdxf.const.BOUNDARY_PATH_EXTERNAL,
            )

            x_min = 0
            x_max = x_width
            y_min = 0
            y_max = y_height

       # import source entities into target block





    edge_path = []

    filename = f'{sensors[int(sensor)-1]}_{measuring_volume}mm_measuring_volume_' + date_time + '.dxf'
    file = os.path.join(filepath,filename)
    gen = circleGenerator(x_min,x_max,y_min,y_max,dot_min,dot_max)

    try:
        for run,idx, x,y,r in gen:

            if run == 0:

                # print(f'x{x}; y{y}; r{r}')
                edge_path.append(hatch.paths.add_edge_path(flags=ezdxf.const.BOUNDARY_PATH_DEFAULT))
                edge_path[-1].add_arc(
                    center=(x, y),
                    radius=r,
                    start_angle=0,
                    end_angle=360
                )


            # elif run == -1:
            #     edge_path[-1].add_arc(
            #         center=(x, y),
            #         radius=r,
            #         start_angle=0,
            #         end_angle=360
            #     )
            elif run == 1:

                doc.saveas(os.path.join(PARENT_DIRECTORY,filename))
                gen.close()

    except KeyboardInterrupt:
            doc.saveas(os.path.join(PARENT_DIRECTORY, filename))
            gen.close()

