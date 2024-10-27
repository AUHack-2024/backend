import cv2
import os
import time
import queue
import asyncio
import base64

from frame_processing import get_scores

class FrameExtractor:
    
    def __init__(self, video_name, frames_queue, dictionary):
        self.video_name = video_name
        self.frames_queue = frames_queue
        self.video_location = 'videos'
        self.dictionary = dictionary
        self.video_path = os.path.join(self.video_location, self.video_name)
        self.frame_skip = 5
        

    def extract_frames(self, my_fps=5):
        start_time = time.time()
        print(f"Starting the process. Video path: {self.video_location}/{self.video_name}")

        
        video_capture = cv2.VideoCapture(self.video_path)
        fps = video_capture.get(cv2.CAP_PROP_FPS)
        
        self.frame_skip = fps // my_fps

        if not video_capture.isOpened():
            print("Error: Could not open video.")
            return

        frame_number = 0
        image_counter = 0
        output_dir = f'pictures/{self.video_name.split(".")[0]}'
        
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        frames_pair = []
        images = []
        self.dictionary[self.video_name] = []
        
        while True:
            success, frame = video_capture.read()

            if not success:
                print("End of video or error reading the frame.")
                break

            if frame_number % self.frame_skip == 0:
                image_path = f'{output_dir}/frame_{image_counter}.jpg'
                cv2.imwrite(image_path, frame)
                frames_pair.append(frame)
                image_counter += 1        
                print("Saved frame:", image_counter)
                
                if(len(frames_pair) == 2):
                    score = get_scores(frames_pair[0], frames_pair[1])
                    
                    with open(image_path, "rb") as image_file:
                        image_data = base64.b64encode(image_file.read()).decode('utf-8')
                        
                    self.dictionary[self.video_name].append({"image": image_data, "score": score.item()})
                    # print(f"Video: {self.video_name}; Score: {self.dictionary[self.video_name]}")
                    frames_pair = []
                    images.append(image_path)

            frame_number += 1

        video_capture.release()
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"Elapsed time: {elapsed_time:.2f} seconds")
        return images