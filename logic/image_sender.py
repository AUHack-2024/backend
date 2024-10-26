import base64
import sys
import os
import keyboard
import asyncio
import threading

# Add the parent directory of 'server_module2' to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import the necessary functions or classes from server_module2
from server_module2 import run_server, send_image, message_handler, clients, message_queue

# Initialize and run the WebSocket server in the background
server_thread = threading.Thread(target=run_server)
server_thread.start()


async def close_clients():
    for client in clients:
        await client.close()

try:
    while True:
        if keyboard.is_pressed('x'):
            print("Closing connection...")
            # Close the server gracefully
            asyncio.run(close_clients())
            break
        elif keyboard.is_pressed('Enter'):
            asyncio.run(send_image())
            asyncio.run(message_handler())
            print(f"Image sent to {len(clients)} clients.")
except KeyboardInterrupt:
    print("Program interrupted. Closing connection...")
    # Close the server gracefully
    asyncio.run(close_clients())
