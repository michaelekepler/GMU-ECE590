import socket
import os

#UDP Information
comp_ip = "192.168.10.80"
port = 5001

#Initialize the socket 
# and bind it to the receiving IP and port
comp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
comp_sock.bind((comp_ip,port))

#Image Information
download_path = "/home/student/Downloads/"
image_name, addr = comp_sock.recvfrom(1024)
bytes_per_chunk, addr = comp_sock.recvfrom(1024)
chunks, addr = comp_sock.recvfrom(1024)
left_over_chunk, addr = comp_sock.recvfrom(1024)
size, addr = comp_sock.recvfrom(1024)
print "\nReceiving the image: ", image_name
print "Size: ", size, " bytes"
print "Chunk size: ", bytes_per_chunk
print "Number of full Rx chunks: ", chunks
print "Number of bytes in the remaining chunk: ", left_over_chunk

#Open the file on the PI to write the image & write it
image = open(download_path+"downloaded_"+image_name,'w')
chunk_count=0
while (chunk_count < int(chunks)):
	print "Receiving Chunk " + str(chunk_count+1) 
	line = comp_sock.recv(int(bytes_per_chunk))  #Write the image line by line
	image.write(line)
	chunk_count = chunk_count + 1
print "Receiving remaining bytes"
line = comp_sock.recv(int(left_over_chunk))

image.write(line)
print "Succesfully wrote the image: " + download_path + "downloaded_" + image_name

#Close image file
image.close()

#Close the socket
comp_sock.close()

