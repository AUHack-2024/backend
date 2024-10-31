import asyncio
import websockets

async def connect_to_server():
    # Replace with your server's public IP and port
    uri = "ws://185.229.154.89:80"  
    try:
        # Attempt to connect to the WebSocket server
        async with websockets.connect(uri) as websocket:
            print("Connected to the server successfully.")
            
            # Optional: Keep the connection open for testing
            await asyncio.Future()  # Keep the connection open indefinitely
            
    except Exception as e:
        print(f"Failed to connect: {e}")

# Run the client
asyncio.run(connect_to_server())
