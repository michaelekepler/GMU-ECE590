import socket

rasp_ip = "10.159.130.58"
comp_ip = "10.159.114.247"
port = 5001
image = " "

#Initialize the socket
comp_sock = socket.socket(socket.AFINET, socket.SOCK_DGRAM)

#Send the image
comp_sock.sendto(image, (rasp_ip, port))    

#Close the socket
comp_sock.close()

