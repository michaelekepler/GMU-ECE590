import os 

#Display Original Robot Image and size of file
os.system("eog /home/student/Downloads/robot.bmp &")
print "size of robot.bmp in bytes:" +str(os.path.getsize("/home/student/Downloads/robot.bmp"))

#Open Robot image file and extract the contents
with open("/home/student/Downloads/robot.bmp", 'r') as image_file:
	file_contents = image_file.read()

#Write the Image contents to a new file, copy_robot
new_image_file = open("/home/student/Downloads/copy_robot.bmp",'w')
new_image_file.write(file_contents)

#Display copy_robot
os.system("eog /home/student/Downloads/copy_robot.bmp &")
print "size of copy_robot.bmp in bytes:" +str(os.path.getsize("/home/student/Downloads/copy_robot.bmp"))


#Close image objects
image_file.close()
new_image_file.close()

