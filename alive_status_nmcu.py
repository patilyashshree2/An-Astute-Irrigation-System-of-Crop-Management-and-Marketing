#Check Alive or Dead status of nodeMCU


#alive_status_nmcu.py
import subprocess
import os
import socket
import csv
import time,sched
import RPi.GPIO as GPIO
import glob
import logging
import json
import requests
s = sched.scheduler(time.time, time.sleep)
from threading import Timer
from suds.client import Client

headers={'Content-type': 'application/json'} #headers set to specify the content type of the data being sent to the URI
URL = "http://192.168.43.104:5010/insert_ip" #URI to send JSON data to be inserted into insert_ip table

def run_sensor_status(): # checks is the nodemcu is functioning else sends the ip of faulty to server
   faulty_nmcu=[]    
   raspberry_id="1"
   
   send_noti="6"
   
   ip_list=[]
   f=open("/home/pi/Desktop/nmcu_ip.csv","r") # opens file in read mode
   file_contents=csv.reader(f) # reads each record from csv into a dictionary
   ip_list=list(file_contents) # converts dictionary into list
       
   for i in range(len(ip_list)):  # iterates for each ip of the nodemcus

       try:
           deadline = time.time() + 5.0 # used to set a time limit of 5 seconds
           UDP_IP=ip_list[i][1]
   
           UDP_PORT=1885
           MESSAGE="aiscmm_smart_irrigation_169.254.152.165_sensor_status" # message sent to the nodemcu requesting for sensor status
           
           print "UDP target ip:", UDP_IP
           print "udp target port:", UDP_PORT
           print "msg:",MESSAGE

           sock=socket.socket(socket.AF_INET,socket.SOCK_DGRAM) # creates a socket
           sock.sendto(MESSAGE,(UDP_IP, UDP_PORT)) # udp message is sent to the specific nodemcu using ip and port
           print "Packet send"
           sock.settimeout(deadline-time.time()) # closes connection after timeout
           chunks=[]
           bytes_recd=0
           chunks=sock.recv(4096) # receives data sent by nodemcu
   
           chunks_list=[]
           chunks_list=chunks.split(",")
   
           st=chunks_list[0]
           print st
           raspberry_id="1"
           send_noti="6"
           if st!="alive": 
               faulty_nmcu.append(ip_list[i]) # unrechable ips are appended into the list
           
           
       except socket.timeout:
           print "time out"
           faulty_nmcu.append(ip_list[i])
           continue
   print faulty_nmcu
   return faulty_nmcu

   
faulty_nmcu=run_sensor_status()
for row in faulty_nmcu: # iterates through each faulty nodemcu ip
   data={"nodemcu_id":row[0],"raspberry_id":1,"nodemcu_ip":row[1],"raspberry_ip":"169.254.152.165","email":"rashmipawar921@gmail.com"} # creates dictionary of current values to be sent to server
                   
   json_data = json.dumps(data) # converts dictionary to json
   r = requests.get(url = URL, json = json_data, headers = headers) # sends json data to the URI
print "data is updated to db"

