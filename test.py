# from config import Config

# print(Config.HOST, Config.CELERY_PORT, Config.FASTAPI_PORT)


import asyncio

async def worker(name, queue):
    while True:
        # Get a task from the queue
        task = await queue.get()
        
        if task is None:  # Exit signal
            break

        # Process the task
        print(f'Worker {name} processing task: {task}')
        await asyncio.sleep(task)  # Simulate work with sleep

        # Mark the task as done
        queue.task_done()

async def main():
    # Create a queue
    queue = asyncio.Queue()

    # Start worker tasks
    workers = [asyncio.create_task(worker(i, queue)) for i in range(3)]

    # Add tasks to the queue
    for task_duration in [2, 1, 3, 4, 2]:
        await queue.put(task_duration)

    # Wait until the queue is fully processed
    await queue.join()

    # Stop workers
    for _ in workers:
        await queue.put(None)  # Send exit signal to workers

    await asyncio.gather(*workers)  # Wait for workers to finish

# Run the main function
asyncio.run(main())