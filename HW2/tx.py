import socket
import time
import sys

UDP_IP = "10.159.130.58"    #IP address of RaspPI
UDP_PORT = 5005


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

end_loop = False
while (end_loop == False):
	#Input Commands
	print('________________________________________________________________________________')
	l_pos = input('Enter Left Wheel Position:')
	r_pos = input('Enter Right Wheel Position:')
 	
	#Check for valid input
	if not(l_pos >= 0) or not(r_pos >= 0):
		end_loop = True
	else:
		#Command Packet
		Command = 'Left:'+str(l_pos)+'!'+'Right:'+str(r_pos)
		num_bits = sys.getsizeof(Command) * 8    #8 bits/byte	

		#Transmit Packet
		tx_start = time.time()
		sock.sendto(Command, (UDP_IP, UDP_PORT))
		tx_end = time.time()

		#Bit Rate Calculation
		tx_dur = tx_end - tx_start
		bit_rate = num_bits/tx_dur

		#Output Statistics
		print '\nLeft Command:%.2f \tRight Command:%.2f \tPacket size(bits):%i \tTx_duration(ms):%0.6f \tBit Rate (Mbits/s):%2.2f' %(l_pos, r_pos, num_bits, tx_dur*1000, bit_rate/1000000)

#Close the socket
sock.close()  
