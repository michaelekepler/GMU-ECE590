import socket
import time
import os

#UDP Information
comp_ip = "192.168.10.80"
port = 5001

#Initialize the socket
rasp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

#Image Information
image_path = "/home/pi/Downloads/"
image_name = "robot.png"
size = os.path.getsize( image_path + image_name )

bytes_per_chunk = 32768
chunks = size / bytes_per_chunk
left_over_chunk = size % bytes_per_chunk
print "\nImage:\t\t\t ", image_path, image_name
print "Size:\t\t\t ", size, "Bytes"
print "File chunks:\t\t ", chunks
print "Bytes in last chunk:\t ", left_over_chunk

#Send the image information to the computer
print "\nSending image information to the computer"
rasp_sock.sendto(image_name,(comp_ip, port))
rasp_sock.sendto(str(bytes_per_chunk),(comp_ip, port))
rasp_sock.sendto(str(chunks),(comp_ip, port))
rasp_sock.sendto(str(left_over_chunk),(comp_ip, port))
rasp_sock.sendto(str(size),(comp_ip, port))

#Open the the image to read
print '\nOpening image: ' + image_path + image_name
image = open(image_path + image_name, 'r')

#Send the image to the PI, (Transmit file in parts)i
print "\nTransmitting file to the Pi:\n"
count = 0
while (count < chunks):
    print "Transmitting chunk " +str(count+1)
    line = image.readline(bytes_per_chunk)
    rasp_sock.sendto(line, (comp_ip, port))
    count = count + 1
line = image.read(left_over_chunk)
print "Transmitting remaining bytes"
rasp_sock.sendto(line, (comp_ip, port))
print "\nSuccessfully transmitted the image"

#Close image file
image.close()

#Close the socket
rasp_sock.close()

