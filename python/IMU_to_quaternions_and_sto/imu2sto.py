#pyinstaller --onefile --noconsole --add-data "C:\Users\Usuario\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.10_qbz5n2kfra8p0\LocalCache\local-packages\Python310\site-packages\ahrs\utils\WMM2020\WMM.COF;ahrs\utils\WMM2020" --hidden-import=xml.etree.ElementTree --hidden-import=xml.dom.minidom --hidden-import=tkinter --hidden-import=filedialog --hidden-import=ttk --hidden-import=numpy --hidden-import=pandas --hidden-import=os --hidden-import=webbrowser --hidden-import=scipy.spatial.transform.Rotation --hidden-import=subprocess --hidden-import=matplotlib.pyplot --hidden-import=ahrs.filters --hidden-import=Vec3 --hidden-import=datetime --hidden-import=scipy.signal imu2sto.py

import xml.etree.ElementTree as ET
import xml.dom.minidom
import tkinter as tk
from tkinter import filedialog, ttk  # import the filedialog and ttk modules
import numpy as np
from scipy.spatial.transform import Rotation
from scipy import signal
# import ahrs
import pandas as pd
import matplotlib.pyplot as plt
import os
import subprocess
import webbrowser
from datetime import datetime
# To install ahrs.filters use pip install AHRS
# website https://pypi.org/project/AHRS/
from ahrs.filters import Madgwick
# Opensim libraries to create the .mov files from the .sto files
# To install the Opensim libraries follow instructions: https://simtk-confluence.stanford.edu:8443/display/OpenSim/Conda+Package
# It is possible to donwload the conda package (check Python and Numpy version) from https://anaconda.org/opensim-org/opensim/files and then
# Install the downloaded files using: conda install "location\name_of_file"

# Opensim libraries not need if .mot files is not create from the .sto files (adding the Opensim model file)
#import opensim as osim
#from opensim import Vec3

madgwick = Madgwick()

# label_5 displays the results and errors information after using the Run button
label_global_results = None
num_files = 0
files_path = ""
frequency = "52"
font_text = ("Helvetica", 8)
font_text2 = ("Arial", 9)
files = []
numrow = []
widgets = []  # create an empty list for storing the widgets
button_list_acc = [] # create an empty list for storing the widgets button print acceleration file
button_list_gyr = [] # create an empty list for storing the widgets button print gyroscope file
filenames = []  
selected_files = []  # create an empty list for storing the selected file names
selected_parts = []  
entered_values_0_a = []
entered_values_rot_x = []
entered_values_rot_y = []
entered_values_rot_z = []
entered_values_1_a = []
entered_values_1_b = []
entered_values_1_c = []
entered_values_2_a = []
entered_values_2_b = []
entered_values_2_c = []
entered_values_3_a = []
entered_values_3_b = []
entered_values_3_c = []

# List of the elements that can be selected with the combobox widget
placements_list = ["torso", "pelvis", "femur_r", "femur_l", "tibia_r", "tibia_l", "calcn_r", "calcn_l", "patella_r", "patella_l", "talus_r", "talus_l", "toes_r", "toes_l", "humerus_r", "humerus_l", "ulna_r", "ulna_l", "radius_r", "radius_l", "hand_r", "hand_l"]

# Create the main window
window = tk.Tk()
window.geometry("1380x620")
# Set the title of the window
window.title("imu2sto - marra610@student.otago.ac.nz")
# Remove the tkinter icon on the title bar
# window.wm_iconbitmap('')
# window.iconbitmap('')

# Class for storing the information for each file
class File:
    def __init__(
        self, name, frequency, file_a, part, rot_x, rot_y, rot_z, acceleration_a, acceleration_b,acceleration_c,velocity_a, velocity_b, velocity_c, magnetometer_a, magnetometer_b, magnetometer_c
    ):
        self.name = name
        self.frequency = frequency
        self.file_a = file_a
        self.part = part
        self.rot_x = rot_x
        self.rot_y = rot_y
        self.rot_z = rot_z
        self.acceleration_a = acceleration_a
        self.acceleration_b = acceleration_b
        self.acceleration_c = acceleration_c
        self.velocity_a = velocity_a
        self.velocity_b = velocity_b
        self.velocity_c = velocity_c
        self.magnetometer_a = magnetometer_a
        self.magnetometer_b = magnetometer_b
        self.magnetometer_c = magnetometer_c

# "Save..." button function for saving the information to an XML file
def save_xml():
    root = ET.Element("root")

    # Add a element for each file
    for i in range(num_files):
        if i >= len(widgets):  # if the list does not have enough elements
            break  # stop iterating through the list
        # Unpack variables
        (entry_0, entry_0_a, combobox, entry_rot_x, entry_rot_y, entry_rot_z, label_1, entry_1_a, entry_1_b, entry_1_c,label_2, entry_2_a, entry_2_b, entry_2_c,label_3, entry_3_a, entry_3_b, entry_3_c,label_4) = widgets[i]
        
        # Create a "file" element and add it to the root element
        file_element = ET.SubElement(root, "file")
        
        # Add subelements to the "file" element
        ET.SubElement(file_element, "name").text = files_path+"/"+entry_0.get()
        ET.SubElement(file_element, "frequency").text = entry_frequency.get()
        ET.SubElement(file_element, "file_a").text = entry_0_a.get()
        ET.SubElement(file_element, "part").text = combobox.get()
        ET.SubElement(file_element, "rot_x").text = entry_rot_x.get()
        ET.SubElement(file_element, "rot_y").text = entry_rot_y.get()
        ET.SubElement(file_element, "rot_z").text = entry_rot_z.get()
        ET.SubElement(file_element, "acceleration_a").text = entry_1_a.get()
        ET.SubElement(file_element, "acceleration_b").text = entry_1_b.get()
        ET.SubElement(file_element, "acceleration_c").text = entry_1_c.get()
        ET.SubElement(file_element, "velocity_a").text = entry_2_a.get()
        ET.SubElement(file_element, "velocity_b").text = entry_2_b.get()
        ET.SubElement(file_element, "velocity_c").text = entry_2_c.get()
        ET.SubElement(file_element, "magnetometer_a").text = entry_3_a.get()
        ET.SubElement(file_element, "magnetometer_b").text = entry_3_b.get()
        ET.SubElement(file_element, "magnetometer_c").text = entry_3_c.get()

    # Write the XML tree to a file
    # Open a save file dialog to choose the file to save
    filepath = filedialog.asksaveasfilename(defaultextension=".xml")

    # Add the ".xml" extension to the filepath if it is not already present
    if not filepath.endswith(".xml"):
        filepath += ".xml"
    
    # Try to create the file in "x" mode (raises FileExistsError if file already exists)
    try:
        with open(filepath, "x") as f:
            xml_str = xml.dom.minidom.parseString(ET.tostring(root)).toprettyxml()
            f.write(xml_str)
    except FileExistsError:
        # File already exists, so we'll just overwrite it
        with open(filepath, "w") as f:
            xml_str = xml.dom.minidom.parseString(ET.tostring(root)).toprettyxml()
            f.write(xml_str)
 
