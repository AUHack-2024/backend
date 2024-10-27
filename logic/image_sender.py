import asyncio
import json
from server_module2 import start_server, send_video_info, clients

class ImageSender:
    def start_server(self, lock):
        start_server(lock)

    def close_clients(self):
        for client in clients:
            client.close()
            
    # async def read_message(self):
    #     return await receive_message()

    def send_video_info_to_clients(self, video_info):
        video_info = json.dumps(video_info)
        # print(f"Serialized frames: {video_info}")
        
        if clients:
            asyncio.run(send_video_info(video_info))
            print(f"Image sent to {len(clients)} clients.")
        else:
            print("No clients connected to send the image.")
            
            
    # def serialize_video_info(self, video_info):
    #     str = "{["

    #     for frame in video_info["video"]:
    #         str += f"{{\"image\": \"{frame["image"]}\", \"score\": {frame["score"]}}},"
        
    #     str = f"\"best\": {video_info["best"]}"

    #     return str + "]}"