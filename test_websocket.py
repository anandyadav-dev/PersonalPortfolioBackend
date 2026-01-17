
import asyncio
import websockets
import json

async def test_websocket():
    uri = "ws://127.0.0.1:8000/api/v1/resume/ws"
    async with websockets.connect(uri) as websocket:
        # Send question
        question = {"question": "what is the name of condidate ?"}
        await websocket.send(json.dumps(question))
        print(f"Sent: {question}")

        # Receive streamed response
        while True:
            try:
                response = await websocket.recv()
                data = json.loads(response)
                
                if "error" in data:
                    print(f"Error: {data['error']}")
                    break
                
                if "status" in data:
                    print(f"Status: {data['status']}")
                    if data["status"] == "done":
                        break
                
                if "token" in data:
                    print(data["token"], end="", flush=True)
            except websockets.exceptions.ConnectionClosed:
                print("\nConnection closed")
                break

if __name__ == "__main__":
    asyncio.run(test_websocket())
