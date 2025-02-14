# Python code to convert an image to ASCII image.
import sys, random, argparse
import numpy as np
import math

from PIL import Image




gscale = ["J","n","--"]

#gscale = ['||','!!','x','*','::','| ','! ',': ','..','. ','  '] # old don't use
#gscale = ["$","8","o","b","d","p","q","0","L","u","n","1","+","'''"] # old don't use
def id_to_time_format(id):

    return int(id * 1.001)





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
    global gscale

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
    rows = round(H / h)

    #print("cols: %d, rows: %d" % (cols, rows))
    #print("tile dims: %d x %d" % (w, h))

    # check if image size is too small
    if cols > W or rows > H:
        print("Image too small for specified cols!")
        return

    # ascii image is a list of character strings
    aimg = []
    himg = []
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

from collections import Counter

def most_common_object(input_list):
    # Use Counter to count occurrences of each object in the list
    counts = Counter(input_list)
    
    # Get the most common object and its count
    most_common_item = counts.most_common(1)[0][0]
    count = counts.most_common(1)[0][1]
    
    return most_common_item, count

def convert_data_to_ytt(start,end,aimg,RGB,rowheight,coloraccuracy,colorlist : list,Op_level : int, single_char_mode : bool):
    r_data = f'<p t="{int(start)}" d="{int(end)}" wp="1" ws="1">'
    c_data : list = []
    r=[]
    colordiv = coloraccuracy * 15.875
    if (colordiv == 0):
        colordiv = 1
    for rowi in range(len(aimg)-1):
        r = []
        done_charis = -1
        for chari in range(len(aimg[rowi])-1):
            if done_charis >= chari:
                continue
            for chari2 in range(len(aimg[rowi])-chari):
                if (abs(int(RGB[rowi][chari][0]/colordiv)-int(RGB[rowi][chari+chari2][0]/colordiv)) <= 5-Op_level) and (abs(int(RGB[rowi][chari][1]/colordiv)-int(RGB[rowi][chari2+chari][1]/colordiv)) <= 5-Op_level) and (abs(int(RGB[rowi][chari][2]/colordiv)-int(RGB[rowi][chari2+chari][2]/colordiv)) <= 5-Op_level):
                    c_data.append("0")
                else:
                    break
            new_c_data : list = []
            avgcolor_R = 0
            avgcolor_G = 0
            avgcolor_B = 0
                 
            for colori in range(len(c_data)):
                avgcolor_R += RGB[rowi][chari+colori][0]
                avgcolor_G += RGB[rowi][chari+colori][1]
                avgcolor_B += RGB[rowi][chari+colori][2]

            avgcolor_R = (avgcolor_R/(len(c_data)))
            avgcolor_G = (avgcolor_G/(len(c_data)))
            avgcolor_B = (avgcolor_B/(len(c_data)))
            
            
            if (not single_char_mode):
                avgcolorlight = (avgcolor_R+avgcolor_G+avgcolor_B)/3
                for chari3 in range(len(c_data)):
                    chariavglight = ((RGB[rowi][chari3+chari][0]+RGB[rowi][chari3+chari][1]+RGB[rowi][chari3+chari][2])/3)
                    difference = round((chariavglight-avgcolorlight))
                    if (difference > 1):
                        difference = 1
                    elif (difference < 0 & difference > -2):
                         difference = 0
                    elif (difference < -2):
                        difference = -1
                        
                    new_c_data.append(gscale[1-difference])
            else:
                 new_c_data = c_data

            avgcolor_R = int(avgcolor_R/colordiv)
            avgcolor_G = int(avgcolor_G/colordiv)
            avgcolor_B = int(avgcolor_B/colordiv)

            if [avgcolor_R,avgcolor_G,avgcolor_B] in colorlist:
                r.append(colorlist.index([avgcolor_R, avgcolor_G, avgcolor_B]))
            else:
                colorlist.append([avgcolor_R, avgcolor_G, avgcolor_B])
                r.append(len(colorlist)-1)
            

            r_data += f'<s p="1"></s><s p="{(int)(r[0])}">{"".join(new_c_data)}</s>'
            done_charis = chari+(len(c_data)-1)
            c_data = []
            r = []
        r_data += "\n"
    r_data += '<s p="1"></s></p>\n'
    return r_data, colorlist

# main() function
def convert(frame, frame_num, ms_per_frame, clms, submilisecondoffset,coloraccuracy,colorlist, Op_Level, ScreenRatio, single_char_mode:bool):
	rtn = []

	# set scale default as 0.65 which suits
	# the Roboto Regular font
	if single_char_mode:
		scale = 0.75 * ScreenRatio
	else:
		scale = 0.76 * ScreenRatio

	if clms:
		cols = int(clms)
	else:
		print("No collums inputed")

	# convert image to ascii txt
	aimg, RGB, rowh = convertImageToAscii(frame, cols, scale)
    
	ms_pos = frame_num * ms_per_frame
	return convert_data_to_ytt(ms_pos + submilisecondoffset, ms_per_frame,aimg,RGB,rowh,(int)(coloraccuracy),colorlist, Op_Level, single_char_mode)


