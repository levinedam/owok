# This file is part of NeuraSelf-UwU.
# Copyright (c) 2025-Present Routo
#
# NeuraSelf-UwU is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# You should have received a copy of the GNU General Public License
# along with NeuraSelf-UwU. If not, see <https://www.gnu.org/licenses/>.


import asyncio
import random
import time

class TypingSimulator:
    @staticmethod
    async def send(bot, channel, content):
        config = bot.config.get('stealth', {}).get('typing', {})
        if not config.get('enabled', False):
            try:
                await channel.send(content)
                return True
            except:
                return False
        
        reaction_min = config.get('reaction_min', 1.0)
        reaction_max = config.get('reaction_max', 3.0)
        mistake_rate = config.get('mistake_rate', 5)
        extra_delay = config.get('extra_delay', 0)
        
        if mistake_rate > 1: mistake_rate /= 100.0

        reaction_time = random.uniform(reaction_min, reaction_max)
        if reaction_time > 0.1:
            await asyncio.sleep(reaction_time)

        try:
            async with channel.typing():
                chars = list(content)
                i = 0
                typo_count = 0
                
                start_time = time.time()
                
                while i < len(chars):
                    char = chars[i]
                    delay = random.uniform(0.08, 0.18)
                    if char in ".,!?;": delay += random.uniform(0.3, 0.5)
                    
                    if random.random() < mistake_rate and i < len(chars) - 1:
                        typo_count += 1
                        await asyncio.sleep(random.uniform(0.1, 0.2)) 
                        await asyncio.sleep(random.uniform(0.2, 0.5))
                        await asyncio.sleep(random.uniform(0.1, 0.2))
                    
                    await asyncio.sleep(delay)
                    i += 1
                
                enter_delay = random.uniform(0.3, 0.7) + (random.uniform(0, extra_delay) if extra_delay > 0 else 0)
                await asyncio.sleep(enter_delay)
                
                total_time = round(time.time() - start_time, 2)
                if typo_count > 0:
                    bot.log("STEALTH", f"Typing: {total_time}s (Simulated {typo_count} typos)")
                
                await channel.send(content)
                return True
        except Exception as e:
            bot.log("ERROR", f"Typing failed: {e}")
            return False
    
    @staticmethod
    def calculate_typing_speed(text, wpm=55):
        return (len(text) / 5) / wpm * 60