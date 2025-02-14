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

example:
```
python main.py --file "video.mp4" --collums 32 --coloraccuracy 2 --scale 0.5
```
