import asyncio
from image_sender import ImageSender
from frame_extractor import FrameExtractor

class MainApp:
    def __init__(self):
        self.frames_queue = asyncio.Queue()
        self.image_sender = ImageSender()
        self.frame_extractor = FrameExtractor('still', self.frames_queue)

    async def send_frames(self):
        while True:
            frame = await self.frame_extractor.frames_queue.get()
            await self.image_sender.send_image_to_clients(frame)

    async def initiate_frame_extraction(self):
        frame_extractor = self.frame_extractor
        await frame_extractor.extract_frames()

    async def run(self):
        await asyncio.sleep(1)
        sender_task = asyncio.create_task(self.send_frames())
        await self.initiate_frame_extraction()
        await sender_task 

async def main():
    app = MainApp()
    try:
        await app.run()
    except KeyboardInterrupt:
        print("Program interrupted. Closing connection...")
        await app.image_sender.close_clients()

if __name__ == "__main__":
    asyncio.run(main())
