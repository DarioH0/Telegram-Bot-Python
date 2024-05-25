import asyncio
import aiohttp
import json

class Bot:
    def __init__(self, token, prefix="/"):
        if "TOKEN_HERE" == token:
            print("You need to replace \"TOKEN_HERE\" in the code with your bot's token.")
            print("For help, visit https://core.telegram.org/bots/tutorial#obtain-your-bot-token")
            exit(1)        

        self.token = token
        self.base_url = f"https://api.telegram.org/bot{self.token}"
        self.commands = {}
        self.prefix = prefix

        self.name = None
        self.id = None
        asyncio.run(self._fix_())

    async def _fix_(self):
        self.name = await self.fetch_bot_name()
        self.id = await self.fetch_bot_id()

    async def send_message(self, chat_id, text):
        url = f"{self.base_url}/sendMessage"
        payload = {"chat_id": chat_id, "text": text}
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload) as response:
                return await response.text()

    async def handle_message(self, message):
        chat_id = message["chat"]["id"]
        text = message.get("text", "")
        
        if not text.startswith(self.prefix):
            return
        
        command = text.split()[0][len(self.prefix):]
        if command in self.commands:
            await self.commands[command](message)

    async def check_messages(self, offset=None):
        url = f"{self.base_url}/getUpdates"
        payload = {"offset": offset, "timeout": 30}
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=payload) as response:
                if response.status == 200:
                    updates = (await response.json())["result"]
                    if updates:
                        for update in updates:
                            offset = update["update_id"] + 1
                            message = update["message"]
                            await self.handle_message(message)
                    return offset

    async def run(self):
        offset = 0
        while True:
            try:
                offset = await self.check_messages(offset)
            except Exception as e:
                print(f"An error occurred: {e}")

    def command(self, name):
        def decorator(func):
            self.commands[name] = func
            return func
        return decorator

    def set_prefix(self, prefix):
        self.prefix = prefix

    async def fetch_bot_name(self):
        url = f"{self.base_url}/getMe"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                data = await response.json()
                if response.status == 200:
                    return str(data.get("result", {}).get("username"))
                else:
                    print("Invalid Token")
                    exit(1)

    async def fetch_bot_id(self):
        url = f"{self.base_url}/getMe"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                data = await response.json()
                if response.status == 200:
                    return str(data.get("result", {}).get("id"))
                else:
                    print("Invalid Token")
                    exit(1)

    async def start(self):
        print(f"Connected to @{self.name} (ID: {self.id})")
        print("Press CTRL + Z to close safely.\n")
        await self.on_ready()
        await self.run()
