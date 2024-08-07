import asyncio
from temporalio.client import Client
from temporalio.worker import Worker
from workflows import ProcessGreetingWorklow
from activities import process_my_greeting_activity

async def main():
    client = await Client.connect("localhost:7233")

    async with Worker(
        client,
        task_queue="greeting_signal_tq",
        workflows=[ProcessGreetingWorklow],
        activities=[process_my_greeting_activity],
    ):
        print("Worker started.")
        await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())
