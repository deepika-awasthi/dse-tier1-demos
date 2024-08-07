import asyncio
from temporalio.client import Client
from workflows import ProcessGreetingWorklow

async def main():
    client = await Client.connect("localhost:7233")

    handle = await client.start_workflow(
        ProcessGreetingWorklow.run,
        id="greeting-signal-workflowid",
        task_queue="greeting_signal_tq",
    )

    await handle.signal(ProcessGreetingWorklow.add_sender, "user1")
    await handle.signal(ProcessGreetingWorklow.add_sender, "user2")
    await handle.signal(ProcessGreetingWorklow.add_sender, "user3")
    await handle.signal(ProcessGreetingWorklow.exit)

    result = await handle.result()
    print(f"Result: {result}")

if __name__ == "__main__":
    asyncio.run(main())
