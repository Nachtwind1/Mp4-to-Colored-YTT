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
--file | true | the Input file, can be any video file | 
--collums | true | how many collums in width, 32 recommended | 
--coloraccuracy | true | how many different colors there are, 0 (all 8 bit colors) to 5 (either black or white) | 
--op | false | optimization level, goes from 5 (no optimization) to 0 (as much optimization as possible) | 2
--msoffset | false | after how many milliseconds the subtitles start | 0
--scale | false | the configured size in the .ytt file | 1
--maxfps | false | at how many fps the subtitles should run, set this to 5 if the video lags | same as file
--single_char_mode | false | if the programm should use multiple characters or just one (0) | true

example (this one works best with saturated colors):
```
python main.py --file "video.mp4" --collums 32 --coloraccuracy 3 --op 4 --maxfps 5
```

## known Issues
Issues with youtube:
  -doesn't load on mobile Devices
  -can lag out if collums are set to high
Issues with this tool:
  -code is almost unreadable and pretty unoptimized for speed
