import asyncio
import time
import random

class Automation:
    def __init__(self, bot):
        self.bot = bot
        self.active = True
        self.task = None
        self.owo_cmd = {
            "cmd_name": "owo",
            "prefix": False,
            "checks": True,
            "id": "owo"
        }
        self.last_used = 0.0

    async def start(self):
        self.task = asyncio.create_task(self.loop())

    async def loop(self):
        await asyncio.sleep(40)  # Wait longer before starting
        
        while self.active:
            cfg = self.bot.config.get('commands', {}).get('owo', {})
            if self.bot.paused or not cfg.get('enabled', False):
                await asyncio.sleep(2)
                continue

            current_time = time.time()

            # Fetch cooldown from settings.json, and use random in range
            cooldown_range = cfg.get("cooldown", [10, 13])  # Default range [10, 13]
            cur_cooldown = random.uniform(cooldown_range[0], cooldown_range[1])

            # Ensure we wait at least 'cur_cooldown' seconds between each owo command
            if current_time - self.last_used < cur_cooldown:
                await asyncio.sleep(1)  # Sleep for a second and check again
                continue

            # Send the command and update the last used timestamp
            await self.bot.send_message(self.owo_cmd["cmd_name"])
            self.last_used = time.time()
            
            # Random sleep within range 20-25 seconds to add a small delay between each send
            await asyncio.sleep(random.uniform(20.0, 25.0))

async def setup(bot):
    cog = Automation(bot)
    await cog.start()