# "Load..." button function for opening and parsing the XML file
def open_xml():
    global files, frequency
    files = []
    filepath = filedialog.askopenfilename(filetypes=[("XML Files", "*.xml")])
    
    # Clear the lists
    filenames.clear()
    entered_values_0_a.clear()
    entered_values_rot_x.clear()
    entered_values_rot_y.clear()
    entered_values_rot_z.clear()
    entered_values_1_a.clear()
    entered_values_1_b.clear()
    entered_values_1_c.clear()
    entered_values_2_a.clear()
    entered_values_2_b.clear()
    entered_values_2_c.clear()
    entered_values_3_a.clear()
    entered_values_3_b.clear()
    entered_values_3_c.clear()
    # Parse the XML file and create an XML tree
    tree = ET.parse(filepath)
    root = tree.getroot()
    global files_path
    # Iterate over the file elements in the XML tree
    for file_element in root.findall("file"):
        name_with_path = file_element.find("name").text
        frequency = file_element.find("frequency").text
        files_path = '/'.join(name_with_path.split("/")[:-1])
        name = name_with_path.split("/")[-1]    
        file_a = file_element.find("file_a").text
        part = file_element.find("part").text
        rot_x = file_element.find("rot_x").text
        rot_y = file_element.find("rot_y").text
        rot_z = file_element.find("rot_z").text
        acceleration_a = file_element.find("acceleration_a").text
        acceleration_b = file_element.find("acceleration_b").text
        acceleration_c = file_element.find("acceleration_c").text
        velocity_a = file_element.find("velocity_a").text
        velocity_b = file_element.find("velocity_b").text
        velocity_c = file_element.find("velocity_c").text
        magnetometer_a = file_element.find("magnetometer_a").text
        magnetometer_b = file_element.find("magnetometer_b").text
        magnetometer_c = file_element.find("magnetometer_c").text

        # Create a new file object with the information from the XML element
        file = File(name=name, frequency=frequency,file_a=file_a, part=part, rot_x=rot_x, rot_y=rot_y,rot_z=rot_z, acceleration_a=acceleration_a, acceleration_b=acceleration_b, acceleration_c=acceleration_c,
                    velocity_a=velocity_a, velocity_b=velocity_b, velocity_c=velocity_c,magnetometer_a=magnetometer_a, magnetometer_b=magnetometer_b,magnetometer_c=magnetometer_c)
        
        filenames.append(name_with_path)
        
        files.append(file)

    # Call update_widgets to display the information from the XML file
    update_widgets(files)

# Define a function display the information
def update_widgets(files):
    # Remove the results and errors label
    if label_global_results is not None and label_global_results.winfo_exists():
        label_global_results.destroy()

    global num_files, widgets, result_label  
    # Remove the existing widgets
    for widget in widgets:
        for subwidget in widget:
            subwidget.destroy()
    widgets.clear()  # clear the widgets list
    # Remove the plt acc and gyr buttons
    for button in button_list_acc:
        button.destroy()
    button_list_acc.clear()
    for button in button_list_gyr:
        button.destroy()
    button_list_gyr.clear()
    num_files = 0  # reset the number of files
    # Create a label, combobox, entry, check button, and label widget for each file
    for file in files:
        num_files += 1  # increment the number of files

        # Create a label widget for displaying the file name
        entry_0 = tk.Entry(window, width=13)
        entry_0.insert(0, file.name.split("/")[-1])
        entry_0.grid(row=num_files + 2, column=1)  

        # Create an entry widget for the number of IMU elements on each row of the file
        entry_0_a = tk.Entry(window, width=3, justify="center")
        entry_0_a.insert(0, file.file_a)  
        entry_0_a.grid(row=num_files+2, column=2)  
        
        # Create a combobox widget for placement selection
        combobox = ttk.Combobox(window, width =9,  values=placements_list)
        combobox.set(file.part)
        combobox.grid(row=num_files+2, column=3) 

        # Create an entry widget for the rotation in X-axis
        entry_rot_x = tk.Entry(window, width=3, justify="center")
        entry_rot_x.insert(0, file.rot_x)  
        entry_rot_x.grid(row=num_files+2, column=4) 

        # Create an entry widget for the rotation in Y-axis
        entry_rot_y = tk.Entry(window, width=3, justify="center")
        entry_rot_y.insert(0, file.rot_y)  
        entry_rot_y.grid(row=num_files+2, column=5) 

        # Create an entry widget for the rotation in Z-axis
        entry_rot_z = tk.Entry(window, width=3, justify="center")
        entry_rot_z.insert(0, file.rot_z)  
        entry_rot_z.grid(row=num_files+2, column=6)

        # Create a label widget for displaying the "acceleration" label
        label_1 = tk.Label(window, text="Acc.", width=6,font = font_text, justify="right")
        label_1.grid(row=num_files+2, column=7) 

        # Create entry widgets for entering the position and change of units of the acceleration 
        entry_1_a = tk.Entry(window, width=3, justify="center")
        entry_1_b = tk.Entry(window, width=7, justify="right")
        entry_1_c = tk.Entry(window, width=3, justify="center")
        entry_1_a.insert(0, file.acceleration_a)  
        entry_1_b.insert(0, file.acceleration_b)  
        entry_1_c.insert(0, file.acceleration_c)  
        entry_1_a.grid(row=num_files+2, column=8)  
        entry_1_b.grid(row=num_files+2, column=9) 
        entry_1_c.grid(row=num_files+2, column=10) 

        # Create a label widget for displaying the "angular velocity" label
        label_2 = tk.Label(window, text="Gyr.", width=6,font = font_text, justify="right")
        label_2.grid(row=num_files+2, column=11) 

        # Create entry widgets for entering the position and change of units of the angular velocity
        entry_2_a = tk.Entry(window, width=3, justify="center")
        entry_2_b = tk.Entry(window, width=7, justify="right")
        entry_2_c = tk.Entry(window, width=3, justify="center")
        entry_2_a.insert(0, file.velocity_a) 
        entry_2_b.insert(0, file.velocity_b) 
        entry_2_c.insert(0, file.velocity_c) 
        entry_2_a.grid(row=num_files+2, column=12)  
        entry_2_b.grid(row=num_files+2, column=13) 
        entry_2_c.grid(row=num_files+2, column=14)

        # Create a label widget for displaying the "magnetometer" label
        label_3 = tk.Label(window, text="Mag.", width=6,font = font_text, justify="right")
        label_3.grid(row=num_files+2, column=15)  

        # Create entry widgets for entering the position and change of units of the magnetometer
        entry_3_a = tk.Entry(window, width=3, justify="center")
        entry_3_b = tk.Entry(window, width=7, justify="right")
        entry_3_c = tk.Entry(window, width=3, justify="center")
        entry_3_a.insert(0, file.magnetometer_a)  
        entry_3_b.insert(0, file.magnetometer_b)  
        entry_3_c.insert(0, file.magnetometer_c)  
        entry_3_a.grid(row=num_files+2, column=16) 
        entry_3_b.grid(row=num_files+2, column=17)  
        entry_3_c.grid(row=num_files+2, column=18)  

        # Create a label widget for displaying the result of each file
        result_label = tk.Label(window, text="-", font=("Arial", 7), justify="left")
        result_label.grid(row=num_files+2, column=19)  

        # Display the frequency in the entry_frequency widget
        entry_frequency.delete(0, "end")
        entry_frequency.insert(0, frequency) 

        # Display the path in the entry_path widget
        entry_path.delete(0, "end")
        entry_path.insert(0, files_path)

        # Append the widgets to the list      
        widgets.append((entry_0,entry_0_a,combobox,entry_rot_x,entry_rot_y,entry_rot_z,label_1,entry_1_a,entry_1_b, entry_1_c,label_2, entry_2_a,entry_2_b,entry_2_c,label_3,entry_3_a,entry_3_b,entry_3_c,result_label))


