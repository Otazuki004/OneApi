from pyrogram import Client, idle
from . import *
import logging
import asyncio

async def start():
  logging.info("Starting pyrogram...")
  await bot.run()

async def main():
    await start()

def run_main():
    loop = asyncio.get_event_loop()
    if loop.is_running():
        asyncio.ensure_future(main())
    else:
        loop.run_until_complete(main())

run_main()
