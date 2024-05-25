from telegrambot import Bot
import asyncio

bot = Bot(token="TOKEN_HERE", prefix="/")

async def on_ready():
    print(f"Bot is ready")
bot.on_ready = on_ready

@bot.command("start")
async def start_command(message):
    chat_id = message["chat"]["id"]

    await bot.send_message(chat_id, "Hello from my custom wrapper!")

@bot.command("ping")
async def ping_command(message):
    chat_id = message["chat"]["id"]

    await bot.send_message(chat_id, "Pong!")

@bot.command("help")
async def help_command(message):
    chat_id = message["chat"]["id"]
    commands = list(bot.commands)
    
    expression = f'\n* {bot.prefix}'.join(commands)
    await bot.send_message(chat_id, f"My commands are:\n* {bot.prefix}{expression}")

asyncio.run(bot.start())