# Function that applies the first entry widget values to the rest of the entry widgets
def apply_all():
    # Set the values for all rows except the first one
    if len(widgets) > 1:
        for i in range(1, len(widgets)):
            for j in [1,7, 8, 9,11, 12, 13, 15,16,17]:  # loop through the specified widgets in each row
                if isinstance(widgets[i][j], tk.Entry):  # if the widget is an Entry widget
                    widgets[i][j].delete(0, "end")  # delete the current value
                    widgets[i][j].insert(0, widgets[0][j].get())  # insert the new value

# "Select Files" button function for opening a file dialog and displaying the file names
def select_files():
    # Delete the global_results label if it exists
    if label_global_results is not None and label_global_results.winfo_exists():
        label_global_results.destroy()

    global num_files, widgets, files_path, files
    
    files_paths_names = filedialog.askopenfilenames()
    if files_paths_names:  # if the user selected at least one file
        for file_path_name in files_paths_names:
            file_full_name = file_path_name
            files_path = '/'.join(file_full_name.split("/")[:-1])
            file_name = file_full_name.split("/")[-1]
            filenames.append(file_full_name)  # append the file name to the filenames list
            index = files_paths_names.index(file_path_name)
            # Create the elements with the default values for each widget
            file = File(file_path_name, 52,1, placements_list[index], 0,0,0,1, 1,0, 4, 1,0, 7, 1,0)
            files.append(file)
        num_files += len(files_paths_names)  # increment the number of files
        # Update the widgets to display the information from the list of File objects
        update_widgets(files)

def delete_files():
    global widgets, filenames, files, button_list_acc, button_list_gyr

    # Delete each widget in the widgets list
    for row in widgets:
        for widget in row:
            widget.destroy()
    # Delete the global_results label if it exists
    if label_global_results is not None and label_global_results.winfo_exists():
        label_global_results.destroy()
    # Remove the plt acc and gyr buttons
    for button in button_list_acc:
        button.destroy()
    button_list_acc.clear()
    for button in button_list_gyr:
        button.destroy()
    button_list_gyr.clear()
    #path_label.config(text="")
    entry_frequency.delete(0, "end")
    entry_frequency.insert(0, "") 
    entry_path.delete(0, "end")
    entry_path.insert(0, "")
    window.geometry("1380x560")
    widgets = []
    filenames = []
    files = []


