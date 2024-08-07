import asyncio
from typing import List
from datetime import timedelta
from temporalio import workflow
from activities import process_my_greeting_activity

@workflow.defn
class ProcessGreetingWorklow:
    def __init__(self) -> None:
        self.incoming_greeting_queue: asyncio.Queue[str] = asyncio.Queue()
        self.exit = False

    @workflow.run
    async def run(self) -> List[str]:
        sent_greetings_list: List[str] = []
        while True:
            await workflow.wait_condition(
                lambda: not self.incoming_greeting_queue.empty() or self.exit
            )

            while not self.incoming_greeting_queue.empty():
                greeting_msg = f"Hello, {self.incoming_greeting_queue.get_nowait()}"
                sent_greetings_list.append(greeting_msg)
                await workflow.execute_activity(
                    process_my_greeting_activity,
                    greeting_msg,
                    start_to_close_timeout=timedelta(seconds=10),
                )

            if self.exit:
                return sent_greetings_list

            # Yield control to avoid deadlock
            await asyncio.sleep(0)


    @workflow.signal
    async def add_sender(self, name: str) -> None:
        await self.incoming_greeting_queue.put(name)

    @workflow.signal
    def exit(self) -> None:
        self.exit = True
