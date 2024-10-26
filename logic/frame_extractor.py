import cv2
import os
import time
import queue
import asyncio

class FrameExtractor:
    
    def __init__(self, video_name, frames_queue):
        self.video_name = video_name + '.mp4'
        self.frames_queue = frames_queue
        self.video_location = 'videos'
        self.video_path = os.path.join(self.video_location, self.video_name)
        self.frame_skip = 5
        

    async def extract_frames(self):
        start_time = time.time()
        print(f"Starting the process. Video path: {self.video_location}/{self.video_name}")

        video_capture = cv2.VideoCapture(self.video_path)

        if not video_capture.isOpened():
            print("Error: Could not open video.")
            return

        frame_number = 0
        image_counter = 0
        output_dir = f'pictures/{self.video_name.split(".")[0]}'
        
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        while True:
            success, frame = video_capture.read()

            if not success:
                print("End of video or error reading the frame.")
                break

            if frame_number % self.frame_skip == 0:
                frame_file = f"{output_dir}/frame_{image_counter}.jpg"
                
                cv2.imwrite(frame_file, frame)
                image_counter += 1        
                print("Saved frame:", image_counter)
                await self.frames_queue.put(frame_file)

            frame_number += 1

        video_capture.release()
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"Elapsed time: {elapsed_time:.2f} seconds")
