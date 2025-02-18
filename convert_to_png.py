# Importing all necessary libraries 
import cv2 
from PIL import Image

# function to print an in-place progress bar (doesn't spam terminal and looks very clean)
def print_progress_bar(iteration, total):
    percent = "{:.1f}".format(100 * (iteration / float(total)))
    progress = f"Progress: {iteration}/{total} - {percent}%"
    print(progress, end='\r', flush=True)

def convert(vidfile, startms=0, idoffset=0, optional_fps=None):
    import cv2
    from PIL import Image

    frames = []

    cam = cv2.VideoCapture(vidfile)
    original_fps = cam.get(cv2.CAP_PROP_FPS)
    ms_per_frame = 1000 / original_fps

    # If optional_fps is provided, calculate the frame skipping step
    if optional_fps and optional_fps < original_fps:
        step = int(original_fps / optional_fps)  # Number of frames to skip
        ms_per_frame = 1000 / optional_fps
    else:
        step = 1  # Process all frames

    cam.set(cv2.CAP_PROP_POS_MSEC, startms + idoffset * ms_per_frame)

    pos_after_offset = int(cam.get(cv2.CAP_PROP_POS_FRAMES))
    total_frames = int(cam.get(cv2.CAP_PROP_FRAME_COUNT)) - pos_after_offset

    print('Extracting Frames')
    ScreenR = 0
    while True:
        frame_num = int(cam.get(cv2.CAP_PROP_POS_FRAMES)) - pos_after_offset
        print_progress_bar(frame_num // step, total_frames // step)

        ret, frame = cam.read()
        if not ret: break

        # Skip frames based on the step size
        if frame_num % step != 0:
            continue

        f = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        if not frames:
            ScreenR = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB).shape[1] /cv2.cvtColor(frame, cv2.COLOR_BGR2RGB).shape[0] 
        frames.append(f)
    print()

    cam.release()

    return ms_per_frame, len(frames), frames, ScreenR
