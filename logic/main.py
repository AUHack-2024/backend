import asyncio
from image_sender import ImageSender
from frame_extractor import FrameExtractor
import os
import sys
import time


class MainApp:
    def __init__(self):
        print(sys.path)
        sys.path.insert(0, os.path.join(sys.path[0], 'videos'))
        self.videos = os.listdir('videos')
    
        self.frames_queue = asyncio.Queue()
        self.image_sender = ImageSender()
        
        print(f"Videos found: {self.videos}")
        self.dictionary = {v:0 for v in self.videos}
        
        for video in self.videos:
            self.frame_extractor = FrameExtractor(video, self.frames_queue, self.dictionary)
            images = self.frame_extractor.extract_frames()
            
            for image in images:
                self.image_sender.send_image_to_clients(image)
                while self.image_sender.read_message() != "All done!":
                    time.sleep(0.05)
            
            
if __name__ == "__main__":
    MainApp()

