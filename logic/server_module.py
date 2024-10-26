import asyncio
import websockets
import base64
from asyncio import Queue

class WebSocketImageServer:
    def __init__(self, host="0.0.0.0", port=8080):
        self.host = host
        self.port = port
        self.clients = set()
        self.message_queue = Queue()

    async def register(self, websocket):
        self.clients.add(websocket)
        print("Client connected.")
        try:
            await websocket.wait_closed()
        finally:
            self.clients.remove(websocket)
            print("Client disconnected.")

    async def send_image(self):
        """Encodes and queues an image for sending to clients."""
        try:
            with open("pictures/still/frame_v1.0.0_0.jpg", "rb") as image_file:
                image_data = base64.b64encode(image_file.read()).decode('utf-8')
                await self.message_queue.put(image_data)
                print("Image queued to be sent to clients.")
        except FileNotFoundError:
            print("Image file not found.")
        except Exception as e:
            print(f"Error in send_image: {e}")

    async def message_handler(self):
        """Continuously sends messages from the queue to all connected clients."""
        while True:
            message = await self.message_queue.get()
            if message is None:
                break
            disconnected_clients = set()
            for client in self.clients:
                try:
                    await client.send(message)
                except websockets.ConnectionClosed:
                    disconnected_clients.add(client)
                    print("Client disconnected during message send.")
            self.clients.difference_update(disconnected_clients)
            print("Image sent to all connected clients.")

    async def handler(self, websocket, path):
        """Handles incoming WebSocket connections."""
        await self.register(websocket)

    async def start(self):
        # Start the WebSocket server
        self.server = await websockets.serve(self.handler, self.host, self.port)
        print(f"Server started at ws://{self.host}:{self.port}")
        
        # Start the message handler in the background
        self.message_handler_task = asyncio.create_task(self.message_handler())
        await self.server.wait_closed()

    async def trigger_image_send(self):
        """Public method to trigger image sending."""
        await self.send_image()
        
    async def close_clients(self):
        """Disconnects all connected clients."""
        for client in self.clients:
            await client.close()
        self.clients.clear()
        print("All clients have been disconnected.")

    def close_connection(self):
        """Public method to close all connections and stop the server."""
        asyncio.run(self.close_clients())
        if self.server:
            self.server.close()
            print("Server has been stopped.")

    def run_server(self):
        asyncio.run(self.start())