import asyncio
from PIL import Image
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from typing import List

from Gif_Ascii_Animator import extract_gif_frames, convert_frames_to_ascii

app = FastAPI()

# At some point, figure out how to avoid sending newlines in favor of something else
newline = "\033[1E"
clear = "\033[2J"

plinko = r"""
 _   _ ___________  _____ _____  ______ _     _____ _   _  _   _______ 
| | | |  _  | ___ \/  ___|  ___| | ___ \ |   |_   _| \ | || | / /  _  |
| |_| | | | | |_/ /\ `--.| |__   | |_/ / |     | | |  \| || |/ /| | | |
|  _  | | | |    /  `--. \  __|  |  __/| |     | | | . ` ||    \| | | |
| | | \ \_/ / |\ \ /\__/ / |___  | |   | |_____| |_| |\  || |\  \ \_/ /
\_| |_/\___/\_| \_|\____/\____/  \_|   \_____/\___/\_| \_/\_| \_/\___/ 
"""

frames_big = convert_frames_to_ascii(extract_gif_frames(Image.open("horse-plinko.gif")), scale=6.75)
frames_small = convert_frames_to_ascii(extract_gif_frames(Image.open("horse-plinko-borderless.gif")), scale=2.25)

# A list to store all active WebSocket connections
connected_clients: List[WebSocket] = []


async def broadcast_message():
    """Function to broadcast a message to all connected WebSockets every second"""
    frame_index_small = 0
    frame_index_big = 0
    
    while True:
        
        # Broadcast message to all clients
        message = "This is a broadcast message!"
        for websocket in connected_clients:
            try:
                print(websocket.scope["path"])
                if (websocket.scope["path"] == "/small"):
                    await websocket.send_text(plinko + "\n" + frames_small[frame_index_small])    
                else:
                    await websocket.send_text(frames_big[frame_index_big])
                
            except WebSocketDisconnect:
                # Remove clients that are no longer connected
                connected_clients.remove(websocket)
                
        frame_index_small += 1
        frame_index_big += 1
        
        if frame_index_big >= len(frames_big):
            frame_index_big = 0
        if frame_index_small >= len(frames_small):
            frame_index_small = 0
        
        
        await asyncio.sleep(.15)  # Sleep for 1 second before broadcasting again

@app.on_event("startup")
async def startup():
    """Start the background broadcast task when the server starts"""
    asyncio.create_task(broadcast_message())

@app.websocket("/")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for clients to connect"""
    await websocket.accept()
    print("Client connected")
    connected_clients.append(websocket)

    try:
        while True:
            # Keep the connection open to receive messages (if needed)
            await websocket.receive_text()
    except WebSocketDisconnect:
        connected_clients.remove(websocket)
        print("Client disconnected")

@app.websocket("/small")
async def websocket_endpoint_small(websocket: WebSocket):
    """WebSocket endpoint for clients to connect"""
    await websocket.accept()
    print("Client connected")
    connected_clients.append(websocket)

    try:
        while True:
            # Keep the connection open to receive messages (if needed)
            await websocket.receive_text()
    except WebSocketDisconnect:
        connected_clients.remove(websocket)
        print("Client disconnected")
