#########################################################################
#
#    Program for continuous UDP transmission of images from one computer
#    to another, more specifically from the Raspberry Pi to the Linux 
#    Virtual Machine.
#
#    This program acts as the reciever of the image
#    The program that serves as the transmitter can be found at:
#	/home/student/GMU-ECE590/HW2/vm_files/rx_image.py
#
#    To successfully transmit and recieve an image:
#       1) Update the programs to suit your machines for the following parameters:
#		a) Ip addresses
#		b) ports
#		c) path of the image
#	2) Run the rx_image.py on the receiving machine
#	3) run the tx_image.py on the transmitting machine 
#
###################################################################

import socket
import os
import numpy
import cv2
import time

#UDP Information
rasp_ip = "192.168.10.81"
comp_ip = "192.168.10.80"
pi2cpu_port = 5001
cpu2pi_port = 5002

#Initialize the socket 
# and bind it to the receiving IP and port
cpu2pi_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #Tx Port
pi2cpu_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #Rx Port
pi2cpu_sock.bind((comp_ip,pi2cpu_port))

download_path = "/home/student/Downloads/"
rx_count = 0

while True:
        rx_count = rx_count + 1	

	#Image Information
	image_name = pi2cpu_sock.recv(512)
	bytes_per_chunk = pi2cpu_sock.recv(512)
	chunks= pi2cpu_sock.recv(512)
	left_over_chunk = pi2cpu_sock.recv(512)
	size = pi2cpu_sock.recv(512)

	bytes_per_chunk = int(bytes_per_chunk)
	chunks = int(chunks)
	left_over_chunk = int(left_over_chunk)
	size = int(size)
	
	cpu2pi_sock.sendto("proceed1", (rasp_ip, cpu2pi_port))

	#Open the file on the PI to write the image & write it
	image = open(download_path+'img_feed','w')
	chunk_count=0

	while (chunk_count < chunks):
		chunk = pi2cpu_sock.recv(bytes_per_chunk)
		image.write(chunk)
		chunk_count = chunk_count + 1
	remainder = pi2cpu_sock.recv(left_over_chunk)
	image.write(remainder)
	
	#Close image file
	image.close()

	#View the image feed
	CVimg = cv2.imread(download_path+'img_feed',1)
	cv2.imshow('Image feed', CVimg)
	cv2.waitKey(10)
        
	cpu2pi_sock.sendto("proceed2", (rasp_ip, cpu2pi_port))
	#For transmission frequency of ~5Hz
#	time.sleep(0.03)

#Close the sockets
pi2cpu_sock.close()
cpu2pi_sock.close()
