import cv2
import os
import time
import queue
import asyncio
import base64

from frame_processing import get_scores

class FrameExtractor:
    
    def __init__(self, video_name, dictionary):
        self.video_name = video_name
        self.video_location = 'videos'
        self.dictionary = dictionary
        self.video_path = os.path.join(self.video_location, self.video_name)
        self.frame_skip = 5
        

    def extract_frames(self, my_fps=3):
        start_time = time.time()
        print(f"Starting the process. Video path: {self.video_location}/{self.video_name}")

        video_capture = cv2.VideoCapture(self.video_path)
        fps = video_capture.get(cv2.CAP_PROP_FPS)
        
        self.frame_skip = int(fps // my_fps)

        if not video_capture.isOpened():
            print("Error: Could not open video.")
            return

        frame_number = 0
        image_counter = 0
        output_dir = f'pictures/{self.video_name.split(".")[0]}'
        
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        previous_frame = None
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
                print("Saved frame:", image_counter)
                images.append(image_path)
                
                
                if previous_frame is not None:
                    score = get_scores(previous_frame, frame)
                    print(f"Frame pair: {image_counter - 1} and {image_counter}")
                    
                    
                    with open(image_path, "rb") as image_file:
                        image_data = base64.b64encode(image_file.read()).decode('utf-8')
                        
                    self.dictionary[self.video_name].append({
                        "image": image_data,
                        "score": score.item()
                    })
                    print(f"Video: {self.video_name}; Score: {score.item()}")

                previous_frame = frame
                image_counter += 1

            frame_number += 1

        video_capture.release()
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"Elapsed time: {elapsed_time:.2f} seconds")
        return images