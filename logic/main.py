import asyncio
from frame_extractor import FrameExtractor
import os
import json
import threading
from server_module import start_server, send_video_info, clients

lock = threading.Lock()

def extract_frames(videos, dictionary):
    for video in videos:
        frame_extractor = FrameExtractor(video, dictionary)
        frame_extractor.extract_frames()
        
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
            
        video_info = json.dumps(video_info)

        if clients:
            asyncio.run(send_video_info(video_info))
            print(f"Image sent to {len(clients)} clients.")
        else:
            print("No clients connected to send the image.")
        
    print("All videos processed. Exiting.")
    

def main():
    # Set up paths and verify video folder
    videos_path = 'videos'
    if not os.path.exists(videos_path):
        raise FileNotFoundError(f"The directory {videos_path} does not exist.")
    
    videos = os.listdir(videos_path)
    
    dictionary = {v: 0 for v in videos}
    server_thread = threading.Thread(target=start_server, args=(lock,))
    computation_thread = threading.Thread(target=extract_frames, args=(videos, dictionary))
    
    server_thread.start()
    computation_thread.start()

    print(f"Videos found: {videos}")

# Run the main async function
main()
