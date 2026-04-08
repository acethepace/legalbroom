import asyncio
import websockets
import json

async def test_ws():
    uri = "ws://localhost:8000/ws"
    async with websockets.connect(uri) as websocket:
        query = "What are the recent cases on the Fourth Amendment?"
        print(f"Sending query: {query}")
        await websocket.send(json.dumps({"message": query}))
        
        try:
            while True:
                response = await asyncio.wait_for(websocket.recv(), timeout=60)
                data = json.loads(response)
                print(f"Received: {data}")
                if data.get("type") == "citations":
                    print("Received citations, test passed!")
                    break
        except asyncio.TimeoutError:
            print("Timeout waiting for response")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_ws())
