import time
import math
from functools import partial

import customtkinter as ctk
import matplotlib.pyplot as plt
import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.patches import FancyBboxPatch

from valve import Valve
from sensor import Sensor
from data import Data

# Main Window Creation:
app = ctk.CTk()
app.geometry("1280x1020")
app.minsize(1200, 600)
app.title("Control App")
app.resizable(width=True, height=True)

# Theme of the Window/App:
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


#
#
#
# Program/Error Shutdown
def main_shutdown():
    for v in valve_list:
        v.close()

    print("All Valves Closed!")

def on_closing():
    main_shutdown()
    app.destroy()

app.protocol("WM_DELETE_WINDOW", on_closing)

#
#
#
# PAGE CREATION:

# Gives the whole page a 2x1 grid, which the gridframe lives in:
app.grid_rowconfigure(0, weight=0)
app.grid_rowconfigure(1, weight=1)
app.grid_columnconfigure(0, weight=1)

navbar = ctk.CTkFrame(app, fg_color="transparent", corner_radius=8)
sensor_page = ctk.CTkFrame(app, fg_color="transparent", corner_radius=8)
graph_page  = ctk.CTkFrame(app, fg_color="transparent", corner_radius=8)


# Attaches these two to the page:
# Within App ==> NavBar (r=0, c=0)
# Within App ==> sensor_page (r=1, c=0) 
# Within App ==> graph_page (r=1, c=0)

# Grids each Frame to its parents Row and Col then defines its internal row and col

# 1x1
navbar.grid(row=0, column=0, sticky="ew") 
navbar.grid_rowconfigure(0, weight=1)
navbar.grid_columnconfigure(0, weight=1)

# 1x1
sensor_page.grid(row=1, column=0, sticky="nsew")
sensor_page.grid_rowconfigure(0, weight=1)
sensor_page.grid_columnconfigure(0, weight=1)

# 1x1
graph_page.grid(row=1, column=0, sticky="nsew")
graph_page.grid_rowconfigure(0, weight=1)
graph_page.grid_columnconfigure(0, weight=1)

# Auto Hides Other Pages:
graph_page.grid_remove()

#
#
#
# NAVBAR CREATION WITH CONTENT:
navbar_grid_frame = ctk.CTkFrame(navbar, fg_color="transparent", corner_radius=8)
navbar_grid_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

navbar_grid_frame.rowconfigure(0, weight=1)
navbar_grid_frame.columnconfigure(0, weight=1)
navbar_grid_frame.columnconfigure(1, weight=1)

# Button Functions:
def toggle_sensor_page():
    graph_page.grid_remove()
    sensor_page.grid() 

def toggle_graph_page():
    sensor_page.grid_remove()
    graph_page.grid()

# Button Creations:
navbar_sensor_button = ctk.CTkButton(navbar_grid_frame, text="Sensor Page", fg_color="#627C85", command=toggle_sensor_page)
navbar_graph_buttom = ctk.CTkButton(navbar_grid_frame, text="Graph Page", fg_color="#627C85", command=toggle_graph_page)

# Button Griding:
navbar_sensor_button.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
navbar_graph_buttom.grid(row=0, column=1, sticky="ew", padx=5, pady=5)

# 
# 
# 
# DATA WE NEED:

# All Data:
data = Data("valvelist.txt","sensorlist.txt")
valve_list = data.getValve_list()
sensor_list = data.getSensor_list()

# Sensor Page:
widget_items = valve_list + sensor_list
sensor_labels = {}
valve_labels = {}

#  Graph page:
time_data = []
sensor_history = { sensor: [] for sensor in sensor_list }
graph_list = {}
plots = {}
start_time = time.time()
sensor_hist = {s: {"t": [], "v": []} for s in sensor_list}


#
#
#
# SENSOR_PAGE CREATION WITH CONTENT:
sensor_grid_frame = ctk.CTkFrame(sensor_page, fg_color="transparent", corner_radius=8)
sensor_grid_frame.grid(row=0, column=0, sticky="nsew")

# Configuring the Window and defining grid (r x 5 grid) which includes the ABORT Button:
col_count = 5
row_count = math.ceil((len(widget_items) + 1)/col_count)
for r in range(row_count):
    sensor_grid_frame.rowconfigure(r, weight=1)
for c in range(col_count):
    sensor_grid_frame.columnconfigure(c, weight=1)

# Placing Widgets (Valves, Sensors and ABORT)

