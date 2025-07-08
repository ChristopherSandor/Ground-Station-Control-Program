from functools import partial
import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import math
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
    print("shutting down")

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
# SENSOR_PAGE CREATION WITH CONTENT:
sensor_grid_frame = ctk.CTkFrame(sensor_page, fg_color="transparent", corner_radius=8)
sensor_grid_frame.grid(row=0, column=0, sticky="nsew")

# DATA WE NEED:
data = Data("valvelist.txt","sensorlist.txt")
widget_items = data.getValve_list() + data.getSensor_list()
sensor_labels = {}

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

        s = obj.get_status()
        if(s==True):
            status="Open"
        elif(s==False):
            status="Closed"
        else:
            status="ERROR"
        
        status_label = ctk.CTkLabel(cell, text=status, fg_color="transparent", font=("Arial", 22), text_color="white")
        status_label.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="n")

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
        btn_open = ctk.CTkButton(cell, text="Open", command=partial(obj.open), fg_color="#477048", hover_color="#2D462D")
        btn_close = ctk.CTkButton(cell, text="Close", command=partial(obj.close), fg_color="#A54242", hover_color="#702D2D")

        btn_open .grid(row=2, column=0, sticky="nsew", padx=10, pady=10)
        btn_close.grid(row=2, column=1, sticky="nsew", padx=10, pady=10)

    # Sensor Judgement:
    elif isinstance(obj, Sensor):
        reading_label = ctk.CTkLabel(cell, text="---", font=("Arial", 22), text_color="#D8AE4D", fg_color="transparent")
        reading_label.grid(row=1, column=0, sticky="n")
        sensor_labels[obj] = reading_label

    # ABORT: 
    else:
        btn_abort = ctk.CTkButton(cell, text="ABORT", command=main_shutdown, font=("Arial", 36), fg_color="#A54242", hover_color="#702D2D")
        btn_abort.grid(row=0, column=0, sticky="nsew")



# Constant Loops (Updates Information)
def update_all_sensors():

    # Sensors
    for sensor, lbl in sensor_labels.items():
        
        val     = sensor.get_data()
        # 2) then compute the trend based on the fresh history
        verdict = sensor.trend()

        if verdict is True:
            lbl.configure(text_color="#477048")   # growing fast → green
        elif verdict is False:
            lbl.configure(text_color="#A54242")   # falling fast → red
        else:
            lbl.configure(text_color="#D8AE4D")   # small change → yellow


        lbl.configure(text=f"{val} PSI")

    app.after(100, update_all_sensors)
app.after(0, update_all_sensors)

# Runs the app
app.mainloop()

try:
    app.mainloop()
finally:
    main_shutdown()