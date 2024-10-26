import cv2
import os
import time
import argparse

parser = argparse.ArgumentParser(description='Extract frames from a video.')
parser.add_argument('--video-name', type=str, default='still.mp4', help='Name of the video file')

args = parser.parse_args()

video_name = args.video_name + '.mp4'
start_time = time.time()

video_location = 'videos'
video_path = os.path.join(video_location, video_name)
video_capture = cv2.VideoCapture(f"{video_path}")
frame_skip = 5
print(f"Starting the process. Video path: {video_location}/{video_name}")


if not video_capture.isOpened():
    print("Error: Could not open video.")
    
frame_number = 0
frame_skip = 5
image_counter = 0
while True:
    success, frame = video_capture.read()

    if not success:
        print("End of video or error reading the frame.")
        break

    if(frame_number % frame_skip == 0):
        output_dir = f'pictures/{video_name.split(".")[0]}'
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        cv2.imwrite(f'{output_dir}/frame_v1.0.0_{image_counter}.jpg', frame)
        image_counter += 1        
        print("next itera")
    frame_number += 1

video_capture.release()

end_time = time.time()
elapsed_time = end_time - start_time
print(f"Elapsed time: {elapsed_time:.2f} seconds")