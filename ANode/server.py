from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from .solver import a_star_solve_stream

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # adjust for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.websocket("/ws/solve")
async def solve(websocket: WebSocket):
    await websocket.accept()
    try:
        payload = await websocket.receive_json()
        initial_grid = payload["grid"]

        async for step in a_star_solve_stream(initial_grid):
            await websocket.send_json(step)

    except Exception as e:
        await websocket.send_json({"error": str(e)})
    finally:
        await websocket.close()
