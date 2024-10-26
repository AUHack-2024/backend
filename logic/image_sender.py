import sys
import os
import keyboard
import asyncio



# Add the parent directory of 'logic' to the Python path
from server_module import WebSocketImageServer

# Initialize the WebSocket server
server = WebSocketImageServer()

# Run the server in the background
import threading
server_thread = threading.Thread(target=server.run_server)
server_thread.start()

# Trigger image send without WebSocket connection

try:
    while True:
        if keyboard.is_pressed('x'):
            print("Closing connection...")
            server.close_connection()
            break
        elif keyboard.is_pressed('Enter'):
            asyncio.run(server.trigger_image_send())
            print("Image sent to all clients.")
except KeyboardInterrupt:
    print("Program interrupted. Closing connection...")
    server.close_connection()
