import asyncio
import logging
import os
from sys import stdout

import discord
from discord.ext import commands

from app.core.client import Client
from app.core.settings import config

logging.basicConfig(filename='/app/logs/log.txt', level=logging.INFO)
logger = logging.getLogger("main")

if os.environ.get("BOT_TOKEN") is None:
    raise ValueError("BOT_TOKEN environment variable not set")


INTENTS = discord.Intents.default()
INTENTS.message_content = True

client = Client(
    command_prefix=commands.when_mentioned_or(config.BOT_PREFIX),
    case_insensitive=True,
    intents=INTENTS,
    help_command=None,
)


@client.event
async def on_ready():
    logging.info("Loaded prefix: %s", config.BOT_PREFIX)
    logging.info("Bot started!")
    for command in client.commands:
        logging.info("Loaded command: %s", command.name)


@client.event
async def on_voice_state_update(member, before, after):
    voice_client = client.voice_clients[0] if client.voice_clients else None
    if voice_client:
        if len(voice_client.channel.members) == 1:
            await voice_client.disconnect()


async def main():
    async with client:
        await client.start(config.BOT_TOKEN)


if __name__ == "__main__":
    asyncio.run(main())
