import os

#Path Information
path = "/home/student/Downloads/"
name = "robot.png" 

#Get the size of the file
size =  os.path.getsize( path + name )
print "The size of the image is: ", size, "Bytes"

#Determine number of chunks
bytesPerChunk = 32768
chunks = size / bytesPerChunk
left_over_chunk = size % 32768

#Open files for reading and writing
image_read = open(path + name, 'r')
image_write = open(path + "tx_"+ name, 'w')

#Copy the image into a new file
count = 0
#For chunks of 32768 bytes
while (count < chunks):
	line = image_read.read(bytesPerChunk)
	image_write.write(line)
	count = count + 1
#For the remaining bytes
line = image_read.read(left_over_chunk)
image_write.write(line)


#Open the file on the PI to write the image & write it
#image = open(image_path+image_name,'wb')
#linecount=0
#while True: 
#    line = comp_sock.recv(1024)  #Write the image line by line
##    comp_sock.settimeout(2)
##    if line == "END":
#    if not line: 
#        break
#    image.write(line)
#    linecount =  linecount +1
#    print "writing line " + str(linecount)
#image.close()
#print "Image Received"
#
##Close socket
#comp_sock.close()
