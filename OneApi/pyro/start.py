from .. import *
from pyrogram import *

@Client.on_message(filters.command('start'))
async def start(_, message):
  await message.reply("Hmm I'm alive probably")
