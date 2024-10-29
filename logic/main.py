import asyncio
from image_sender import ImageSender
from frame_extractor import FrameExtractor
import os
import threading

lock = threading.Lock()
is_dictionary_ready = False

def extract_frames(videos, frames_queue, dictionary, image_sender):
    global is_dictionary_ready
    
    for video in videos:
        frame_extractor = FrameExtractor(video, frames_queue, dictionary)
        images = frame_extractor.extract_frames()
        
        is_dictionary_ready = True
        
        frames = dictionary[video]
        
        if len(frames) > 10:
            average_by_group = []
            group = []
            
            for i in range(len(frames)):
                group.append(frames[i]["score"])
                if i % 10 == 0:
                    average_by_group.append(sum(group) / len(group))
                    group = []

            if group:
                average_by_group.append(sum(group) / len(group))
                
            best_index = average_by_group.index(min(average_by_group)) + 1
            print(f"Average scores for: {average_by_group}; Best group: {best_index}")
            
            video_info = {"video": frames, "best": best_index}
        else:
            # less then 10 frames, send the the first group as the best
            video_info = {"video": frames, "best": 1}
            
            
        image_sender.send_video_info_to_clients(video_info)
        
    print("All videos processed. Exiting.")

async def main():
    # Set up paths and verify video folder
    videos_path = 'videos'
    if not os.path.exists(videos_path):
        raise FileNotFoundError(f"The directory {videos_path} does not exist.")
    
    videos = os.listdir(videos_path)
    frames_queue = asyncio.Queue()
    image_sender = ImageSender()
    
    dictionary = {v: 0 for v in videos}
    server_thread = threading.Thread(target=image_sender.start_server, args=(lock,))
    computation_thread = threading.Thread(target=extract_frames, args=(videos, frames_queue, dictionary, image_sender))
    
    server_thread.start()
    computation_thread.start()

    print(f"Videos found: {videos}")

# Run the main async function
asyncio.run(main())
