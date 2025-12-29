import asyncio
import time
import random
import core.state as state

class Stealth:
    def __init__(self, bot):
        self.bot = bot
        self.active = True
        self.task = None
        
    async def start(self):
        self.task = asyncio.create_task(self.switcher_loop())

    async def switcher_loop(self):
        await asyncio.sleep(5)
        while self.active:
            cfg = self.bot.config.get('utilities', {}).get('channel_switcher', {})
            if cfg.get('enabled', False):
                interval_config = cfg.get('interval', 1500)
                
                # Handle both number and list formats
                if isinstance(interval_config, list) and len(interval_config) == 2:
                    interval = random.uniform(interval_config[0], interval_config[1])
                else:
                    interval = float(interval_config)
                
                await asyncio.sleep(interval)
                
                channels = cfg.get('channels', [])
                if len(channels) >= 2:
                    current = str(self.bot.channel_id)
                    next_chan = channels[1] if current == str(channels[0]) else channels[0]
                    
                    self.bot.channel_id = int(next_chan)
                    self.bot.log("SYS", f"Stealth: Rotated to channel {next_chan}")
                
                if isinstance(interval_config, list) and len(interval_config) == 2:
                    interval = random.uniform(interval_config[0], interval_config[1])
                else:
                    interval = float(interval_config)
                await asyncio.sleep(interval)
            else:
                await asyncio.sleep(60)

async def setup(bot):
    cog = Stealth(bot)
    await cog.start()