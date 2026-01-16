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
import re
import random
import core.state as state

class Gems:
    def __init__(self, bot):
        self.bot = bot
        self.active = True
        
        self.gem_tiers = {
            "fabled": ["057", "071", "078", "085"],
            "legendary": ["056", "070", "077", "084"],
            "mythical": ["055", "069", "076", "083"],
            "epic": ["054", "068", "075", "082"],
            "rare": ["053", "067", "074", "081"],
            "uncommon": ["052", "066", "073", "080"],
            "common": ["051", "065", "072", "079"],
        }
        
        self.inventory_check = False
        self.last_inv_time = 0

    def convert_small_numbers(self, text):
        mapping = str.maketrans("⁰¹²³⁴⁵⁶⁷⁸⁹", "0123456789")
        nums = "".join(filter(str.isdigit, text.translate(mapping)))
        return int(nums) if nums else 0

    def find_gems_available(self, content):
        matches = re.findall(r"`(\d+)`.*?([⁰¹²³⁴⁵⁶⁷⁸⁹]+)", content)
        available = {}
        for gid, count_str in matches:
            available[gid] = self.convert_small_numbers(count_str)
        return available

    def find_gems_to_use(self, available):
        cnf = self.bot.config.get('commands', {}).get('gems', {})
        tier_cfg = cnf.get('tiers', {})
        type_cfg = cnf.get('types', {})
        order_cfg = cnf.get('order', {})

        tier_priority = ['fabled', 'legendary', 'mythical', 'epic', 'rare', 'uncommon', 'common']
        
        if order_cfg.get('lowestToHighest', False):
            tier_priority.reverse()

        desired_types = []
        if type_cfg.get('huntGem', True): desired_types.append('huntGem')
        if type_cfg.get('empoweredGem', True): desired_types.append('empoweredGem')
        if type_cfg.get('luckyGem', True): desired_types.append('luckyGem')
        if type_cfg.get('specialGem', False): desired_types.append('specialGem')

        type_to_index = {
            "huntGem": 0,
            "empoweredGem": 1, 
            "luckyGem": 2,
            "specialGem": 3
        }

        use_set = cnf.get('use_gems_set', False)
        
        if use_set:
            for tier in tier_priority:
                if not tier_cfg.get(tier, True): continue
                
                tier_ids = self.gem_tiers.get(tier)
                if not tier_ids: continue

                has_all = True
                temp_gems = []
                
                for g_type in desired_types:
                    idx = type_to_index.get(g_type)
                    if idx is None or idx >= len(tier_ids): 
                        has_all = False
                        break
                    
                    gem_id = tier_ids[idx]
                    if available.get(gem_id, 0) < 1:
                        has_all = False
                        break
                    temp_gems.append(gem_id)
                
                if has_all:
                    for g in temp_gems:
                        available[g] -= 1
                    return temp_gems
            
        gems_to_equip = []
        for g_type in desired_types:
            idx = type_to_index.get(g_type)
            if idx is None: continue

            for tier in tier_priority:
                if not tier_cfg.get(tier, True): continue
                
                tier_ids = self.gem_tiers.get(tier)
                if not tier_ids or idx >= len(tier_ids): continue
                
                gem_id = tier_ids[idx]

                if available.get(gem_id, 0) > 0:
                    gems_to_equip.append(gem_id)
                    available[gem_id] -= 1
                    break

        return gems_to_equip if gems_to_equip else None

    async def on_message(self, message):
        core_config = self.bot.config.get('core', {})
        monitor_id = str(core_config.get('monitor_bot_id', '408785106942164992'))
        
        if str(message.author.id) != monitor_id:
            return
        if message.channel.id != self.bot.channel_id:
            return
        
        content = message.content.lower()
        
        gems_config = self.bot.config.get('commands', {}).get('gems', {})
        if not gems_config.get('enabled', False):
            return

        if "caught" in content:
            if not self.bot.is_message_for_me(message):
                return
            gem_indicators = ["<:gem", "💎", ":egem"]
            if not any(g in content for g in gem_indicators):
                now = time.time()
                if now - self.last_inv_time > 30: 
                    self.bot.log("SYS", "🔍 Gems missing! Triggering inventory check.")
                    self.inventory_check = True
                    self.last_inv_time = now
                    await self.bot.send_message(f"{self.bot.prefix}inv")

        elif "'s inventory" in content and "**" in content:
            if not self.bot.is_message_for_me(message, role="header"):
                return
            if self.inventory_check:
                self.inventory_check = False
                available = self.find_gems_available(message.content)
                to_use = self.find_gems_to_use(available)
                
                if to_use:
                    use_cmd = f"{self.bot.prefix}use {' '.join([gid[1:] if gid.startswith('0') else gid for gid in to_use])}"
                    await self.bot.send_message(use_cmd)
                    self.bot.log("SUCCESS", f"💎 Auto-Equipped: {use_cmd}")
                    state.stats['gems_used'] = state.stats.get('gems_used', 0) + len(to_use)
                else:
                    self.bot.log("WARN", "No eligible gems found in inventory.")

async def setup(bot):
    cog = Gems(bot)
    bot.add_listener(cog.on_message, 'on_message')
