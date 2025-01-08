from .. import *
from pyrogram import *

@client.on_message(filters.command('start') & filters.user(DEVS))
async def start(_, message):
  await message.reply("Hmm I'm alive probably")
