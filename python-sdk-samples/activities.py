from temporalio import activity

@activity.defn
async def process_my_greeting_activity(greeting : str) -> None:
	print(f"greeting sent successfully : {greeting}")