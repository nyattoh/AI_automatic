from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import Response

from app.core.orchestrator import Orchestrator
from app.core.metrics import render_metrics

app = FastAPI()
orchestrator = Orchestrator(pm=1, dev=1)

@app.on_event("startup")
async def startup() -> None:
    await orchestrator.start()

@app.on_event("shutdown")
async def shutdown() -> None:
    await orchestrator.stop()


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/metrics")
async def metrics() -> Response:
    return Response(render_metrics(), media_type="text/plain; version=0.0.4")


@app.websocket("/ws/stream")
async def websocket_endpoint(ws: WebSocket) -> None:
    await ws.accept()
    queue = orchestrator.ws_queue
    try:
        while True:
            msg = await queue.get()
            await ws.send_json(msg.dict())
    except WebSocketDisconnect:
        pass
