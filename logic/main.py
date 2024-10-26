import asyncio
from image_sender import ImageSender
from frame_extractor import FrameExtractor
import os
import sys


class MainApp:
    def __init__(self):
        print(sys.path)
        sys.path.insert(0, os.path.join(sys.path[0], 'videos'))
        self.videos = os.listdir('videos')
    
        
        
        self.frames_queue = asyncio.Queue()
        # self.image_sender = ImageSender()
        
        print(f"Videos found: {self.videos}")
        self.dictionary = {v:0 for v in self.videos}
        
        for video in self.videos:
            self.frame_extractor = FrameExtractor(video, self.frames_queue, self.dictionary)
            self.frame_extractor.extract_frames()
            
            
if __name__ == "__main__":
    MainApp()

