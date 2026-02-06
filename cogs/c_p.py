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

from discord.ext import commands
import asyncio
import time
import random
import re
import json
import os

class CursePray(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.state_file = "config/cp_state.json"
        self.active = True
        self.last_run = self._load_last_run()
        self.loop_task = asyncio.create_task(self.loop())

    def _load_last_run(self):
        if os.path.exists(self.state_file):
            try:
                with open(self.state_file, "r") as f:
                    data = json.load(f)
                    return data.get("cp_last_run", 0)
            except:
                pass
        return 0

    def _save_last_run(self):
        data = {}
        if os.path.exists(self.state_file):
            try:
                with open(self.state_file, "r") as f:
                    data = json.load(f)
            except:
                pass
        data["cp_last_run"] = self.last_run
        with open(self.state_file, "w") as f:
            json.dump(data, f)

    async def loop(self):
        self.bot.log("SYS", "Curse/Pray module started.")
        await self.bot.wait_until_ready()
        await asyncio.sleep(self.bot.get_startup_delay(offset=10))
        while self.active:
            cmds_cfg = self.bot.config.get("commands", {})
            curse_cfg = cmds_cfg.get("curse", {})
            pray_cfg = cmds_cfg.get("pray", {})
            
            if self.bot.paused or (not curse_cfg.get("enabled", False) and not pray_cfg.get("enabled", False)):
                await asyncio.sleep(5)
                continue

            available = []
            if curse_cfg.get("enabled", False): available.append("curse")
            if pray_cfg.get("enabled", False): available.append("pray")
            
            if not available:
                await asyncio.sleep(5)
                continue
                
            choice = random.choice(available)
            cfg = curse_cfg if choice == "curse" else pray_cfg
            
            cooldown_range = cfg.get("cooldown", [305, 310])
            cur_cooldown = random.uniform(cooldown_range[0], cooldown_range[1])

            if time.time() - self.last_run > cur_cooldown:
                await self._execute(choice, cfg)
                self.last_run = time.time()
                self._save_last_run()
            await asyncio.sleep(5)

    async def _execute(self, cmd, cfg):
        targets = cfg.get("targets", [])
        if not isinstance(targets, list):
            targets = [targets]
            
        if targets:
            target = random.choice(targets)
            if cfg.get("ping", True):
                full_cmd = f"{cmd} <@{target}>"
            else:
                full_cmd = f"{cmd} {target}"
        else:
            full_cmd = cmd
            
        await self.bot.send_message(full_cmd)
        self.bot.log("CMD", f"Executed: {full_cmd}")

    @commands.Cog.listener()
    async def on_message(self, message):
        await self._process_response(message)

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        await self._process_response(after)

    async def _process_response(self, message):
        core_config = self.bot.config.get("core", {})
        monitor_id = str(core_config.get("monitor_bot_id", "408785106942164992"))
        if str(message.author.id) != monitor_id:
            return
        if message.channel.id != self.bot.channel_id:
            return
            
        full_content = self.bot.get_full_content(message)
        
        is_for_me = self.bot.is_message_for_me(message)
        
        success_triggers = [
            "puts a curse on", "is now cursed.",
            "prays for", "prays..."
        ]
        
        if is_for_me and any(t in full_content for t in success_triggers):
            self.last_run = time.time()
            self._save_last_run()
            self.bot.log("SUCCESS", "Spiritual action confirmed, cooldown reset.")

        if "Slow down and try the command again" in full_content:
            self.last_run = time.time()
            self._save_last_run()
            self.bot.log("COOLDOWN", "Rate limit detected for spiritual command.")

async def setup(bot):
    await bot.add_cog(CursePray(bot))
