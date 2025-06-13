import asyncio
from typing import Dict, List

from app.core.metrics import cc_requests_total, cc_tokens_total
from app.schema.message import Msg
from app.agents.pm_agent import PMAgent
from app.agents.dev_agent import DevAgent


class Orchestrator:
    def __init__(self, pm: int = 1, dev: int = 1):
        self.pm = pm
        self.dev = dev
        self.queue: asyncio.Queue[Msg] = asyncio.Queue()
        self.children: Dict[str, asyncio.Queue] = {}
        self.tasks: List[asyncio.Task] = []
        self.ws_queue: asyncio.Queue[Msg] = asyncio.Queue()

    async def start(self) -> None:
        for i in range(1, self.pm + 1):
            pm_name = f"PM{i}"
            pm_q: asyncio.Queue[Msg] = asyncio.Queue()
            pm = PMAgent(pm_name, pm_q, self.queue)
            self.children[pm_name] = pm_q
            self.tasks.append(asyncio.create_task(pm.start()))
            for j in range(1, self.dev + 1):
                dev_name = f"{pm_name}-DEV{j}"
                dev_q: asyncio.Queue[Msg] = asyncio.Queue()
                dev = DevAgent(dev_name, dev_q, self.queue)
                self.children[dev_name] = dev_q
                self.tasks.append(asyncio.create_task(dev.start()))
        self.tasks.append(asyncio.create_task(self._main_loop()))

    async def _main_loop(self) -> None:
        while True:
            try:
                msg: Msg = await self.queue.get()
                cc_requests_total.labels(role=msg.sender).inc()
                cc_tokens_total.labels(role=msg.sender).inc(msg.tokens)
                if msg.receiver == "broadcast":
                    for child_q in self.children.values():
                        await child_q.put(msg)
                elif msg.receiver in self.children:
                    await self.children[msg.receiver].put(msg)
                await self.ws_queue.put(msg)
            except asyncio.CancelledError:
                break

    async def stop(self) -> None:
        for t in self.tasks:
            t.cancel()
        for t in self.tasks:
            try:
                await t
            except asyncio.CancelledError:
                pass