# "Run" button function for running the quaternion and .sto file creation code
def run_code():
    global label_global_results, result_label, widgets, files_path, widget_path, button_list_acc, button_list_gyr
    selected_files.clear()
    selected_parts.clear()
    entered_values_0_a.clear()
    entered_values_rot_x.clear()
    entered_values_rot_y.clear()
    entered_values_rot_z.clear()
    entered_values_1_a.clear()
    entered_values_1_b.clear()
    entered_values_1_c.clear()
    entered_values_2_a.clear()
    entered_values_2_b.clear()
    entered_values_2_c.clear()
    entered_values_3_a.clear()
    entered_values_3_b.clear()
    entered_values_3_c.clear()
    # Remove the plt acc and gyr buttons
    for button in button_list_acc:
        button.destroy()
    button_list_acc.clear()
    for button in button_list_gyr:
        button.destroy()
    button_list_gyr.clear()

    # Iterate over the widgets list
    for i, (entry_0, entry_0_a, combobox, entry_rot_x,entry_rot_y,entry_rot_z,_, entry_1_a, entry_1_b,entry_1_c, _, entry_2_a, entry_2_b, entry_2_c,_, entry_3_a, entry_3_b, entry_3_c,_) in enumerate(widgets):
        selected_files.append(entry_0.get())
        selected_parts.append(combobox.get())
        entered_values_0_a.append(entry_0_a.get())
        entered_values_rot_x.append(entry_rot_x.get())
        entered_values_rot_y.append(entry_rot_y.get())
        entered_values_rot_z.append(entry_rot_z.get())
        entered_values_1_a.append(entry_1_a.get())
        entered_values_1_b.append(entry_1_b.get())
        entered_values_1_c.append(entry_1_c.get())
        entered_values_2_a.append(entry_2_a.get())
        entered_values_2_b.append(entry_2_b.get())
        entered_values_2_c.append(entry_2_c.get())
        entered_values_3_a.append(entry_3_a.get())
        entered_values_3_b.append(entry_3_b.get())
        entered_values_3_c.append(entry_3_c.get())
    
    # lists of integers and floats for verification if the data inside the entry widgets is correct
    integer_lists = [entered_values_0_a, entered_values_1_a, entered_values_2_a]
    float_lists = [entered_values_1_b, entered_values_2_b]
    rotations_lists = [entered_values_rot_x, entered_values_rot_y, entered_values_rot_z]
    filters_lists = [entered_values_1_c, entered_values_2_c, entered_values_3_c]
    ok_start_running_code = True  # Variable for indicating if the code should run
    ok_continue_running_code = True  # Variable for indicating if the code should continue run
    errors = [] # list for storing the error messages
    warnings = [] # list for storing the warnings messages
    results = [] # list for storing the results messages
    # Default number of IMU data 3 acc + 3 gyr + 3 mag
    iterate_IMUs = 9
    last_element_row = 0
    if not (entry_frequency.get().isdigit()):
        errors.append("Error in entry Frequency value must be integer number")
        ok_start_running_code = False
        sampling_freq = 0
    else:
        frequency = entry_frequency.get()
        sampling_freq = float(frequency) 
    # Error not files selected
    if len(widgets) < 1:
        errors.append("Select files to Run the program")
        ok_start_running_code = False

    # Increase the window height if more than 6 files selected
    if len(widgets) > 6:
        height = (len(widgets)-7) * 45 + 560
        window.geometry(f"1380x{height}")

    # Error elements duplicated in the combobox
    if len(selected_parts) != len(set(selected_parts)):
        ok_start_running_code = False
        errors.append("Some placements are duplicated")

    # check if all values in the integer lists are integers
    for lst in integer_lists:
        for value in lst:
            if not (value.isdigit()):
                errors.append(f"Error in entry {lst} values must be integer numbers")
                ok_start_running_code = False 

    # check if all values in the float lists are floats
    for lst in float_lists:
        for val in lst:
            try:
                float(val)
            except ValueError:
                ok_start_running_code = False
                errors.append(f"Error in entry {lst} values must be float numbers")

    for index,val in enumerate(entered_values_3_a):
        if (val != ""):
            try:
                float(entered_values_3_b[index])
            except ValueError:
                    ok_start_running_code = False
                    errors.append(f"Error in entry {entered_values_3_b} values must be float numbers")

    # check if all values in the rotation lists are floats between -180 and 180
    for lst in rotations_lists:
        for val in lst:
            try:
                float_val = float(val)
                if float_val < -180 or float_val > 180:
                    ok_start_running_code = False
                    errors.append(f"Error in entry {lst}, values must be float numbers between -180 and 180")
            except ValueError:
                ok_start_running_code = False
                errors.append(f"Error in entry {lst}, values must be float numbers between -180 and 180")
    
    for lst in filters_lists:
        for val in lst:
            try:
                float_val = float(val)
                if float_val < 0 or float_val > sampling_freq:
                    ok_start_running_code = False
                    errors.append(f"Error in entry {lst}, values must be float numbers between 0 and the selected Frequency "+str(sampling_freq))
            except ValueError:
                ok_start_running_code = False
                errors.append(f"Error in entry {lst}, values must be float numbers between 0 and the selected Frequency "+str(sampling_freq))
    
    # check if the value in the magnetometer position is an integer or empty "" (empty indicates not magnetometer in the data)
    for value in entered_values_3_a:
        if value == "":
            # Changes the default number of IMU data to 6 = 3 acc + 3 gyr (no magnetometer present)
            iterate_IMUs = 6
        if not (value.isdigit() or value == ""):
            errors.append(f"Error in entry {entered_values_3_a} values must be integer numbers or left empty")
            ok_start_running_code = False 

    if ok_start_running_code:          
        # fusion of sensors placements
        if len(selected_parts) > 0:
            sensors_placement = selected_parts[0]+"_imu"
            if len(selected_parts) > 1:
                for i in range(len(selected_parts)-1):
                    sensors_placement = sensors_placement+"	"+selected_parts[i+1]+"_imu"
        # Start the list with the information that will be displayed in the global_result label
        results.append(" Placement: "+sensors_placement)  

        # List for IMU data rotated, if there is more than 1 IMU data on each row splitted in 1 IMU per row
        IMU=[]
        numrows=[]
        # List for quaternions
        Q=[]

        # Verify if the string in the entry widget "widget_path" exists and creates the directory if not and also check if there is an error in the string name before creating the new directory
        widget_path = entry_path.get()
        # if not os.path.isdir(widget_path):
        #     # widget_path is not a directory, use files_path instead
        #     widget_path = files_path
        #     results.append("Warning: First Failed to create selected directory, default directory used instead")
        #     # Display the path in the entry_path widget
        #     entry_path.delete(0, "end")
        #     entry_path.insert(0, files_path)
        # # At this point, widget_path is guaranteed to be a valid directory (or so we hope)
        try:
            if not os.path.exists(widget_path):
                # Folder does not exist, create it
                os.makedirs(widget_path)
        except Exception as e:
            # An error occurred while trying to create the directory
            # You can handle the error here
            warnings.append("Warning: Second Failed to create selected directory :"+e+" , default directory used instead")

        # Load the IMU files and Create the quaternions with the Madgwick orientation filter
        
        for i in range(len(selected_files)):
            
            # Check if the extension of the file is .txt or .csv before getting the data from the file
            file_name, file_extension = os.path.splitext(selected_files[i])
            if file_extension == ".txt":
                file_data = np.loadtxt(files_path+"/"+selected_files[i], delimiter=",")
            elif file_extension == ".csv":
                file_data = pd.read_csv(files_path+"/"+selected_files[i], header=None).values
            else:
                # Unsupported file type
                warnings.append("Warning: The data files must be .txt or .csv")
                ok_continue_running_code = False
            
            if entered_values_3_a[i] == "":
                # In case of "" in magnetometer entry detects if there are magnetometer data or not to iterate over 9 or 6 elements 
                if np.shape(file_data)[1] == ((6*(int(entered_values_0_a[i])-1))+(max(int(entered_values_1_a[i]),int(entered_values_2_a[i]))+2)):
                    iterate_IMUs = 6
                    last_element_row = ((6*(int(entered_values_0_a[i])-1))+(max(int(entered_values_1_a[i]),int(entered_values_2_a[i]))+2))
                elif np.shape(file_data)[1] == ((9*(int(entered_values_0_a[i])-1))+(max(int(entered_values_1_a[i]),int(entered_values_2_a[i]))+5)):
                    iterate_IMUs = 9
                    last_element_row = ((9*(int(entered_values_0_a[i])-1))+(max(int(entered_values_1_a[i]),int(entered_values_2_a[i]))+5))
            else:
                last_element_row = ((9*(int(entered_values_0_a[i])-1))+(max(int(entered_values_1_a[i]),int(entered_values_2_a[i]),int(entered_values_3_a[i]))+2))
            
            if np.shape(file_data)[1] < last_element_row:
                warnings.append("Warning: the size of the rows of file "+file_name+" , is lower than expected: "+str(last_element_row))
                ok_continue_running_code = False

            if ok_continue_running_code:
                # Allocate numpy array for IMU
                if (entered_values_3_a[i] == ""):
                    data = np.empty((np.shape(file_data)[0]*int(entered_values_0_a[i]), 7))
                else:
                    data = np.empty((np.shape(file_data)[0]*int(entered_values_0_a[i]), 10))
                # Enter IMU data from the file   
                for j in range(np.shape(file_data)[0]):
                    for k in range (int(entered_values_0_a[i])):
                        index = j*int(entered_values_0_a[i]) + k
                        data[index,0] = round((index/sampling_freq),4)
                        for l in range(3):
                            data[index,1+l] = file_data[j,(int(entered_values_1_a[i])-1+l)+(k*iterate_IMUs)]
                            data[index,4+l] = file_data[j,(int(entered_values_2_a[i])-1+l)+(k*iterate_IMUs)]
                            if not (entered_values_3_a[i] == ""):
                                data[index,7+l] = file_data[j,(int(entered_values_3_a[i])-1+l)+(k*iterate_IMUs)]

                # Rotation of the data array result R_data array
                rot_x = entered_values_rot_x[i]
                rot_y = entered_values_rot_y[i]
                rot_z = entered_values_rot_z[i]
                # Create a copy of the original data array
                R_data = data.copy()
                # Create a rotation matrix from Euler angles
                rot_matrix = Rotation.from_euler('xyz', [rot_x, rot_y, rot_z], degrees=True)
                # Apply rotation to the Acceleration data
                R_data[:, 1:4] = np.dot(data[:, 1:4], rot_matrix.as_matrix())
                # Apply rotation to the Gyroscope data
                R_data[:, 4:7] = np.dot(data[:, 4:7], rot_matrix.as_matrix())
                # Apply rotation to the Magnetometer data 
                if not (entered_values_3_a[i] == ""):
                    R_data[:, 7:10] = np.dot(data[:, 7:10], rot_matrix.as_matrix())

                # Filter of the R_data array result F_R_data array
                F_R_data = R_data.copy()
                Acc_pct_correction = float(entered_values_1_c[i])
                Gyr_pct_correction = float(entered_values_2_c[i])
                if not (entered_values_3_a[i] == ""):
                    Mag_pct_correction = float(entered_values_3_c[i])
                F_R_data = R_data.copy()
                if Acc_pct_correction > 0:
                    acceleration_data = R_data[:, 1:4]
                    filtered_acceleration_data = np.zeros_like(acceleration_data)
                    # cutoff_freq = 0.5 + (20*((100-Acc_pct_correction)/100))
                    cutoff_freq = Acc_pct_correction
                    filter_order = 2
                    b, a = signal.butter(filter_order, cutoff_freq / (sampling_freq / 2), btype='low')
                    for index in range(3):
                        filtered_acceleration_data[:, index] = signal.filtfilt(b, a, acceleration_data[:, index],padlen=0)
                    F_R_data[:, 1:4] = filtered_acceleration_data
                else:
                    F_R_data[:, 1:4] = R_data[:, 1:4]

                # Gyroscope correction using the mean of the num_seconds_calibration 
                num_seconds_calibration = 1
                calibration_steps = num_seconds_calibration * round(sampling_freq)
                angular_velocity_data = R_data[:, 4:7]
                bias = np.mean(angular_velocity_data[:calibration_steps], axis =0)
                angular_velocity_data -= bias

                if Gyr_pct_correction > 0:
                    # angular_velocity_data = R_data[:, 4:7]
                    filtered_angular_velocity_data = np.zeros_like(angular_velocity_data)
                    # cutoff_freq = 0.5 + (20*((100-Gyr_pct_correction)/100))
                    cutoff_freq = Gyr_pct_correction
                    filter_order = 2
                    b, a = signal.butter(filter_order, cutoff_freq / (sampling_freq / 2), btype='low')
                    for index in range(3):
                        filtered_angular_velocity_data[:, index] = signal.filtfilt(b, a, angular_velocity_data[:, index],padlen=0)
                    F_R_data[:, 4:7] = filtered_angular_velocity_data
                else:
                    F_R_data[:, 4:7] = angular_velocity_data

                if not (entered_values_3_a[i] == ""):
                    if Mag_pct_correction > 0:
                        magnetometer_data = R_data[:, 7:10]
                        filtered_magnetometer_data = np.zeros_like(magnetometer_data)
                        # cutoff_freq = 0.5 + (20*((100-Mag_pct_correction)/100))
                        cutoff_freq = Mag_pct_correction
                        filter_order = 2
                        b, a = signal.butter(filter_order, cutoff_freq / (sampling_freq / 2), btype='low')
                        for index in range(3):
                            filtered_magnetometer_data[:, index] = signal.filtfilt(b, a, magnetometer_data[:, index],padlen=0)
                        F_R_data[:, 7:10] = filtered_magnetometer_data
                    else:
                        F_R_data[:, 7:10] = R_data[:, 7:10]

                np.savetxt(widget_path+"/F_R_"+selected_files[i], F_R_data, delimiter=",")

                # Append the data to the IMU list
                IMU.append(F_R_data)

                # Allocate for quaternions
                Q.append(np.tile([1., 0., 0., 0.], ((IMU[i].shape[0]), 1))) 
                t = 0
                j = 0
                # Add the value of the frequency to the madgwick filter
                madgwick.frequency = sampling_freq
                # Quaternions conversion correction using the mean of the num_seconds_calibration 
                # Check if the value in the entry widget seconds for the Madgwick Filter is an integer
                if not entry_madwick_filter_seconds.get() or not entry_madwick_filter_seconds.get().isdigit():
                    warnings.append("Warning in entry Seconds Madgwick Filter values must be integer numbers, 1 second applied")
                    num_seconds_calibration = 1
                else:
                    num_seconds_calibration = int(float(entry_madwick_filter_seconds.get()))

                calibration_steps = num_seconds_calibration * round(sampling_freq)
                # Check if the value in the entry widget gain for the Madgwick Filter is an integer
                if not entry_madwick_filter_gain.get() or not entry_madwick_filter_gain.get().replace('.', '').isdigit():
                    warnings.append("Warning in entry Gain Madgwick Filter values must be numbers, gain 3 applied")
                    madgwick.gain = 3
                else:
                    try:
                        madgwick.gain = float(entry_madwick_filter_gain.get())
                    except ValueError:
                        warnings.append("Warning in entry Gain Madgwick Filter values must be numbers, gain 3 applied")
                        madgwick.gain = 3
                    
                for row in IMU[i]:       
                    # madgwick = ahrs.filters.Mahony(frequency=sampling_freq)         
                    if entered_values_3_a[i] and entered_values_3_a[i].isdigit() and int(entered_values_3_a[i]) > 0:
                        # After the number of rows high_gain_steps it adapts the gain to the default value when magnetometer data are present
                        if t > calibration_steps:
                            madgwick.gain = 0.041
                        # Data for the Madgwick function
                        # gyr (numpy.ndarray, default: None) – N-by-3 array with measurements of angular velocity in rad/s
                        # acc (numpy.ndarray, default: None) – N-by-3 array with measurements of acceleration in in m/s^2
                        # mag (numpy.ndarray, default: None) – N-by-3 array with measurements of magnetic field in mT
                        # frequency (float, default: 100.0) – Sampling frequency in Herz.
                        # The frequency data is not need because we can add it while creating the .sto file
                        Q[i][t] = madgwick.updateMARG(Q[i][t-1], 
                            gyr=[(row[4])*float(entered_values_2_b[i]),
                                (row[5])*float(entered_values_2_b[i]),
                                (row[6])*float(entered_values_2_b[i])], 
                            acc=[(row[1])*float(entered_values_1_b[i]),
                                (row[2])*float(entered_values_1_b[i]),
                                (row[3])*float(entered_values_1_b[i])], 
                            mag=[(row[7])*float(entered_values_3_b[i]),
                                (row[8])*float(entered_values_3_b[i]),
                                (row[9])*float(entered_values_3_b[i])])
                    else:
                        # After the number of rows high_gain_steps it adapts the gain to the default value when no magnetometer data are present
                        if t > calibration_steps:
                            madgwick.gain = 0.033
                        # If the IMU raw data don't have Magnetometer values the quaternions are created with the madgwick.updateIMU function
                        # For more information https://ahrs.readthedocs.io/en/latest/filters/madgwick.html
                        Q[i][t] = madgwick.updateIMU(Q[i][t-1], 
                            gyr=[(row[4])*float(entered_values_2_b[i]),
                                (row[5])*float(entered_values_2_b[i]),
                                (row[6])*float(entered_values_2_b[i])], 
                            acc=[(row[1])*float(entered_values_1_b[i]),
                                (row[2])*float(entered_values_1_b[i]),
                                (row[3])*float(entered_values_1_b[i])])                   
                    t += 1 
                numrows.append(Q[i].shape[0])
                widgets[i][18]["text"] = " Quaternion created, size: " +str(Q[i].shape)  # update the text of the result_label widget
                results.append(" Original file, "+selected_files[i]+", size "+str(np.shape(file_data))+" // IMU file filtered and rotated, size: " +str(IMU[i].shape)+" , file name: : F_R_"+selected_files[i]+" // Quaternion created, size: " +str(Q[i].shape)+" , file name : Q_"+selected_files[i])
                button = tk.Button(window, text=" Plot Acc", command=lambda i=i: plot_acc_data(i))
                button.grid(row=i+3, column=20)
                button_list_acc.append(button)
                def plot_acc_data(i):
                    # Get the data
                    data = IMU[i]
                    # Extract the time and acceleration data
                    time_acc = data[:, 0]
                    acceleration = data[:, 1:4]*float(entered_values_1_b[i])
                    # Calculate the magnitude of the acceleration vector
                    magnitude_acc = np.sqrt(np.sum(acceleration**2, axis=1))
                    # Plot the data
                    plt.xlim(np.min(time_acc), np.max(time_acc))
                    plt.plot(time_acc, acceleration)
                    # Plot the magnitude
                    plt.plot(time_acc, magnitude_acc)
                    # Add a title, lables and legend to the graph
                    plt.title("Acceleration XYZ file: "+selected_files[i]+" placement "+selected_parts[i]+", LF correction %: "+entered_values_1_c[i] ,  fontdict={'fontsize': 10, 'fontweight': 'normal'})
                    plt.xlabel('Time (s)', fontsize=10)
                    plt.ylabel('Acc (m/s^2)', fontsize=10)
                    plt.legend(['X', 'Y', 'Z', 'Magnitude'])
                    plt.axhline(y=0, color='black', linewidth=0.4)
                    plt.axhline(y=9.81, color='black', linewidth=0.4)
                    plt.show()
                button_gyr = tk.Button(window, text=" Plot Gyr", command=lambda i=i: plot_gyr_data(i))
                button_gyr.grid(row=i+3, column=21)
                button_list_gyr.append(button_gyr)
                def plot_gyr_data(i):
                    # Get the data
                    data = IMU[i]
                    # Extract the time and angular velocity data
                    time_gyr = data[:, 0]
                    acceleration = data[:, 4:7]*float(entered_values_2_b[i])
                    # Calculate the magnitude of the angular velocity vector
                    magnitude_gyr = np.sqrt(np.sum(acceleration**2, axis=1))
                    # Plot the data
                    plt.xlim(np.min(time_gyr), np.max(time_gyr))
                    plt.plot(time_gyr, acceleration)
                    # Plot the magnitude
                    plt.plot(time_gyr, magnitude_gyr)
                    # Add a title, lables and legend to the graph
                    plt.title("Angular Velocity XYZ file: "+selected_files[i]+" placement "+selected_parts[i]+", LF correction %: "+entered_values_2_c[i],  fontdict={'fontsize': 10, 'fontweight': 'normal'})
                    plt.xlabel('Time (s)', fontsize=10)
                    plt.ylabel('Gyr (rad/s)', fontsize=10)
                    plt.legend(['X', 'Y', 'Z', 'Magnitude'])
                    plt.axhline(y=0, color='black', linewidth=0.4)
                    plt.show()

        if ok_continue_running_code:
            # Save the quaternions files adding Q to the name of the file and using the widget_path folder
            for i in range(len(Q)):
                np.savetxt(widget_path + r"\Q_"+selected_files[i], Q[i], delimiter=' ')

            # Header for the placement.sto and movement.sto files
            def header_sto_file():
                f.write("DataRate=52.0\n")
                f.write("DataType=Quaternion\n")
                f.write("version=3\n")
                f.write("OpenSimVersion=4.2\n")
                f.write("endheader\n")
                f.write("time	"+sensors_placement+"\n")

            # Create the placement.sto file with the data of the first raw of the quaternion
            # This file is not necessary because in Opensim it is possible to use the movement.sto file for the calibration/placement
            # in that case Opensim also takes the first line of the movement.sto file
            f = open(widget_path + r"\placement.sto", 'w')
            header_sto_file()
            f.write("0")
            # Create the placement file just after the calibration step 
            placement_step = calibration_steps + 1
            for i in range(len(Q)):
                f.write(" "+"\t{},{},{},{}".format(Q[i][placement_step,0],Q[i][placement_step,1],Q[i][placement_step,2],Q[i][placement_step,3]))

            results.append(" Placement file created: "+widget_path+"/placement.sto")         

            # Create the movement.sto file with the data of the quaternions
            f = open(widget_path + r"\movement.sto", 'w')
            header_sto_file()
            time = 0

            # To iterate the quaternions if the number of rows is different
            min_numrows = min(numrows)
            if len(set(numrows)) != 1:
                warnings.append(" Warning: length of the IMU data files and quaternions is different "+str(numrows)+ ", movement file created over the first "+str(min_numrows)+" rows" )

            for j in range(placement_step,min_numrows):
                f.write(str(time))
                for i in range(len(Q)):
                    f.write(" "+"\t{},{},{},{}".format(Q[i][j,0],Q[i][j,1],Q[i][j,2],Q[i][j,3]))
                f.write("\n")
                j += 1
                time += round((1/float(frequency)),4)
                    
            results.append(" Movement file created: "+widget_path+"/movement.sto") 

            if warnings:
                results += warnings

            # Add time to the results information and creates a log.txt file
            results.append(" Log registry file created log.txt at " + str(datetime.now().strftime("%Y/%m/%d %H:%M:%S")))
            with open(widget_path+'/log.txt', 'w') as file_log:
                file_log.writelines([result + '\n' for result in results])

            # Check if the label_global_results exists and display the information in the results list
            if label_global_results is not None and label_global_results.winfo_exists():
                label_global_results.config(text="\n" + "\n".join(results))
            else:    
                label_global_results = tk.Label(window, text="\n" + "\n".join(results), font=("Arial", 8), wraplength=1200, justify="left")
                label_global_results.grid(row=num_files + 3, column=1, columnspan=19)
        else:
            if warnings:
                # Displais an information error message in the label_result of each file
                for i in range(len(widgets)):
                    widgets[i][18]["text"] = "Warnings found ("+str(len(warnings))+") check the list of errors"  # update the text of the result_label widget
                # Check if the label_global_results exists and display the information in the errors list
                if label_global_results is not None and label_global_results.winfo_exists():
                    label_global_results.config(text="\n" + "\n".join(warnings))
                else:    
                    label_global_results = tk.Label(window, text="\n" + "\n".join(warnings), font=("Arial", 8), wraplength=1200, justify="left")
                    label_global_results.grid(row=num_files + 3, column=1, columnspan=19)
    else:
        # Displais an information error message in the label_result of each file
        for i in range(len(widgets)):
            widgets[i][18]["text"] = "Errors found ("+str(len(errors))+") check the list of errors"  # update the text of the result_label widget
        # Check if the label_global_results exists and display the information in the errors list
        if label_global_results is not None and label_global_results.winfo_exists():
            label_global_results.config(text="\n" + "\n".join(errors))
        else:    
            label_global_results = tk.Label(window, text="\n" + "\n".join(errors), font=("Arial", 8), wraplength=1200, justify="left")
            label_global_results.grid(row=num_files + 3, column=1, columnspan=19)

