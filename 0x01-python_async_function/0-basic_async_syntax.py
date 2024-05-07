#!/usr/bin/env python3
""" Basics of async """
import asyncio
import random


def run(coro):
    loop = asyncio.get_event_loop()
    return loop.run_until_complete(coro())


async def wait_random(max_delay: int = 10) -> float:
    """ Asynchronous coroutine that takes an int argument and
        waits for a random delay seconds.
        Args:
            max_delay: integer argument.
        Return:
            Random float.
    """
    i = random.uniform(0, max_delay)
    await asyncio.sleep(i)
    return i



