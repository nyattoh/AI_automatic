import asyncio
from abc import ABC, abstractmethod
from typing import Optional

from app.schema.message import Msg


class BaseAgent(ABC):
    def __init__(self, name: str, in_queue: asyncio.Queue, out_queue: asyncio.Queue):
        self.name = name
        self.in_queue = in_queue
        self.out_queue = out_queue
        self._task: Optional[asyncio.Task] = None
        self._running = False

    async def start(self) -> None:
        if not self._running:
            self._running = True
            self._task = asyncio.create_task(self._run())

    async def _run(self) -> None:
        while self._running:
            try:
                msg: Msg = await self.in_queue.get()
                await self.handle_message(msg)
            except asyncio.CancelledError:
                self._running = False
                break

    async def stop(self) -> None:
        self._running = False
        if self._task:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass

    @abstractmethod
    async def handle_message(self, msg: Msg) -> None:
        pass
