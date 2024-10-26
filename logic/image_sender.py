import asyncio
from server_module2 import start_server, send_image, clients

class ImageSender:
    def __init__(self):
        self.server_task = asyncio.create_task(self.start_server())  # Start the server upon initialization

    async def start_server(self):
        await start_server()

    async def close_clients(self):
        for client in clients:
            await client.close()

    async def send_image_to_clients(self, image):
        if clients:  # Ensure there are clients connected
            await send_image(image)
            print(f"Image sent to {len(clients)} clients.")
        else:
            print("No clients connected to send the image.")