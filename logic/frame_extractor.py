import cv2
import os
import time

start_time = time.time()

video_location = 'videos'
video_name = 'still.mp4'
video_path = os.path.join(video_location, video_name)
video_capture = cv2.VideoCapture(f"{video_path}")
frame_skip = 5
print(f"Starting the process. Video path: {video_location}/{video_name}")


if not video_capture.isOpened():
    print("Error: Could not open video.")
    
frame_number = 0
frame_skip = 5
counter = 0
while True:
    video_capture.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
    success, frame = video_capture.read()

    if not success:
        print("End of video or error reading the frame.")
        break

    cv2.imwrite(f'pictures/frame_v1.0.0_{counter}.jpg', frame)
    counter += 1
    print("next itera")
    frame_number += 5

video_capture.release()

end_time = time.time()
elapsed_time = end_time - start_time
print(f"Elapsed time: {elapsed_time:.2f} seconds")