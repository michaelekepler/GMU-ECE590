from __future__ import print_function

import numpy, cv2
if cv2.__version__.startswith('$Rev'):
	print("Error: OpenCV 2.4 is required", file=sys.stderr)
	raise ImportError("cv2.imencode has the incorrect signature")

# Image compression for network transport
IMG_DTYPE = numpy.uint8
IMGZ_QUALITY = 50 # Jpeg quality from 0 to 100 (higher is better but bigger)
IMG_WIDTH = 320
IMG_HEIGHT = 240

def img2bufz(img): return cv2.imencode(".jpeg", img, (cv2.IMWRITE_JPEG_QUALITY, IMGZ_QUALITY))[1].tostring()
def bufz2img(buf): return cv2.imdecode(numpy.frombuffer(buf, IMG_DTYPE), cv2.IMREAD_COLOR)

# Color tracking
BLUE_MAX  = numpy.array((120 + 15, 255, 255), IMG_DTYPE)
BLUE_MIN  = numpy.array((120 - 30, 150,   0), IMG_DTYPE)
ORANGE_MAX = numpy.array((25,255,255), IMG_DTYPE)
ORANGE_MIN = numpy.array((5,128, 0), IMG_DTYPE)

RGB2HSV_FLAG = cv2.COLOR_BGR2HSV

def create_mask_blue(image):
	image = cv2.cvtColor(image, RGB2HSV_FLAG)
	return cv2.inRange(image, BLUE_MIN, BLUE_MAX)
def create_mask_orange(image):
	image = cv2.cvtColor(image, RGB2HSV_FLAG)
	return cv2.inRange(image, ORANGE_MIN, ORANGE_MAX)

# Object detection - returns (x, y, onscreen:True/False)
def find_object_center(image):
	[ys, xs] = image.nonzero()
	print("\x1b[0KFound", len(ys), "pixels positive")
	if len(ys) < 500: return (0, 0, False)
	x =  xs.mean() / (IMG_WIDTH  / 2.0) - 1.0
	y = -ys.mean() / (IMG_HEIGHT / 2.0) + 1.0
	return (x, y, True)

def draw_marker(image, x, y, color):
	x =  (x + 1.0) * (IMG_WIDTH  / 2.0)
	y = -(y - 1.0) * (IMG_HEIGHT / 2.0)
	tl = (int(x) - 2, int(y) - 2)
	br = (int(x) + 3, int(y) + 3)
	cv2.rectangle(image, tl, br, color, cv2.cv.CV_FILLED)
