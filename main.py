import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import math
from valve import Valve

# Main Window Creation:
app = ctk.CTk()
app.geometry("1280x1020")
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
    print("hello")

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
sensor_grid_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

# DATA WE NEED:
sensor_titles = ["Valve 0", "Valve 1", "Valve 2", "Valve 3", "Valve 4", "Valve 5", "Valve 6", "Valve 7", "Valve 8", "Valve 9", "Valve 10", "Valve 11", "Valve 12", "Valve 13","Valve 14", "Tank 1", "Tank 2", "Tank 3", "Chamber 1", "Chamber 2"]

# Configuring the Window and defining grid (r x 5 grid):
row_count = math.ceil((len(sensor_titles)+1)/5)
for r in range(row_count):
    sensor_grid_frame.rowconfigure(r, weight=1)
for c in range(5):
    sensor_grid_frame.columnconfigure(c, weight=1)

# Widget Creation/Placement:
sensor_grid_frame_labels = {}

final_sensor = True
for r in range(5):
    for c in range(5):
        widgetCounter = r*5 + c

        if(widgetCounter < len(sensor_titles)):
            s_title_value = sensor_titles[widgetCounter]
        elif(widgetCounter == len(sensor_titles)):
            s_title_value = "ABORT"
        else:
            s_title_value = ""

        label = ctk.CTkLabel(sensor_grid_frame, text= s_title_value, fg_color="transparent")
        label.grid(row=r, column=c, padx=5, pady=5, sticky="n")
        sensor_grid_frame_labels[(r,c)] = label

        widgetCounter = widgetCounter + 1
    
    widgetCounter = widgetCounter + 1





# Runs the app
app.mainloop()


try:
    app.mainloop()
finally:
    main_shutdown()