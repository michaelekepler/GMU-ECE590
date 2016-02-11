import socket

UDP_IP ="10.159.130.58"    #IP address of the RaspPI 
UDP_PORT= 5005

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

while True: 
	#Receive Packet
	print('___________________________________________________________________')
	packet, addr = sock.recvfrom(1024)  #Buffer size is 1024 bytes
	
	#Format of data packet: Left:###!Right:###
	[Left, Right] = packet.split('!')
	[L_check,L_pos] = Left.split(':')
	[R_check,R_pos] = Right.split(':')
	
	#Check the validity of the packet
	if (L_check == "Left") and (R_check == "Right"):
		LW_pos = int(L_pos)
		RW_pos = int(R_pos)
		print'Left Wheel Position:%i Position Doubled:%i' %(LW_pos,2*LW_pos)
		print'Right Wheel Position:%i Position Doubled:%i\n' %(LW_pos,2*LW_pos)
	else:
		print'Packet Corrupted, Positions not Updated'
	print "Recieved Packet:", packet, " from ", addr, '\n'
        print socket.gethostname()

