import asyncio
import websockets
import json

async def test_ws():
    uri = "ws://localhost:8000/ws"
    async with websockets.connect(uri) as websocket:
        print("Connected to WebSocket")
        query = "What are the Fourth Amendment implications for digital privacy and cell phone searches?"
        await websocket.send(json.dumps({"message": query}))
        print(f"Sent query: {query}")
        
        try:
            while True:
                response = await asyncio.wait_for(websocket.recv(), timeout=60)
                data = json.loads(response)
                print(f"Received: {data}")
                if data["type"] == "content" and data["text"]:
                    # Keep receiving until we get some content
                    pass
                if data["type"] == "citations":
                    print("Received citations, done.")
                    break
        except asyncio.TimeoutError:
            print("Timeout waiting for response")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_ws())
