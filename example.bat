@ECHO OFF
echo 'put your Input.mp4 in this folder and then just press enter on this console'

pause
@ECHO ON
python main.py --file "Input.mp4" --collums 64 --coloraccuracy 2 --scale 0.5

@ECHO OFF
echo "that was it, you should have a .YTT file in the output folder"
pause