# Pi-GPS
+ Using Tkinter (Python windows system) - GPS6MV2 module
+ 

-- python3 gps_tkinter.py

# FUNCTIONS
- DISPLAY LIVE GPS position
- RECORD history all GPS positions received in a .json file [date,latitude,longitude]
- WAYPOINTS list .json to choose from
- DISPLAY DISTANCE to chosen waypoint
- SET actual GPS position as a waypoint (named by date)
- CLEAR GPS positions history .json

# MENU

# WAYPOINTS
In this concept Waypoints are collected from the file "gps_tkinter_waypoints.json"
This file is easily editable if needed.
Version 0-1:
  - add actual GPS position as a waypoint in the file "gps_tkinter_waypoints.json" with button "+ POSITION ACTUELLE" top left corner

# WAYPOINTS LIST
The list displays waypoints written in "gps_tkinter_waypoints.json" by names.
When a waypoint name is selected from the list window,
a new window will open, to display name, latitude and longitude.
Selecting a waypoint will turn the distance displaying on top right corner of the main program window.
The chosen waypoint is written in file "gps_tkinter_waypoint.json".

# POSITIONS
Button REC to start recording.
The button will turn on Red when activ.
A counter displays the count of all GPS positions written in the file "gps_tkinter_datas.json".

## LANGAGE
- made in French :)

## TO-DO
- on clear waypoints list: reload list
- on add new waypoint: reload list
- add waypoint window to finish
- add russian
- add english
- blank actual targeted waypoint
