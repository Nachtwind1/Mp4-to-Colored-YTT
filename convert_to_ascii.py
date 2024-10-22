# Python code to convert an image to ASCII image.
import sys, random, argparse
import numpy as np
import math

from PIL import Image




# 10 levels of grey
gscale2 = ['||','!!','x','*','::','| ','! ',': ','..','. ','  ']
#gscale2 = '$8obdpq0Lun1+ '
def id_to_time_format(id):
    return int(id + 1)

def getAverageL(image):

	"""
	Given PIL Image, return average value of grayscale value
	"""
	# get image as numpy array
	im = np.array(image)

	# get shape
	w,h = im.shape

	# get average
	return np.average(im.reshape(w*h))

def getEqualWidthScale(scale, width):
    equal_width_scale = ""
    for char in scale:
        equal_width_scale += char + " " * (width - 1)
    return equal_width_scale

def convertImageToAscii(frame, cols, scale):
    """
    Given Image and dims (rows, cols) returns an m*n list of Images 
    """
    # declare globals
    global gscale1, gscale2

    # open image and convert to grayscale
    image = frame.convert('L')

    # store dimensions
    W, H = image.size[0], image.size[1]
    #print("input image dims: %d x %d" % (W, H))

    # compute width of tile
    w = W / cols

    # compute tile height based on aspect ratio and scale
    h = w / scale

    rowh = (h / H) * 3
    # compute number of rows
    rows = int(H / h)

    #print("cols: %d, rows: %d" % (cols, rows))
    #print("tile dims: %d x %d" % (w, h))

    # check if image size is too small
    if cols > W or rows > H:
        print("Image too small for specified cols!")
        return

    # ascii image is a list of character strings
    aimg = []
    himg = []
    iimg = []
    allrgb = []

    # generate list of dimensions
    for j in range(rows):
        RGB = []
        y1 = int(j * h)
        y2 = int((j + 1) * h)

        # correct last tile
        if j == rows - 1:
            y2 = H

        for i in range(cols):

            # crop image to tile
            x1 = int(i * w)
            x2 = int((i + 1) * w)

            # correct last tile
            if i == cols - 1:
                x2 = W

            # crop image to extract tile
            img = frame.crop((x1, y1, x2, y2))

            rgb_imgage = img.convert('RGB')
            Red, Green, Blue = rgb_imgage.split()
            
            Red,Green,Blue = most_common_object(Red.getdata())[0],most_common_object(Green.getdata())[0],most_common_object(Blue.getdata())[0]

            
            RGB.append([(int)(Red),(int)(Green),(int)(Blue)])
            # append ascii char to array
            aimg.append("#")

            

        himg.append(0.0)
        aimg.append('\n')
        allrgb.append(RGB)

    # return txt image
    return "".join(aimg).split("\n"), allrgb, rowh

# /$$$$$$$   /$$$$$$  /$$$$$$$         /$$$$$$   /$$$$$$  /$$$$$$$  /$$$$$$$$
#| $$__  $$ /$$__  $$| $$__  $$       /$$__  $$ /$$__  $$| $$__  $$| $$_____/
#| $$  \ $$| $$  \ $$| $$  \ $$      | $$  \__/| $$  \ $$| $$  \ $$| $$      
#| $$$$$$$ | $$$$$$$$| $$  | $$      | $$      | $$  | $$| $$  | $$| $$$$$   
#| $$__  $$| $$__  $$| $$  | $$      | $$      | $$  | $$| $$  | $$| $$__/   
#| $$  \ $$| $$  | $$| $$  | $$      | $$    $$| $$  | $$| $$  | $$| $$      
#| $$$$$$$/| $$  | $$| $$$$$$$/      |  $$$$$$/|  $$$$$$/| $$$$$$$/| $$$$$$$$
#|_______/ |__/  |__/|_______/        \______/  \______/ |_______/ |________/
from collections import Counter

def most_common_object(input_list):
    # Use Counter to count occurrences of each object in the list
    counts = Counter(input_list)
    
    # Get the most common object and its count
    most_common_item = counts.most_common(1)[0][0]
    count = counts.most_common(1)[0][1]
    
    return most_common_item, count

def convert_data_to_ytt(start,end,aimg,RGB,rowheight,coloraccuracy,colorlist):
    r_data = f'<p t="{int(start)}" d="{int(end)}" wp="1" ws="1">'
    c_data= ""
    r=[]
    rgbrow = []
    for rowi in range(len(aimg)-1):
        r = []
        for chari in range(len(aimg[rowi])):
            if ((math.fmod(chari, coloraccuracy)) == 0):
                run = False
                for i1 in range(-1,1):
                    for i2 in range(-1,1):
                        for i3 in range(-1,1):
                            if [int(RGB[rowi][chari][0]/15.875+i1),int(RGB[rowi][chari][1]/15.875+i2),int(RGB[rowi][chari][2]/15.875+i3)] in colorlist:
                                r.append(colorlist.index([int(RGB[rowi][chari][0]/15.875+i1), int(RGB[rowi][chari][1]/15.875+i2), int(RGB[rowi][chari][2]/15.875+i3)]))
                                run = True
                                break
                        if run:
                            break
                    if run:
                        break
                if run == False:
                    colorlist.append([int(RGB[rowi][chari][0]/15.875+i1), int(RGB[rowi][chari][1]/15.875+i2), int(RGB[rowi][chari][2]/15.875+i3)])
                    r.append(colorlist.index([int(RGB[rowi][chari][0]/15.875+i1), int(RGB[rowi][chari][1]/15.875+i2), int(RGB[rowi][chari][2]/15.875+i3)]))
                

            if (math.fmod(chari, coloraccuracy)) == coloraccuracy-1:
                c_data = "#"*coloraccuracy
                r_data += f'<s p="1"></s><s p="{(int)(most_common_object(r)[0])+6}">{c_data}</s>'
                c_data= ""
                r = []
        r_data += "\n"
    r_data += '<s p="1"></s></p>\n'
    return r_data, colorlist

# main() function
def convert(frame, frame_num, ms_per_frame, clms, submilisecondoffset,coloraccuracy,colorlist):
	rtn = []

	# set scale default as 0.43
	scale = 0.43


	if clms:
		cols = int(clms)
	else:
		print("ERROR"*1000)

	# convert image to ascii txt
	aimg, RGB, rowh = convertImageToAscii(frame, cols, scale)
    
	ms_pos = frame_num * ms_per_frame
	return convert_data_to_ytt(ms_pos + submilisecondoffset, ms_per_frame+1,aimg,RGB,rowh,(int)(coloraccuracy),colorlist)


