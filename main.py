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
parser.add_argument('--op', dest='optimisation', required=False)
parser.add_argument('--scale', dest='scale', required=False)
parser.add_argument('--maxfps', dest='fps', required=False)
parser.add_argument('--single_char_mode', dest='scm', required=False)

args = parser.parse_args()

scale = float(args.scale or 1)
scm = bool(args.scm or True)
fps = args.fps
if fps:
    fps = float(fps)

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
Op_Level = int(args.optimisation or 2)


if os.path.exists(args.file):
    ms_per_frame, total_frames, frames, ScreenRatio = convert_to_png.convert(args.file, milisecondsoffset, idoffset, fps)
else:
    print("found no file at that location")


if os.path.exists(args.file):
    colorlist = []
    srt = []
    print('Generating Ascii art')
    for x in range(total_frames):
        convert_to_png.print_progress_bar(x + 1, total_frames)
        srtf, colorlist = convert_to_ascii.convert(frames[x], x, ms_per_frame, args.collums, submilisecondoffset,args.coloraccuracy,colorlist,Op_Level,ScreenRatio, scm)
        srt.append(srtf)

    print()
    prefix = """<?xml version="1.0" encoding="utf-8"?>
<timedtext format="3"><head>
<wp id="0" ap="7" ah="0" av="0" />
<wp id="1" ap="7" ah="50" av="100" />
<ws id="0" ju="2" pd="0" sd="0" />
<ws id="1" ju="2" pd="0" sd="0" />
"""
    for i in range(len(colorlist)):
        colorhex = convert_to_hex([int(colorlist[i][0]*Op_Level*15.875),int(colorlist[i][1]*Op_Level*15.875),int(colorlist[i][2]*Op_Level*15.875)])
        prefix += f'<pen id="{i}" sz="{100*float(scale)}" fc="{colorhex}" fo="255" bo="0" />\n'
    prefix += '''</head>
<body>'''
    writestring = prefix + "\n".join(srt) + '''</body></timedtext>'''
    #write to file
    out_name = str(args.file).split("/")[-1].split(".")
    out_name_final = []
    for i in range(len(out_name)-1):
        out_name_final.append(out_name[i])
    out_name_final = "output/"+str(".".join(out_name_final))+".ytt"
    open(out_name_final,"w").write(writestring)