# "Close" button function
def close_window():
    window.destroy()

# "Help" button function opens a website with information about the program
def open_help():
    webbrowser.open("https://drive.google.com/file/d/1mhg7X98GejYahnPr0Yw7Pu4BCNbbYN6x/view?usp=sharing")

# "Open folder" button function opens a website with information about the program
def open_folder():
    # Verify if the string in the entry widget "widget_path" exists and creates the directory if not and also check if there is an error in the string name before creating the new directory
    widget_path = entry_path.get()
    if not os.path.isdir(widget_path):
        # widget_path is not a directory, use files_path instead
        widget_path = files_path
        # Display the path in the entry_path widget
        entry_path.delete(0, "end")
        entry_path.insert(0, files_path)
    # At this point, widget_path is guaranteed to be a valid directory (or so we hope)
    try:
        if not os.path.exists(widget_path):
            # Folder does not exist, create it
            os.makedirs(widget_path)
    except Exception as e:
        # An error occurred while trying to create the directory
        # You can handle the error here
        print(e)
    print (widget_path)
    abs_path = os.path.abspath(widget_path)
    subprocess.run(['explorer', abs_path])

# Create aspace gap to the left
label = tk.Label(window, width=2)
label.grid(row=0, column=0)

# Add the "Select Files" button
button = tk.Button(window, text="Select Files", width = 10, command=select_files)
button.grid(row=0, column=1) 

