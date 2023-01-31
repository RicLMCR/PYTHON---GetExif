# ********************* EXTRACT GPS INFO FROM IMAGE FILE *****************************

# Given a folder of images / photos, we would like to identify any images 
# that contain useful information (in particular location data) and highlight this to 
# the user.

# The tool can be a script or make use of a suitable Python GUI to allow the user to 
# select the folder and display the results. Potentially other APIs can be used to 
# provide look-up or display of the location based on the discovered GPS/location 
# coordinates.

import os
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS

# Variables
count = 0
file_list = []
file_path = ""
open_image = ""

# Prompt user for folder location
print("\nWelcome to the WKWYA GPS location app V1.0\n")
locate_file = input("Please enter the folder path\n")


# Find file folder location on local drive
def find_file():
    if os.path.exists(locate_file):
        print("Files listed:", locate_file,"\n")
        
        # List image files within folder add to file_list array
        for i in os.listdir(locate_file):
            if i: 
                if i.endswith(".jpg") or i.endswith(".jpeg"):
                    global file_list
                    file_list.append(i)
            else:
                print("This folder does not contain any files")
                
    # If unable to locate file then exit
    else:
        print("File cannot be located. Program will terminate")
        exit()
        
        
# List, select and open image files
def select_images():
    #  Print list of image files
    for i in file_list:
        global count
        print(count, ":",i)
        count = count +1

    # User selects image file
    file_select = int(input("\nSelect your image by entering the prefix\n"))
    selected_file = file_list[file_select]
    
    # Print file path and filename for selection
    global file_path
    file_path = locate_file + selected_file
    print("File_path is:", file_path,"\n")
    
    # Open image with file path and name
    global open_image
    open_image = Image.open(file_path)
    exif_data = open_image.getexif()
    
    
# Extract latitude and longitude from location key
def get_exif(filename):
    exif_data = {}
    image = Image.open(filename)
    info = image._getexif()
    if info:
        for tag, value in info.items():
            decoded = TAGS.get(tag, tag)
            if decoded == "GPSInfo":
                gps_data = {}
                for gps_tag in value:
                    sub_decoded = GPSTAGS.get(gps_tag, gps_tag)
                    gps_data[sub_decoded] = value[gps_tag]
                exif_data[decoded] = gps_data
            else:
                exif_data[decoded] = value
    return exif_data


# Get latitude and longitude
def lat_long():
    exif = get_exif(file_path)

    # Assign latitude and longitude variables
    north = exif["GPSInfo"]["GPSLatitude"]
    west = exif["GPSInfo"]["GPSLongitude"]
    print("Extracting GPS co-ordinates")
    print("\nLatitude is:", north, ". Longitude is:", west)
    
find_file() # Find file folder location on local drive
select_images() # List, select and open image files
get_exif(file_path) # Extract latitude and longitude from location key
lat_long() # Get latitude and longitude

# Additional error tests needed
# file path input must have backslashes
# consider streamlining method of listing files - use map?
# fix lines 33/34 'else' statement
# use gps co-ordinates to display location (in browser maybe?)