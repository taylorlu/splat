import asyncio
import websockets

async def send_file(websocket, path):
    fps = 30
    interval = 1 / fps
    filename_template = 'splats/{}.splat'
    file_index = 0
    max_files = 10

    try:
        while True:
            filename = filename_template.format(file_index)
            try:
                with open(filename, "rb") as file:
                    data = file.read()
                    await websocket.send(data)
                    print(f"Sent {filename} to the client")
            except Exception as e:
                print(f"Error: {e}")

            file_index += 1
            if file_index > max_files:
                file_index = 0
            
            await asyncio.sleep(interval)
    except websockets.exceptions.ConnectionClosed:
        print("Client disconnected")

async def main():
    async with websockets.serve(send_file, "0.0.0.0", 8000):
        print("Server started on ws://127.0.0.1:8000")
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())