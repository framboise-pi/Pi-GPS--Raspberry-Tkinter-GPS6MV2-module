#!/usr/bin/env python
# -*- coding: utf-8 -*-

#####################################
#codelibre.fr
#https://github.com/framboise-pi
#####################################
#Break the rules! Programmons dans notre langue natale
#GY-GPS6MV2 Sensitivity : -161dBm Baud Rate: 4800-230400
#Operating Temperature -40°C ~ 85°C
#Type: 50 channels, GPS L1(1575.42Mhz)
#Horizontal Position Accuracy: 2.5m
#https://www.openstreetmap.org/export#map=5/51.500/-0.100
#####################################

import datetime
import tkinter as tk
from tkinter import *
import serial
import pynmea2
import json
from tkinter import ttk
from json.decoder import JSONDecodeError
import math

# création d'une fenêtre
global fenetre
fenetre = tk.Tk()

#serial init GPS
global pynmea2
global ser
ser = serial.Serial('/dev/ttyAMA0',9600)

#etat de l'enregistrement true/false
global etat
etat = False

#PSEUDO THEME
global theme_bg
theme_bg = 'black'
global theme_fg
theme_fg = 'white'
        
class GPScodelibre:

    def InitWaypoints():
        #create an empty list for jsonload. dict{} do not have append function.
        ecrire = []
        with open("gps_tkinter_waypoints.json", "w") as waypoints_file:
            litterature = json.dump(ecrire, waypoints_file)
            waypoints_file.close()
            
    def InitData():
        #create an empty list for jsonload. dict{} do not have append function.
        ecrire = []
        with open("gps_tkinter_data.json", "w") as data_file:
            litterature = json.dump(ecrire, data_file)
            data_file.close()

    def APropos():
         
        FenetreAPropos = Toplevel(fenetre)
        FenetreAPropos.title("A Propos")
        FenetreAPropos.geometry("300x200+900+150")
        FenetreAPropos.resizable(0, 0)
        FenetreAPropos.configure(bg=theme_bg)
        Label(FenetreAPropos,
              text ="GPS-TKinter v0.1 Absolument Abricot").pack()

    def WaypointAjout():
         
        FenetreWaypointAjout = Toplevel(fenetre)
        FenetreWaypointAjout.title("ajouter un Waypoint")
        FenetreWaypointAjout.geometry("300x200+900+150")
        FenetreWaypointAjout.resizable(0, 0)
        FenetreWaypointAjout.configure(bg=theme_bg)
        # A Label widget to show in toplevel
        Label(FenetreWaypointAjout, 
              text ="Future option").pack()
    
    global WaypointAjoutPositionActuelle
    def WaypointAjoutPositionActuelle():

        derniere = open("gps_tkinter.json")
        derniere_data = json.load(derniere)
        derniere_date = derniere_data['date']
        derniere_lat = derniere_data['lat']
        derniere_long = derniere_data['long']
        derniere.close()
        
        with open("gps_tkinter_waypoints.json") as GPSwaypoints:
            liste_waypoints = json.load(GPSwaypoints)
        ecrire_waypoints = {
                "nom": derniere_date, 
                "long": derniere_long,
                "lat": derniere_lat
                }
            
        liste_waypoints.append(ecrire_waypoints)
        #liste.update(ecrire)
        with open("gps_tkinter_waypoints.json", "w") as waypoints_file:
            waypoints_maj = json.dump(liste_waypoints, waypoints_file, indent=3, separators=(',',': '))
            waypoints_file.close()
    
    global WaypointChoixFenetre
    global listbox
    FenetreWaypointChoix = Toplevel(fenetre)
    FenetreWaypointChoix.title("CHOISIR un Waypoint")
    FenetreWaypointChoix.geometry("300x200+810+150")
    FenetreWaypointChoix.resizable(0, 0)
    FenetreWaypointChoix.configure(bg=theme_bg)
    listbox = tk.Listbox(FenetreWaypointChoix)
    listbox.pack()

    with open("gps_tkinter_waypoints.json") as GPSwaypoints:
        liste_waypoints = json.load(GPSwaypoints)
    for noms in liste_waypoints:
        ligne = 0
        listbox.insert(ligne, noms['nom'])
        ligne = ligne + 1
    
    global distance
    
    global items_selected
    def items_selected(event):
        # get all selected indices
        selection = event.widget.curselection()
        global selected_waypoint


        if selection:
            index = selection[0]
            selected_waypoint = event.widget.get(index)
            FenetreDistance = Toplevel(fenetre)
            FenetreDistance.title("WAYPOINT SUIVI")
            FenetreDistance.geometry("300x200+900+400")
            FenetreDistance.resizable(0, 0)
            FenetreDistance.configure(bg=theme_bg)

            with open("gps_tkinter_waypoints.json") as GPSwaypoints:
                liste_waypoints = json.load(GPSwaypoints)
                for waypoint in liste_waypoints:
                    if (waypoint['nom'] == selected_waypoint):
                        ecrire = {
                            "nom": waypoint['nom'],
                            "lat": waypoint['lat'],
                            "long": waypoint['long']
                            }
                        with open("gps_tkinter_waypoint.json", "w") as write_file:
                            ecriture = json.dump(ecrire, write_file)
                        
                        selected_lat = "latitude: ",waypoint['lat']
                        selected_long = "longitude: ",waypoint['long']
                        selected_waypoint = waypoint['nom']
            
            Label(FenetreDistance, text = selected_waypoint).pack()
            Label(FenetreDistance, text = selected_lat).pack()
            Label(FenetreDistance, text = selected_long).pack()

    def WaypointsChoix():
        FenetreWaypointChoix = Toplevel(fenetre)
        FenetreWaypointChoix.title("Waypoints")
        FenetreWaypointChoix.geometry("300x200+200+150")
        FenetreWaypointChoix.resizable(0, 0)
        FenetreWaypointChoix.configure(bg=theme_bg)
        listbox = tk.Listbox(FenetreWaypointChoix)
        listbox.pack()

        with open("gps_tkinter_waypoints.json") as GPSwaypoints:
            liste_waypoints = json.load(GPSwaypoints)
        for noms in liste_waypoints:
            ligne = 0
            listbox.insert(ligne, noms['nom'])
            ligne = ligne + 1
        listbox.bind('<<ListboxSelect>>', items_selected)
    
    global haversine
    def haversine(lat1, long1, lat2, long2):
        R = 6372800  # Earth radius in meters

        phi1, phi2 = math.radians(lat1), math.radians(lat2) 
        dphi       = math.radians(lat2 - lat1)
        dlambda    = math.radians(long2 - long1)
        
        a = math.sin(dphi/2)**2 + \
            math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
        
        return 2*R*math.atan2(math.sqrt(a), math.sqrt(1 - a))
   

    global Enregistrement
    def Enregistrement():
        global etat
        etat = not etat

