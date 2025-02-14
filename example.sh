echo "put your Input.mp4 in this folder"
read -p "Press Enter to continue"

python3 main.py --file "./input.mp4" -collums 64 --coloraccuracy 2 --scale 0.5

echo "that was it, you should have a .YTT file in the output folder"
