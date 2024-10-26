import asyncio
from server_module2 import start_server, send_image, clients

class ImageSender:
    def start_server(self, lock):
        start_server(lock)

    def close_clients(self):
        for client in clients:
            client.close()
            
    # async def read_message(self):
    #     return await receive_message()

    def send_image_to_clients(self, frames):
        if clients:  # Ensure there are clients connected
            asyncio.run(send_image(frames))
            print(f"Image sent to {len(clients)} clients.")
        else:
            print("No clients connected to send the image.")