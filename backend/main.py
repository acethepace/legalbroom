import os
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict, Any

from app.rag.engine import RAGEngine
from app.services.courtlistener import CourtListenerService

app = FastAPI(title="Legal AI Assistant API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components
courtlistener_service = CourtListenerService()
rag_engine = RAGEngine(courtlistener_service)

@app.on_event("shutdown")
async def shutdown_event():
    await courtlistener_service.close()

@app.get("/")
def root():
    return {"message": "Legal AI Assistant API is running"}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            # Receive message from user
            data = await websocket.receive_json()
            user_message = data.get("message")
            case_details = data.get("case_details")
            
            if user_message:
                # Generate and stream response
                async for chunk in rag_engine.stream_answer(user_message, []):
                    await websocket.send_json(chunk)
            elif case_details:
                # Generate and stream case analysis
                async for chunk in rag_engine.stream_case_analysis(case_details):
                    await websocket.send_json(chunk)
            else:
                continue
                
    except WebSocketDisconnect:
        print("WebSocket disconnected")
    except Exception as e:
        print(f"Error in WebSocket: {e}")
        try:
            await websocket.send_json({"type": "error", "text": str(e)})
        except:
            pass

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
