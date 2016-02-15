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

    #Recive confirmation to start tx (sync Rx and Tx programs)
    start = cpu2pi_sock.recv(512)

    #Alternate images for transmission
    tx_count = tx_count + 1
    if (tx_count % 2 == 1):
        img_path = img1_path
        img_name = img1_name
    else:
        img_path = img2_path
        img_name = img2_name
    
    #Transmission Information
    size = os.path.getsize( img_path + img_name )
    bytes_per_chunk = 32768
    chunks = size / bytes_per_chunk
    left_over_chunk = size % bytes_per_chunk
    
    #Send the image information to the computer
    print "sending image name"
    pi2cpu_sock.sendto(img_name,(comp_ip, pi2cpu_port))
    print "sending bytes per chunk"
    pi2cpu_sock.sendto(str(bytes_per_chunk),(comp_ip, pi2cpu_port))
    print "sending number of chunks"
    pi2cpu_sock.sendto(str(chunks),(comp_ip, pi2cpu_port))
    print "sending left_over_chunk size"
    pi2cpu_sock.sendto(str(left_over_chunk),(comp_ip, pi2cpu_port))
    print "sending image size"
    pi2cpu_sock.sendto(str(size),(comp_ip, pi2cpu_port))
    
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
        print "chunk %i" %(count+1)
        pi2cpu_sock.sendto(line, (comp_ip, pi2cpu_port))
        end_t = time.time()
        time_dur = time_dur + (end_t-start_t)
        count = count + 1
    line = img.read(left_over_chunk)
    start_t = time.time()
    print "Sending Remainder"
    pi2cpu_sock.sendto(line, (comp_ip, pi2cpu_port))
    end_t = time.time()
    time_dur = time_dur + (end_t - start_t)

    #Close image file
    img.close()
    
    #Print transmission stats
    bit_rate = (size*8)/time_dur
    print "%i)Size(bytes): %i \tTx Duration(ms): %2.2f \tBit Rate(Mbps): %2.2f \tFrequency(Hz): %1.2f\t Image: %s" %(tx_count, size, (time_dur*1000), (bit_rate/1000000),(1/tx_dur), img_name)
    
    #Recive confirmation of end transmission (for Rx Tx sync purposes)
    end = cpu2pi_sock.recv(512)

    #For transmission frequency of ~5Hz
    time.sleep(0.17)

#Close the socket
pi2cpu_sock.close()
cpu2pi_sock.close()