for idx, obj in enumerate(widget_items + ["ABORT"]):
    r = idx // col_count
    c = idx % col_count

    # Grid in Cell formating:
    if not(isinstance(obj, Valve)) and not(isinstance(obj, Sensor)):
        cell = ctk.CTkFrame(sensor_grid_frame, fg_color="transparent")
    else:
        cell = ctk.CTkFrame(sensor_grid_frame, fg_color="#333333")

    cell.grid(row=r, column=c, padx=15, pady=15, sticky="nsew")
    cell.grid_rowconfigure(0, weight=1)

    # Title Judgement:
    if isinstance(obj, Valve):
        cell.grid_rowconfigure(1, weight=1)
        cell.grid_rowconfigure(2, weight=0)
        cell.grid_columnconfigure(0, weight=1, uniform="valve_cols")
        cell.grid_columnconfigure(1, weight=1, uniform="valve_cols")

        title = obj.get_valve_name()
        label = ctk.CTkLabel(cell, text = title, fg_color="transparent", font=("Arial", 24), text_color="white")
        label.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="n")

    elif isinstance(obj, Sensor):
        cell.grid_rowconfigure(1, weight=1)
        cell.grid_columnconfigure(0, weight=1)
        title = obj.sensor_name
        label = ctk.CTkLabel(cell, text = title, fg_color="transparent", font=("Arial", 24), text_color="white")
        label.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="n")
    else:
        title = None
        cell.grid_columnconfigure(0, weight=1)

    # Valve Judgement:
    if isinstance(obj, Valve):

        # Buttons
        btn_open = ctk.CTkButton(cell, text="Open", command=partial(obj.open), fg_color="#477048", hover_color="#2D462D")
        btn_close = ctk.CTkButton(cell, text="Close", command=partial(obj.close), fg_color="#A54242", hover_color="#702D2D")

        btn_open .grid(row=2, column=0, sticky="nsew", padx=10, pady=10)
        btn_close.grid(row=2, column=1, sticky="nsew", padx=10, pady=10)

        # Label (Close/Open)
        
        status_label = ctk.CTkLabel(cell, text=obj.get_status(), fg_color="transparent", font=("Arial", 22, "bold"), text_color="white")
        status_label.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="n")

        valve_labels[obj] = status_label

    # Sensor Judgement:
    elif isinstance(obj, Sensor):
        reading_label = ctk.CTkLabel(cell, text="---", font=("Arial", 22), text_color="#D8AE4D", fg_color="transparent")
        reading_label.grid(row=1, column=0, sticky="n")
        sensor_labels[obj] = reading_label

    # ABORT: 
    else:
        btn_abort = ctk.CTkButton(cell, text="ABORT", command=main_shutdown, font=("Arial", 36), fg_color="#A54242", hover_color="#702D2D")
        btn_abort.grid(row=0, column=0, sticky="nsew")

#
#
# GRAPH_PAGE CREATION WITH CONTENT:
graph_page_grid_frame = ctk.CTkFrame(graph_page, fg_color="transparent", corner_radius=8)
graph_page_grid_frame.grid(row=0, column=0, sticky="nsew")

col_count_graph = 2
row_count_graph = math.ceil(len(sensor_list)/col_count_graph)

for r in range(row_count_graph):
    graph_page_grid_frame.rowconfigure(r, weight=1)
for c in range(col_count_graph):
    graph_page_grid_frame.columnconfigure(c, weight=1, uniform="graphs")


for idx, sensor in enumerate(sensor_list):
    r = idx // col_count_graph
    c = idx % col_count_graph

    cell = ctk.CTkFrame(graph_page_grid_frame, fg_color="#2E2E2E", corner_radius=8)
    cell.grid(row=r, column=c, padx=15, pady=15, sticky="nsew")
    cell.grid_rowconfigure(0, weight=1)
    cell.grid_columnconfigure(0, weight=1)

    fig = Figure(figsize=(4, 3), dpi=110,  facecolor="#2E2E2E")
    fig.subplots_adjust(bottom=0.2)
    ax = fig.add_subplot(111, facecolor="#3A3A3A")

    
    ax.set_title(sensor.sensor_name)
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Pressure (PSI)")
    line, = ax.plot([], [], lw=2)

    canvas = FigureCanvasTkAgg(fig, master=cell)
    canvas.draw()
    canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew")

    plots[sensor] = {"line": line, "ax": ax, "canvas": canvas}




# 
# 
# 
# Global Loops (Updates Information)
def update_all_sensors():

    # Sensors
    for sensor, lbl in sensor_labels.items():
        
        val = sensor.get_data()
        verdict = sensor.trend()

        if verdict is True:
            lbl.configure(text_color="#477048")   # growing fast → green
        elif verdict is False:
            lbl.configure(text_color="#A54242")   # falling fast → red
        else:
            lbl.configure(text_color="#D8AE4D")   # small change → yellow

        lbl.configure(text=f"{val} PSI")

    # Valves
    for valve, lbl in valve_labels.items():

        state = valve.get_status()
        lbl.configure(text = state)

        if(state == "Open"):
            lbl.configure(text_color="#477048")
        else:
            lbl.configure(text_color="#A54242")

    t = time.time() - start_time
    for sensor in sensor_list:
        val = sensor.get_data()
        hist = sensor_hist[sensor]
        hist["t"].append(t)
        hist["v"].append(val)

        plot = plots[sensor]
        plot["line"].set_data(hist["t"], hist["v"])
        plot["ax"].relim()
        plot["ax"].autoscale_view()
        plot["canvas"].draw()



    app.after(800, update_all_sensors)
app.after(0, update_all_sensors)

# 
# 
# 
# Runs the app
app.mainloop()

try:
    app.mainloop()
finally:
    main_shutdown()