##################################### FENETRE PRINCIPALE

    styl = ttk.Style()
    styl.configure('blue.TSeparator', background='blue')
    styl.configure('red.TSeparator', background='red')
    styl.configure('white.TSeparator', background='white')

    fenetre.geometry("720x480+150+150")   # taille de la fenêtre et position initiale sur l'écran
    fenetre.title("GPS6MV2 - exploitation des données")   # titre de la fenêtre
    fenetre.resizable(0, 0)
    fenetre.configure(bg=theme_bg)
    fenetre.grid_rowconfigure(0, weight=1)
    fenetre.grid_rowconfigure(1, weight=1)
    fenetre.grid_rowconfigure(2, weight=1)
    fenetre.grid_rowconfigure(3, weight=1)
    fenetre.grid_rowconfigure(4, weight=1)
    fenetre.grid_rowconfigure(5, weight=1)
    fenetre.grid_rowconfigure(6, weight=1)
    fenetre.grid_rowconfigure(7, weight=1)
    fenetre.grid_columnconfigure(0, weight=1)
    fenetre.grid_columnconfigure(1, weight=1)
    fenetre.grid_columnconfigure(2, weight=1)

    menu = Menu(fenetre)
    menu_programme = Menu(menu)
    menu_programme.add_command(label='A propos', command=APropos)
    menu_programme.add_command(label='Quitter', command=fenetre.destroy)
    menu.add_cascade(label='Programme', menu=menu_programme)

    ######verifier si présence des fichiers else créer

    menu_positions = Menu(menu)
    menu_positions.add_command(label='+ Effacer l\'historique des positions', command=InitData)
    menu_positions.add_command(label='+ Sauvegarder une copie .json & effacer [INACTIF]')
    menu.add_cascade(label='Positions', menu=menu_positions)


    menu_waypoints = Menu(menu)
    menu_waypoints.add_command(label='+ Liste des Waypoints', command=WaypointsChoix)
    menu_waypoints.add_command(label='+ Ajouter un Waypoint [INACTIF]', command=WaypointAjout)
    menu_waypoints.add_command(label='+ Effacer les Waypoints', command=InitWaypoints)
    menu.add_cascade(label='Waypoints', menu=menu_waypoints)

    fenetre.config(menu=menu)

    label1 = Label(fenetre,bg=theme_bg, fg=theme_fg, text="Latitude:")
    label1.config(font=("Arial", 12))
    label1.grid(column=0, row=2)
    
    global label2
    label2 = Label(fenetre, text=" ")  # contiendra la mesure de température
    label2.grid(column=1, row=2)

    label3 = Label(fenetre, bg=theme_bg, fg=theme_fg, text="Longitude:")
    label3.config(font=("Arial", 12))
    label3.grid(column=0, row=3)
    
    global label4
    label4 = Label(fenetre, text=" ")  # contiendra la mesure de pression
    label4.grid(column=1, row=3)

    #nombre de points sauvegardés .JSON
    global label8
    label8 = Label(fenetre, text="")
    label8.grid(column=2, row=3)
    
    global label9a
    label9a = Label(fenetre, text="AUCUN WAYPOINT")
    label9a.config(font=("Arial", 10))
    label9a.grid(column=1, row=0)
    
    global label9
    label9 = Label(fenetre, text="CHARGEMENT")
    label9.config(font=("Arial", 16))
    label9.grid(column=2, row=0)

    separator = ttk.Separator(
        fenetre,
        orient='horizontal',
        style='black.TSeparator',
        class_= ttk.Separator,
        takefocus= 1,
        cursor='plus')
    separator.grid(row=1, column=1, ipadx=200, pady=10)

    separator2 = ttk.Separator(fenetre, orient='horizontal',style='white.TSeparator')
    separator2.grid(column=1, row=4, ipadx=200)

    label5 = Label(fenetre, text="dernière postion valide:")
    label5.grid(column=1, row=4)

    global label5a
    label5a = Label(fenetre, text="")
    label5a.grid(column=1, row=5)

    label6 = Label(fenetre, text="Latitude")
    label6.configure(bg=theme_bg, fg=theme_fg)
    label6.grid(column=0, row=6)

    #derniere lat
    global label6a
    label6a = Label(fenetre, text="")
    label6a.config(font=("Courier", 18))
    label6a.grid(column=1, row=6)

    label7 = Label(fenetre, text="Longitude")
    label7.configure(bg=theme_bg, fg=theme_fg)
    label7.grid(column=0, row=7)
    
    global label7a
    label7a = Label(fenetre, text="")
    label7a.grid(column=1, row=7)
    label7a.config(font=("Courier", 18))

    global button_bg
    button_bg = 'lightgreen'
    
    global button_fg
    button_fg = 'black'

    global JsonChapter
    def JsonChapter(GPSdata):
        try:
            GPSparse = pynmea2.parse(GPSdata)

            lat = float(GPSparse.latitude)
            lat = str(round(lat,8))
            long = float(GPSparse.longitude)
            long = str(round(long,8))
            
            if (lat == "0.0"):
                lat = "YYY"
                pass
            if (long =="0.0"):
                long = "YYY"
                pass
            
            now = datetime.datetime.now()
            now = now.strftime("%m/%d/%Y, %H:%M:%S")
            #JSON
            ecrire = {
                    "date": now,
                    "long": long,
                    "lat": lat
                }
            with open("gps_tkinter.json", "w") as write_file:
                ecriture = json.dump(ecrire, write_file)
            if (etat):
                
                with open("gps_tkinter_data.json") as GPSdata:
                    liste = json.load(GPSdata)
                    # get the current date and time

                    ecrire = {
                            "date": now, 
                            "long": long,
                            "lat": lat
                            }
                        
                    liste.append(ecrire)
                    #liste.update(ecrire)
                    with open("gps_tkinter_data.json", "w") as append_file:
                        litterature = json.dump(liste, append_file, indent=3, separators=(',',': '))
                        append_file.close()
            return(lat,long)
            #except (pynmea2.ChecksumError, pynmea2.ParseError):
        except ValueError:
            print('ChecksumError')
            pass

    global Majvaleur
    def Majvaleur(): 
        with open('gps_tkinter_data.json') as fichier:
            try:
                positionz = json.load(fichier)
                nombre = len(positionz)
                dire = nombre," points enregistrés"
                fichier.close()
            except JSONDecodeError:
                pass
       
        try:
            derniere = open("gps_tkinter.json")
            derniere_data = json.load(derniere)
            derniere_date = derniere_data['date']
            derniere_lat = derniere_data['lat']
            derniere_long = derniere_data['long']
        except:
            derniere_date = "..."
            derniere_lat = "..."
            derniere_long = "..."
        derniere.close()
        GPSraw = ser.readline()
        isDecoded = False
        Decoded = []
        #and évite erreur de ser.readline not utf-8: si coordonnées vides
        if (isinstance(GPSraw, bytes)):
            GPSdata = GPSraw.decode('utf-8', errors='ignore')
            if (GPSdata is not None):
                isDecoded = True
            
        if (isDecoded and GPSdata[0:6] == "$GPRMC"):
            Decoded = JsonChapter(GPSdata)
            
        else:
            Decoded = ['XXX', 'XXX']

        #var text position actuelle
        label2['text'] = Decoded[0]
        label2.config(font=("Courier", 28),bg=theme_bg, fg=theme_fg)
        label4['text'] = Decoded[1]
        label4.config(font=("Courier", 28),bg=theme_bg, fg=theme_fg)
        
        #var text derniere position valable
        label5a['text'] = derniere_date
        label5a.configure(bg=theme_bg, fg=theme_fg)
        label6a['text'] = derniere_lat
        label6a.configure(bg=theme_bg, fg=theme_fg)
        label7a['text'] = derniere_long
        label7a.configure(bg=theme_bg, fg=theme_fg)
        
        points_button_fg = 'white'
        points_button_bg = 'black'
        button_rec_bg = 'red'
        button_rec_fg = 'white'
        button_fg = 'black'
        button_bg = 'white'
            
        global etat
        if (etat):
            points_button_bg = 'black'
            points_button_fg = 'red'
            button_fg = 'red'
            button_bg = 'white'
            button_rec_bg = 'white'
            button_rec_fg = 'black'
            

        #var text du nombre de positions dans le fichier data.JSON
        points = str(nombre)
        label8['text']  = points
        label8.configure(font=("Arial", 18),bg=points_button_bg, fg=points_button_fg)
        
        try:
            waypoint_selection = open("gps_tkinter_waypoint.json")
            waypoint_selection_data = json.load(waypoint_selection)
            waypoint_selection_nom = waypoint_selection_data['nom']
            waypoint_selection_lat = waypoint_selection_data['lat']
            waypoint_selection_long = waypoint_selection_data['long']
            
            distance = haversine(
                float(waypoint_selection_lat),
                float(waypoint_selection_long),
                float(derniere_lat),
                float(derniere_long))
            distance = str(round(distance,1))+"m"
            label9a['text']  = ("WAYPOINT: "+waypoint_selection_data['nom'])
        except: distance = "EN ATTENTE"
        #except: pass
        label9['text']  = distance
        
        A = Button(fenetre,
                   text ="REC",
                   height = 2,
                   width = 2,
                   fg = button_fg,
                   bg = button_bg,
                   activeforeground = button_rec_fg,
                   activebackground = button_rec_bg,
                   command = Enregistrement)
        A.grid(column=2, row=2)
    

        B = Button(fenetre,
                   text ="+ POSITION ACTUELLE",
                   #height = 2,
                   #width = 20,
                   fg = theme_fg,
                   bg = theme_bg,
                   activeforeground = theme_bg,
                   activebackground = theme_fg,
                   #command = WaypointAjoutPositionActuelle(derniere_lat,derniere_long))
                   command = WaypointAjoutPositionActuelle)

        B.grid(column=0, row=0)
        
        fenetre.after(1000, Majvaleur) # on recommence dans 1 seconde
        
    try:
        listbox.bind('<<ListboxSelect>>', items_selected)
    except: pass
                
    fenetre.after(1000, Majvaleur)

    fenetre.mainloop()
