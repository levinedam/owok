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
import time
import json
import os
import discord
from discord.ext import commands

class Giveaway(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db_path = os.path.join(bot.base_dir, 'config', 'giveaway_db.json')
        self.joined_ids = []
        self._load_state()
        
    def _load_state(self):
        try:
            if os.path.exists(self.db_path):
                with open(self.db_path, 'r') as f:
                    data = json.load(f)
                    self.joined_ids = data.get('joined_ids', [])
        except Exception:
            self.joined_ids = []
            
    def _save_state(self):
        if len(self.joined_ids) > 100:
            self.joined_ids = self.joined_ids[-100:]
        try:
            with open(self.db_path, 'w') as f:
                json.dump({'joined_ids': self.joined_ids}, f)
        except Exception as e:
            self.bot.log("ERROR", f"Failed to save giveaway DB: {e}")

    async def _process_message(self, message):
        cfg = self.bot.config.get('commands', {}).get('giveaway', {})
        if not cfg.get('enabled', False): 
            return

        target_channels = [str(c) for c in cfg.get('channels', [])]
        if str(message.channel.id) not in target_channels:
            return

        if not message.embeds: return
        
        is_giveaway = False
        for embed in message.embeds:
            if embed.author and embed.author.name and " A New Giveaway Appeared!" in embed.author.name:
                is_giveaway = True
                break
        
        if not is_giveaway: return
        
        if message.id in self.joined_ids:
            return

        cooldown = cfg.get('cooldown', 2)
        await asyncio.sleep(cooldown)

        if not message.components: return
        
        try:
            component = message.components[0]
            if not isinstance(component, discord.ActionRow): return
            
            button = component.children[0]
            if isinstance(button, discord.Button) and not button.disabled:
                try:
                    await button.click()
                    self.joined_ids.append(message.id)
                    self._save_state()
                    self.bot.log("SUCCESS", f"Joined giveaway in {message.channel.name}")
                except Exception as e:
                    if "Did not receive a response" in str(e):
                         self.joined_ids.append(message.id)
                         self._save_state()
                         self.bot.log("SUCCESS", f"Joined giveaway in {message.channel.name}")
                    else:
                        self.bot.log("ERROR", f"Failed to join giveaway: {e}")
        except Exception as e:
            self.bot.log("ERROR", f"Failed to process giveaway: {e}")

    async def cog_load(self):
        cfg = self.bot.config.get('commands', {}).get('giveaway', {})
        if not cfg.get('enabled', False):
             return

        target_channels = [str(c) for c in cfg.get('channels', [])]
        if not target_channels: return

        self.bot.log("SYS", "Scanning for missed giveaways...")
        
        for channel_id in target_channels:
            try:
                channel = self.bot.get_channel(int(channel_id))
                if not channel:
                     try:
                        channel = await self.bot.fetch_channel(int(channel_id))
                     except:
                        self.bot.log("WARN", f"Giveaway channel {channel_id} not found/accessible.")
                        continue
                
                async for msg in channel.history(limit=20):
                     await self._process_message(msg)
                     
            except Exception as e:
                self.bot.log("ERROR", f"Error scanning channel {channel_id}: {e}")

    @commands.Cog.listener()
    async def on_message(self, message):
        await self._process_message(message)

async def setup(bot):
    await bot.add_cog(Giveaway(bot))