# path_label = tk.Label(window, text="", font = ("Arial", 6))
# path_label.grid(row=0, column=15)

delete_button = tk.Button(window, text="Delete Files", width = 10, command=delete_files)
delete_button.grid(row=0, column=2)

# Add the "Apply all" button
apply_all_button = tk.Button(window, text="Apply all", command=apply_all)
apply_all_button.grid(row=0, column=3)

# Create the "Save..." button and define a function for saving the information to an XML file
save_button = tk.Button(window, text="Save...", width = 8, command=save_xml)
save_button.grid(row=0, column=5, columnspan= 2)

# Create the "Load..." button and define a function for opening and parsing the XML file
open_button = tk.Button(window, text="Load...", width = 8, command=open_xml)
open_button.grid(row=0, column=7, columnspan= 2)

# Add the "Close" button
close_button = tk.Button(window, text="Close", width=8, command=close_window)
close_button.grid(row=0, column=10, columnspan= 2)  

# Add the "Help" button
help_button = tk.Button(window, text="Help", width=10, command=open_help)
help_button.grid(row=0, column=13, columnspan= 2) 

# Add the "Open folder" button
button = tk.Button(window, text="Open Folder", width = 10, command=open_folder)
button.grid(row=0, column=16, columnspan= 2) 

# Add the "Run" button
button = tk.Button(window, text="Run", width = 10, command=run_code)
button.grid(row=0, column=19)  

