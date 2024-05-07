#!/usr/bin/env python3

import asyncio

async def main():
    wait_random = __import__('0-basic_async_syntax').wait_random

    print(await wait_random())
    print(await wait_random(5))
    print(await wait_random(15))
