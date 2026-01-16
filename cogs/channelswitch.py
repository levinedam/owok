# This file is part of NeuraSelf-UwU.
# Copyright (c) 2025-Present Routo
#
# NeuraSelf-UwU is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

import asyncio
import time
import random

class ChannelSwitch:
    def __init__(self, bot):
        self.bot = bot
        self.active = True
        self.task = None
        
    async def start(self):
        self.task = asyncio.create_task(self.switcher_loop())

    async def switcher_loop(self):
        await asyncio.sleep(5)
        while self.active:
            cfg = self.bot.config.get('utilities', {}).get('autochannel', {})
            if cfg.get('enabled', False):
                interval_config = cfg.get('interval', [300, 350])
                
                if isinstance(interval_config, list) and len(interval_config) == 2:
                    interval = random.uniform(interval_config[0], interval_config[1])
                else:
                    interval = float(interval_config)
                
                await asyncio.sleep(interval)
                
                channels = cfg.get('channels', [])
                if len(channels) >= 2:
                    current = str(self.bot.channel_id)
                    available = [c for c in channels if str(c) != current]
                    if available:
                        next_chan = random.choice(available)
                        self.bot.channel_id = int(next_chan)
                        self.bot.log("SYS", f"ChannelSwitch: Rotated to channel {next_chan}")
                
            else:
                await asyncio.sleep(60)

async def setup(bot):
    cog = ChannelSwitch(bot)
    await cog.start()