# Create elements "Frequency" and "Output Folder" for the first row
label_frequency = tk.Label(window, text="Frequency", font = font_text2, width = 10,height=2,justify="center")
label_frequency.grid(row=1, column=1)  
label_madwick_filter = tk.Label(window, text="Madwick Filter/Gain/Seconds", font = ("Arial", 7), width = 19,height=2,justify="center")
label_madwick_filter.grid(row=1, column=3)  
label_frequency = tk.Label(window, text="Output Folder", font = font_text2, width = 10,height=2,justify="center")
label_frequency.grid(row=1, column=9) 
# Create an entry widget for entering "Frequency" and "Output Folder" values
entry_frequency = tk.Entry(window, width=7, justify="center")
entry_frequency.grid(row=1, column=2) 
entry_frequency.insert(0, "52")  
entry_path = tk.Entry(window, width=105, font=("Arial", 6),justify="left")
entry_path.insert(0, "")  
entry_path.grid(row=1, column=10, columnspan= 10)  
entry_madwick_filter_gain = tk.Entry(window, width=7, justify="center")
entry_madwick_filter_gain.grid(row=1, column=4, columnspan=3) 
entry_madwick_filter_gain.insert(0, "3")  
entry_madwick_filter_seconds = tk.Entry(window, width=7, justify="center")
entry_madwick_filter_seconds.grid(row=1, column=7) 
entry_madwick_filter_seconds.insert(0, "1")     


