import asyncio
from argparse import ArgumentParser

from app.core.agent_base import BaseAgent
from app.schema.message import Msg


class PMAgent(BaseAgent):
    async def handle_message(self, msg: Msg) -> None:
        # simply echo to orchestrator after adding own name
        reply = Msg(sender=self.name, receiver="orchestrator", content=msg.content, tokens=len(msg.content))
        await self.out_queue.put(reply)


async def main() -> None:
    parser = ArgumentParser()
    parser.add_argument("--id", default="1")
    args = parser.parse_args()
    q_in: asyncio.Queue[Msg] = asyncio.Queue()
    q_out: asyncio.Queue[Msg] = asyncio.Queue()
    agent = PMAgent(f"PM{args.id}", q_in, q_out)
    await agent.start()
    try:
        while True:
            await asyncio.sleep(1)
    except asyncio.CancelledError:
        await agent.stop()


if __name__ == "__main__":
    asyncio.run(main())
