#!/usr/bin/python -O
from __future__ import print_function

import time, cv2, shared
import shared.udp as udp
import shared.camera as cam

transport = udp.UdpSocket(shared.PC_CAM_ADDR)
capture = cv2.VideoCapture(0)

PERIOD = 1.0/10

try:
	while True:
		next_time = time.time() + PERIOD
		success, image = capture.read()
		if not success:
			print("Warning: Couldn't read video frame!")
			continue
		image = cv2.resize(image, (320, 240))
		transport.send_big(cam.img2bufz(image))
		throttle_delay = next_time - time.time()
		if throttle_delay > 0: time.sleep(throttle_delay)
except KeyboardInterrupt:
	capture.release()