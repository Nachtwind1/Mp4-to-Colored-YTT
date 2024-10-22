import convert_to_ascii
import convert_to_png
import os
import argparse

parser = argparse.ArgumentParser(description="mp4 to srt")

# add expected arguments
parser.add_argument('--file', dest='file', required=True)
parser.add_argument('--collums', dest='collums', required=True)
parser.add_argument('--msoffset', dest='msoffset', required=False)
parser.add_argument('--submsoffset', dest='submsoffset', required=False)
parser.add_argument('--idoffset', dest='idoffset', required=False)
parser.add_argument('--coloraccuracy', dest='coloraccuracy', required=True)
parser.add_argument('--scale', dest='scale', required=False)

args = parser.parse_args()
if args.file != "":
    file = args.file
else:
    print("no file")

if args.coloraccuracy != "":
    coloraccuracy = args.coloraccuracy
else:
    print("no coloraccuracy set")

if args.scale != "":
    scale = args.scale
else:
    scale = "1"
    
def convert_to_hex(rgb):
    # Convert float values to integers
    rgb_int = [int(x) for x in rgb]
    
    # Convert integers to hexadecimal strings
    hex_str = "#{:02X}{:02X}{:02X}".format(*rgb_int)
    
    return hex_str

#Janky Code

# Use given if it is Truthy, 0 if it is Falsey (empty string)
idoffset = int(args.idoffset or 0)
milisecondsoffset = int(args.msoffset or 0)

submilisecondoffset = int(args.submsoffset or 0)


if os.path.exists(file):
    ms_per_frame, total_frames, frames = convert_to_png.convert(file, milisecondsoffset, idoffset)
else:
    print("found no file at that location")


if os.path.exists(file) & (args.file != "") & (args.coloraccuracy != "") & ((args.coloraccuracy != "0") | (args.coloraccuracy != 0)):
    colorlist = []
    srt = []
    print('Generating Ascii art')
    for x in range(total_frames):
        convert_to_png.print_progress_bar(x + 1, total_frames)
        srtf, colorlist = convert_to_ascii.convert(frames[x], x, ms_per_frame, args.collums, submilisecondoffset,coloraccuracy,colorlist)
        srt.append(srtf)

    print()
    prefix = """<?xml version="1.0" encoding="utf-8"?>
<timedtext format="3"><head>
<wp id="0" ap="7" ah="0" av="0" />
<wp id="1" ap="7" ah="50" av="100" />
<ws id="0" ju="2" pd="0" sd="0" />
<ws id="1" ju="2" pd="0" sd="0" />"""
    for i in range(len(colorlist)-1):
        colorhex = convert_to_hex([int(colorlist[i][0]*15.875),int(colorlist[i][1]*15.875),int(colorlist[i][2]*15.875)])
        prefix += f'<pen id="{i+6}" sz="{100*float(scale)}" fc="{colorhex}" fo="255" bo="0" />\n'
    prefix += '''</head>
<body>'''
    writestring = prefix + "\n".join(srt) + '''</body></timedtext>'''
    #write to file
    open("output/subtitles.ytt","w").write(writestring)

