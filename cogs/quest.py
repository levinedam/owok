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

    async def start(self):
        self.task = asyncio.create_task(self.run_loop())

    async def run_loop(self):
        await self.bot.wait_until_ready()
        await asyncio.sleep(self.bot.get_startup_delay(offset=10))
        
        while self.active:
            cfg = self.bot.config.get('commands', {}).get('quest', {})
            if not self.bot.paused and cfg.get('enabled', True):
                if self.bot.is_ready:
                    await self.bot.send_message("quest")
                
                ih = cfg.get('interval_h', 6)
                await asyncio.sleep(ih * 3600)
            else:
                await asyncio.sleep(60)

    async def on_message(self, message):
        # 1. Basic Filters
        core_config = self.bot.config.get('core', {})
        monitor_id = str(core_config.get('monitor_bot_id', '408785106942164992'))
        
        if str(message.author.id) != monitor_id:
            return
        if self.bot.owo_user is None:
            self.bot.owo_user = message.author
        if message.channel.id != self.bot.channel_id:
            return

        full_text = self.bot.get_full_content(message)

        if "quest log" in full_text or "checklist" in full_text:
            is_for_me = self.bot.is_message_for_me(message, role="header")
            
            if not is_for_me:
                return
            
            self._parse_quests(full_text)

    def _parse_quests(self, text):
        progress_pattern = r'progress:\s*\[(\d+)/(\d+)\]'
        timer_pattern = r'next quest in:\s*(\d+h \d+m \d+s)'
        
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        new_quest_data = []
        
        st = self.bot.stats
        old_quests = st.get('quest_data', [])
        
        sync_count = 0

        for i, line in enumerate(lines):
            match = re.search(progress_pattern, line)
            if match:
                current = int(match.group(1))
                total = int(match.group(2))
                
                desc = "Unknown Quest"
                # Search backwards for the description
                for j in range(i-1, max(-1, i-4), -1):
                    # In OwO, the description is often followed IMMEDIATELY by 'reward:' on the same line.
                    # e.g. "**1. Hunt 50 times!** :blank: Reward: ..."
                    raw_line = lines[j]
                    
                    # If this line has progress or is a header, skip entirely
                    if any(x in raw_line.lower() for x in ["progress:", "quest log", "belong to", "next quest"]):
                        continue
                        
                    # If it has "reward:", the description is likely before it
                    desc_part = raw_line
                    if "reward:" in raw_line.lower():
                        # Split by reward (case insensitive)
                        parts = re.split(r'reward:', raw_line, flags=re.IGNORECASE)
                        desc_part = parts[0]
                    
                    # Clean up description
                    clean_desc = desc_part.replace(':blank:', '').replace('‣', '').replace('*', '').strip()
                    clean_desc = re.sub(r'^\d+[\)\.]\s*', '', clean_desc) # Remove "1." or "1)"
                    clean_desc = re.sub(r'<[^>]*>', '', clean_desc) # Remove Discord emoji tags like <:blank:id> or <id>
                    clean_desc = clean_desc.replace('`', '').strip() # Remove leftover backticks
                    
                    if clean_desc and len(clean_desc) > 3:
                        desc = clean_desc
                        break
                
                quest_item = {
                    'description': desc,
                    'current': current,
                    'total': total,
                    'completed': current >= total
                }
                new_quest_data.append(quest_item)
                
                if quest_item['completed']:
                    was_completed = any(q['description'] == desc and q.get('completed') for q in old_quests)
                    if not was_completed:
                        self.bot.log("SUCCESS", f"QUEST COMPLETED: {desc}")

        timer_match = re.search(timer_pattern, text)
        next_timer = timer_match.group(1).upper() if timer_match else None
        
        st['quest_data'] = new_quest_data
        st['next_quest_timer'] = next_timer
        
        if new_quest_data:
            self.bot.log("SYS", f"Dashboard synced: {len(new_quest_data)} quests tracked.")
            if any(q['description'] == "Unknown Quest" for q in new_quest_data):
                self.bot.log("DEBUG", "Some quests could not be named. Structure might be unusual.")
        elif "quest log" in text:
            self.bot.log("DEBUG", "Regex failure: Found 'Quest Log' but couldn't parse progress lines.")

async def setup(bot):
    cog = Quest(bot)
    bot.add_listener(cog.on_message, 'on_message')
    await cog.start()