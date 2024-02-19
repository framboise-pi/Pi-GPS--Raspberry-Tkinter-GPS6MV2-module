#####################################
#codelibre.fr
#https://github.com/framboise-pi
#####################################
import serial
import pynmea2

ser = serial.Serial('/dev/ttyAMA0',9600)
	
while True:
	donneesBrutes = ser.readline().decode('utf-8')
	if donneesBrutes[0:6] == "$GPRMC":
		donneesTraitees = pynmea2.parse(donneesBrutes)
		print( "Latitude: " + str(donneesTraitees.latitude) + "   Longitude: " + str(donneesTraitees.longitude) )
		