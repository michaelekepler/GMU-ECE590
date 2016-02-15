import socket
import os
import numpy
import cv2

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

while True:
	
	#Ask to begin transmission (for Rx Tx sync purposes)
	cpu2pi_sock.sendto("Start", (rasp_ip, cpu2pi_port))

	#Image Information
	download_path = "/home/student/Downloads/"
		
	image_name, addr = pi2cpu_sock.recvfrom(1024)
	print "recieving image name" + image_name
	bytes_per_chunk, addr = pi2cpu_sock.recvfrom(1024)
	bytes_per_chunk = int(bytes_per_chunk)
	print "receiving bytes per chunk" + str(bytes_per_chunk)
	chunks, addr = pi2cpu_sock.recvfrom(1024)
	chunks = int(chunks)
	print "receiveing number of chunks" + str(chunks)
	left_over_chunk, addr = pi2cpu_sock.recvfrom(1024)
	left_over_chunk = int(left_over_chunk)
	print "receiving size of left over chunk" + str(left_over_chunk)
	size, addr = pi2cpu_sock.recvfrom(1024)
	size = int(size)
	print "receiving size:" +str(size) 
	
	#Open the file on the PI to write the image & write it
	image = open(download_path+'img_feed','w')
	chunk_count=0
	while (chunk_count < chunks):
		print "Receiving Chunk " + str(chunk_count+1) 
		chunk = pi2cpu_sock.recv(bytes_per_chunk)  
		image.write(chunk)
		chunk_count = chunk_count + 1
	print "Receiving remaining bytes"
	remainder = pi2cpu_sock.recv(left_over_chunk)
	image.write(remainder)
	
	#Close image file
	image.close()
	
	#View the image feed
	CVimg = cv2.imread(download_path+'img_feed',1)
	cv2.imshow('Image feed', CVimg)
	cv2.waitKey(25)

	#Send confirmation of receive to sync transmissions
	print"Sending Confirmation"
	cpu2pi_sock.sendto("End", (rasp_ip, cpu2pi_port))	
	print "Confirmation Sent"

#Close the sockets
pi2cpu_sock.close()
cpu2pi_sock.close()
