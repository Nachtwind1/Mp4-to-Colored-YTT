# Please Give Credit
if you use this to make a video then please link to this in the comments or description, thanks!
## Requirements with their install commands

### CV2
```bash
pip install opencv-python
```
### Pillow
```bash
pip install pillow
```
### Numpy
```bash
pip install numpy
```

To install all paste and run this
```bash
pip install pillow
pip install numpy
pip install opencv-python
```

## How To use
just run the main.py with python using these arguments
Argument | Required | Description | Default | 
------------- | ------------- | ------------- | -------------
--file | yes | the Input file, can be any video file | 
--collums | yes | how many collums in width, 32 recommended | 
--coloraccuracy | yes | how many different colors there are, 0 (all 8 bit colors) to 5 (either black or white) | 
--op | no | optimization level, goes from 5 (no optimization) to 0 (as much compression as possible, not recommended) | 3
--msoffset | no | after how many milliseconds the subtitles start | 0
--scale | no | the configured size in the .ytt file | 1
--maxfps | no | at how many fps the subtitles should run, set this to 5 if the video lags | same as file
--single_char_mode | no | if the programm should use multiple characters or just one (0) | true
--colorfix | no | apply a colorfix | false

example (this one works best with saturated colors):
```
python main.py --file "video.mp4" --collums 32 --coloraccuracy 3 --op 4 --maxfps 5
```
Videos generated with this:
[![Doom but it's colored subtitles](https://img.youtube.com/vi/97vwGmC0_L4/maxresdefault.jpg)](https://youtu.be/97vwGmC0_L4)

```
python main.py --file doom.mp4 --collums
 48 --coloraccuracy 2 --maxfps 5 --op 4 --single_char_mode False --scale 0.5 --colorfix true
```

## known Issues
### Issues with youtube: 
    doesn't load on mobile Devices, can lag out if collums are set to high
### Issues with this tool: 
    code is almost unreadable and pretty unoptimized for speed, the aspect Ratio not being right
