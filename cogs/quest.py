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
import re
import time
import core.state as state

class Quest:
    def __init__(self, bot):
        self.bot = bot
        self.active = True
        self.task = None
        self.quests = {
            "hunt": {"target": 0, "progress": 0},
            "battle": {"target": 0, "progress": 0},
            "owo": {"target": 0, "progress": 0},
            "curse": {"target": 0, "progress": 0}
        }
        
    async def start(self):
        self.task = asyncio.create_task(self.run_loop())

    async def run_loop(self):
        await asyncio.sleep(30)
        while self.active:
            cfg = self.bot.config.get('commands', {}).get('quest', {})
            if not self.bot.paused and cfg.get('enabled', True):
                await self.bot.send_message("quest")
                ih = cfg.get('interval_h', 3) 
                await asyncio.sleep(ih * 3600)
            else:
                await asyncio.sleep(60)
        
    async def on_message(self, message):
        content = message.content.lower()
        if message.author.id == self.bot.user_id:
            if message.channel.id != self.bot.channel_id: return
            if content == "owo" or content == "uwu": self._update_prog("owo")
            return

        core_config = self.bot.config.get('core', {})
        monitor_id = str(core_config.get('monitor_bot_id', '408785106942164992'))
        if str(message.author.id) != monitor_id: return
        if message.channel.id != self.bot.channel_id: return
        
        full_text = self.bot.get_full_content(message)
        
        if "quest log" in full_text or "checklist" in full_text:
            if not self.bot.is_message_for_me(message, role="header"):
                return
            
            cookie_m = re.search(r'cookie\s+from\s+(\d+)\s+friends?.*?\[(\d+)/(\d+)\]', full_text)
            if cookie_m:
                self.quests['cookie'] = {'target': int(cookie_m.group(3)), 'progress': int(cookie_m.group(2))}

            hunt_m = re.search(r'hunt\s+(\d+)\s+times?.*?\[(\d+)/(\d+)\]', full_text)
            if hunt_m:
                self.quests['hunt'] = {'target': int(hunt_m.group(3)), 'progress': int(hunt_m.group(2))}
            
            battle_m = re.search(r'battle\s+(\d+)\s+times?.*?\[(\d+)/(\d+)\]', full_text)
            if battle_m:
                self.quests['battle'] = {'target': int(battle_m.group(3)), 'progress': int(battle_m.group(2))}
            
            owo_m = re.search(r'type\s+owo\s+(\d+)\s+times?.*?\[(\d+)/(\d+)\]', full_text)
            if owo_m:
                self.quests['owo'] = {'target': int(owo_m.group(3)), 'progress': int(owo_m.group(2))}

            self.bot.log("SYS", "Quest Log Parsed.")
        
        if "and caught a" in content: self._update_prog("hunt")
        elif "battle" in content and "won" in content: self._update_prog("battle")

    def _update_prog(self, qtype):
        q = self.quests.get(qtype)
        if q and q['target'] > 0 and q['progress'] < q['target']:
            q['progress'] += 1
            if q['progress'] == q['target']:
                self.bot.log("SUCCESS", f"QUEST COMPLETED: {qtype.upper()}")


async def setup(bot):
    cog = Quest(bot)
    bot.add_listener(cog.on_message, 'on_message')
    await cog.start()