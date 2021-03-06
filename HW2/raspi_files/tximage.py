##########################################################################
#
#    Program for continuous UDP transmission of images from one computer
#    to another, more specifically from the Raspberry Pi to the Linux
#    Virtual Machine.
#
#    This program acts as the transmitter of the image
#    The program that serves as the receiver can be found at:
#       /home/pi/GMU-ECE590/HW2/vm_files/rx_image.py
#
#    To successfully transmit and receive a image:
#           1) Update the programs to suit your machines for the following
#              parameters:
#                    a) Ip addresses
#                    b) ports
#                    C) path of the image
#           2) Run rx_image.py on the receiving machine
#           3) Run tx_image.py on the transmitting machine
#
#    Notes of caution:
#           1) The program will stall if the image window is clicked
#
##########################################################################



import socket
import time
import os

#UDP Information
rasp_ip = "192.168.10.81"
comp_ip = "192.168.10.80"
pi2cpu_port = 5001
cpu2pi_port = 5002 

#Initialize the socket
pi2cpu_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #Tx port
cpu2pi_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #Rx port
cpu2pi_sock.bind((rasp_ip, cpu2pi_port))

#Image Information
img1_path = "/home/pi/Downloads/"
img1_name = "robot2.bmp"
img2_path = "/home/pi/Downloads/"
img2_name = "robot2_gray.bmp"

tx_count = 0
prev_time = 0    #Time of previous image transmission, used to obtain frequency

while True:    
    tx_count = tx_count + 1
    

    #Alternate images for transmission
    if (tx_count % 2 == 1):
        img_path = img1_path
        img_name = img1_name
    else:
        img_path = img2_path
        img_name = img2_name
    
    #Send the image information to the computer
    size = os.path.getsize(img_path + img_name )
    pi2cpu_sock.sendto(img_name,(comp_ip, pi2cpu_port))

    bytes_per_chunk = 32768
    pi2cpu_sock.sendto(str(bytes_per_chunk),(comp_ip, pi2cpu_port))

    chunks = size / bytes_per_chunk
    pi2cpu_sock.sendto(str(chunks),(comp_ip, pi2cpu_port))

    left_over_chunk = size % bytes_per_chunk
    pi2cpu_sock.sendto(str(left_over_chunk),(comp_ip, pi2cpu_port))

    size = os.path.getsize(img_path + img_name )
    pi2cpu_sock.sendto(str(size),(comp_ip, pi2cpu_port))

    proceed1 = cpu2pi_sock.recv(512)
    
    #Send the image to the computer, (Transmit file in chunks)
    img = open(img_path + img_name, 'r')
    count = 0

    curr_time = time.time()
    tx_dur = curr_time - prev_time
    prev_time = curr_time

    time_dur=0      #time duration of each individual transmission
    while (count < chunks):
        line = img.read(bytes_per_chunk)
        start_t = time.time()
        time.sleep(0.0125)
        pi2cpu_sock.sendto(line, (comp_ip, pi2cpu_port))
        end_t = time.time()
        time_dur = time_dur + (end_t-start_t)
        count = count + 1
    line = img.read(left_over_chunk)
    time.sleep(0.0125)
    start_t = time.time()
    pi2cpu_sock.sendto(line, (comp_ip, pi2cpu_port))
    end_t = time.time()
    time_dur = time_dur + (end_t - start_t)

    #Close image file
    img.close()
    
    #Print transmission stats
    bit_rate = (size*8)/time_dur
    print "TX-%i)Size(bytes): %i \tTx Duration(ms): %2.2f \tBit Rate(Mbps): %2.2f \tFrequency(Hz): %1.2f\t Image: %s" %(tx_count, size, (time_dur*1000), (bit_rate/1000000),(1/tx_dur), img_name)
    
    proceed2 = cpu2pi_sock.recv(528)

    #For transmission frequency of ~5Hz
#    time.sleep(0.03)

#Close the socket
pi2cpu_sock.close()
cpu2pi_sock.close()