# Create labels for the second row
label_0_file = tk.Label(window, text="File name", font = font_text2, width = 12,justify="center")
label_0_file.grid(row=2, column=1)  
label_0_file_1 = tk.Label(window, text="Elem./\rrow", font = font_text2, width = 9,justify="center")
label_0_file_1.grid(row=2, column=2)  
label_0_file_3 = tk.Label(window, text="Placement", font = font_text2, width = 19,justify="center")
label_0_file_3.grid(row=2, column=3)  
label_0_file_3 = tk.Label(window, text="Rotation XYZº", font = font_text2, width = 11,justify="left")
label_0_file_3.grid(row=2, column=4, columnspan= 3)  
label_0_acc_1 = tk.Label(window, text="Pos.", font = font_text2, width = 4,justify="center")
label_0_acc_1.grid(row=2, column=8)  
label_0_acc_2 = tk.Label(window, text="Units\rm/s^2", font = font_text2, width = 7,justify="center")
label_0_acc_2.grid(row=2, column=9)  
label_0_acc_3 = tk.Label(window, text="Filter\rfc Hz", font = ("Arial", 8), width = 4,justify="center")
label_0_acc_3.grid(row=2, column=10)  
label_0_gyr_1 = tk.Label(window, text="Pos.", font = font_text2, width = 4,justify="center")
label_0_gyr_1.grid(row=2, column=12)  
label_0_gyr_2 = tk.Label(window, text="Units\rrad/s", font = font_text2, width = 7,justify="center")
label_0_gyr_2.grid(row=2, column=13) 
label_0_gyr_3 = tk.Label(window, text="Filter\rfc Hz", font = ("Arial", 8), width = 4,justify="center")
label_0_gyr_3.grid(row=2, column=14)  
label_0_mag_1 = tk.Label(window, text="Pos.", font = font_text2, width = 6,justify="center")
label_0_mag_1.grid(row=2, column=16)  
label_0_mag_2 = tk.Label(window, text="Units\rmT", font = font_text2, width = 7,justify="center")
label_0_mag_2.grid(row=2, column=17) 
label_0_mag_3 = tk.Label(window, text="Filter\rfc Hz", font = ("Arial", 8), width = 4,justify="center")
label_0_mag_3.grid(row=2, column=18)   
initial_text = []
initial_text.append("Welcome to the imu2sto program!")
initial_text.append("This program is designed to convert IMU data to quaternions and OpenSim .sto files.")
initial_text.append("To get started, use the following buttons and entry widgets:")
initial_text.append("\n")
initial_text.append("- <Select Files> to add IMU data files. You can select multiple files at once and add more files to your selection later.")
initial_text.append("- <Apply all> to copy the input data from the first file/row to the rest of the files/rows.")
initial_text.append("- <Save...> to create an .xml file with the current configuration of files and inputs.")
initial_text.append("- <Load...> to open an .xml file with a saved configuration of files and inputs.")
initial_text.append("- <Help> for more information on how to use the program.")
initial_text.append("- <Run> to create quaternions and .sto files for the selected files and inputs.")
initial_text.append("- <Plot Acc> or <Plot Gyr> after creating the files, they can be used to plot different files on the same graph, this option is only available after running the program.")
initial_text.append("\n")
initial_text.append("In addition, the following entry widgets are available:")
initial_text.append("- [Frequency]: The frequency at which IMU data was collected.")
initial_text.append("- [Madwick Filter/Gain/Seconds]: Apply the select Gain during the select Seconds and after that applies the default values 0.041 or 0.033 for IMU without Mag.")
initial_text.append("- [Output Folder]: The folder where the resulting files will be saved.")
initial_text.append("- [Elem./row]: The number of IMU data for each row of the file, 1 IMU data for each acc+gyr+(mag) package.")
initial_text.append("- [Placement]: The OpenSim placement of the IMU sensor/file. Each file must have a different placement.")
initial_text.append("- [Rotation XYZº]: To apply a rotation to the IMU data for global alignment before creating the quaternions and .sto files.")
initial_text.append("- [Pos.]: The position, starting at 1, of the first element of acceleration, gyroscope or magnetometer respectively.")
initial_text.append("- [Pos.]: If the IMU doesn't have magnetometer data, this value should be left blank.")
initial_text.append("- [Units]: Units conversion from sensor units to Madgwick filter units (m/s^2, rad/s and mT).")
initial_text.append("- [Filter fc Hz]: Leave blank for no filtering, or enter a value lower than the Frequency to apply an increasing level of Low Pass filtering to acc, gyr or mag.")
initial_text.append("- The resulting IMU files after applying the rotation and filtering are named as F_R_<name of the file>, with 1 IMU data for each row.")
initial_text.append("\n")
initial_text.append("This program is developed as a part of my PhD research to facilitate the data processing.")
initial_text.append("If you have any questions or feedback, please contact me at marra610@student.otago.ac.nz / raulmartinphd@gmail.com")
label_global_results = tk.Label(window, text="\n" + "\n".join(initial_text), font=("Arial", 8), wraplength=1200, justify="left")
label_global_results.grid(row=3, column=1, columnspan=19)
            
window.mainloop()