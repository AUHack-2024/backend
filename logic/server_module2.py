import asyncio
import websockets
import base64
from asyncio import Queue

clients = set()

async def register(websocket):
    clients.add(websocket)
    print("Client connected.")
    try:
        await websocket.wait_closed()
    finally:
        clients.remove(websocket)
        print("Client disconnected.")

async def send_image(image):
    # Periodically queue the image for sending every 5 seconds (adjust as needed)
    try:
        with open(image, "rb") as image_file:
            image_data = base64.b64encode(image_file.read()).decode('utf-8')
            
            for client in clients:
                await client.send(image_data)
                
            print("Image queued to be sent to clients.")
    except FileNotFoundError:
        print("Image file not found.")
    except Exception as e:
        print(f"Error in send_image: {e}")

async def handler(websocket, path):
    await register(websocket)

async def start_server():
    # Start the WebSocket server
    server = await websockets.serve(handler, "0.0.0.0", 8080)
    print("Server started at ws://0.0.0.0:8080")
