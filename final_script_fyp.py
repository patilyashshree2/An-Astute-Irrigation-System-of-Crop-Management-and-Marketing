#final_script_fyp.py
import subprocess
import os
import socket
import csv
import time,sched
import RPi.GPIO as GPIO
import glob
import logging
import requests
import json
from errno import ENETUNREACH
headers={'Content-type': 'application/json'} #headers set to specify the content type of the data being sent to the URI
s = sched.scheduler(time.time, time.sleep) #used to start a new thread process
from threading import Timer
from suds.client import Client
URL_get_data = "http://192.168.43.104:5010/get_data" #URI to send JSON data to be inserted into get_data table
URL_update_mois_data="http://192.168.43.104:5010/update_mois_data" #URI to send JSON data to be updated into update_mois_data table
URL_delete_ip="http://192.168.43.104:5010/delete_ip" #URI to send JSON data to be deleated from the table

TRIG=23 # trigger pin of ultrasonic
ECHO=24 # echo pin of ultrasonic
mois = 0
RELAY_1 = 25
RELAY_2=16
GPIO.setmode(GPIO.BCM)
GPIO.setup(RELAY_1,GPIO.OUT)
GPIO.setup(RELAY_2,GPIO.OUT)
GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)
moisture_threshold_low=550
moisture_threshold_high=80
water_tank_height=25
water_tank_status = ""
distance = 0
raspberry_id=1

def read_distance(): # measures using the ultrasonic sensor and returns the level of water in the tank
   try:

       water_level=0
       print "Water level sensor testing"
       GPIO.output(TRIG, False)
       print "Waiting For Sensor To Settle"
       time.sleep(2)
       GPIO.output(TRIG, True) # trigger starts sending pulse

       time.sleep(0.00001)

       GPIO.output(TRIG, False) # trigger stops sending pulse
       while GPIO.input(ECHO)==0: # loops till echo receives back the reflected pulse
               pulse_start = time.time()
       while GPIO.input(ECHO)==1:
               pulse_end = time.time()
       pulse_duration = pulse_end - pulse_start # calculates the duration of pulse traversed
       distance = pulse_duration * 17150 
       distance = round(distance, 2)
       print distance
       final_distance = distance
       print int(100-((100*distance)/water_tank_height))
       return final_distance
   except:
       return 0 
       
   
def run_status():  # checks for the functioning status of nodemcus
   try:
       data="rashmipawar921@gmail.com"
       json_data = json.dumps(data) # converts dictionary data into json
       r = requests.get(url = URL_delete_ip, json = json_data, headers = headers) # the data in json format is sent to the specified URI using GET method
       print "running alive_status_nmcu.py"
       execfile("/home/pi/Desktop/alive_status_nmcu.py") # executes the specified file
   except:
       pass
   
def run_sensor():  # requests the nodemcus for sensor readings and sends it to server
   
   temp=0
   raspberry_id="1"
   water_tank_level=30
   water_pump_status="off"
   send_noti="1"
   water_level=20
   ip_list=[]
   f=open("/home/pi/Desktop/nmcu_ip.csv","r") # opens file in read mode
   file_contents=csv.reader(f) # reads each record from csv into a dictionary
   ip_list=list(file_contents) # converts dictionary into list

   moisture_readings={}

   for i in range(len(ip_list)): # iterates for each ip of the alive nodemcus

       try:
           deadline = time.time() + 5.0 # used to set a time limit of 5 seconds
           UDP_IP=ip_list[i][1]
           UDP_PORT=1885
           MESSAGE="aiscmm_smart_irrigation_169.254.152.165_sensor_data" # message sent to the nodemcu requesting for sensor readings
           
           print "UDP target ip:", UDP_IP
           print "udp target port:", UDP_PORT
           print "msg:",MESSAGE

           sock=socket.socket(socket.AF_INET,socket.SOCK_DGRAM) # creates a socket
           try:
               sock.sendto(MESSAGE,(UDP_IP, UDP_PORT)) # udp message is sent to the specific nodemcu using ip and port
               print "Packet send"
           except IOError as e:
               if e.errno==ENETUNREACH:
                   pass
           sock.settimeout(deadline-time.time()) # closes connection after timeout
           chunks=[]
           bytes_recd=0
           chunks=sock.recv(4096) # receives data sent by nodemcu
           print chunks
           chunks_list=[]
           chunks_list=chunks.split(",") # list of sensor readings is created

           temp=chunks_list[0]
           mois = chunks_list[2]
           moisture_readings[i]=float(mois)
           raspberry_id="1"
           water_pump_status="off"
           send_noti="1"

           flag = 2 
       except socket.timeout:
           print "time out"
           moisture_readings[i]=2000
           continue

   no_of_pipes=2 #static
   pipe_list1=[]
   pipe_list2=[]
   for i in moisture_readings: 
       pipe_no=(i+1)%no_of_pipes;
       if pipe_no==1:
           pipe_list1.append(moisture_readings[i]) # appends into list readings of moisture near pipe 1
       else:
           pipe_list2.append(moisture_readings[i]) # appends into list readings of moisture near pipe 2
       
   mois_avg1=0;
   mois_avg2=0;
   faulty_count1=0
   faulty_count2=0
   mois_avg_list=[]
   for i in range(len(pipe_list1)):
       if pipe_list1[i]==2000:
           faulty_count1=faulty_count1+1
           continue
       else:
           mois_avg1=mois_avg1+pipe_list1[i]
       mois_avg1=mois_avg1/(len(pipe_list1)-faulty_count1) # calculates average of moisture readings near pipe1
   mois_avg_list.append(mois_avg1)
   
   for i in range(len(pipe_list2)):
       if pipe_list2[i]==2000:
           faulty_count2=faulty_count2+1
           continue
       else:
           mois_avg2=mois_avg2+pipe_list2[i]
       mois_avg2=mois_avg2/(len(pipe_list2)-faulty_count2) # calculates average of moisture readings near pipe1
   mois_avg_list.append(mois_avg2)
   
   print mois_avg_list
   
   water_tank_status = "off"
       try:
   
       for i in range(len(mois_avg_list)):
           try: 
               if(mois_avg_list[i]>moisture_threshold_low): # checks if moisture level measured is lesser than required threshold
                   distance = read_distance()
                   water_tank_level=distance
                   print(distance, water_tank_height)
                   if(distance<water_tank_height): # checks if there is sufficient water in the tank
                       print("inside the pump")
                       if i==0:
                           GPIO.output(RELAY_1,True) # turns on the water pump 1
                   
                           water_tank_status = "motor on"
                           print water_tank_status
                           data={"raspberry_id":raspberry_id,"pump_id":i+1,"mois":mois_avg_list[i]} # creates dictionary of current values to be sent to server
                           print data
                           
                           json_data = json.dumps(data) # converts dictionary to json
                           r = requests.get(url = URL_update_mois_data, json = json_data, headers = headers) # sends json data to the URI
                           print "data is updated to db"
                           
                           time.sleep(10)
                           GPIO.output(RELAY_1, False) # turns off the water pump 1
                           water_tank_status = "off"
                           print water_tank_status
                       
                       else:
                           GPIO.output(RELAY_2,True) # turns on the water pump 2
                       
                           water_tank_status = "motor on"
                           print water_tank_status
                           data={"raspberry_id":raspberry_id,"pump_id":i+1,"mois":mois_avg_list[i]} # creates dictionary of current values to be sent to server
                           
                           json_data = json.dumps(data) # converts dictionary to json
                           r = requests.get(url = URL_update_mois_data, json = json_data, headers = headers) # sends json data to the URI
                           print "data is updated to db"
                           
                           time.sleep(10)
                           GPIO.output(RELAY_2, False) # turns off the water pump 2
                           water_tank_status = "off"
                           print water_tank_status
                           
                   else:
                       
                       print water_tank_status
                       
               else:
                   
                   print water_tank_status
           except:
               continue
       
           data={"temp":temp,"mois":mois_avg_list[i],"raspberry_id":raspberry_id,"water_tank_level":water_tank_level,"water_tank_status":water_tank_status,"send_noti":send_noti} # creates dictionary of current values to be sent to server
                       
           json_data = json.dumps(data) # converts dictionary to json
           r = requests.get(url = URL_get_data, json = json_data, headers = headers) # sends json data to the URI
           print "data is updated to db"
   except:
       pass

while(1):

   s.enter(30, 1, run_sensor, ()) # schedules the process thread to run every 30 seconds
   s.enter(300, 2, run_status, ()) # schedules the process thread to run every 300 seconds
   s.run()
