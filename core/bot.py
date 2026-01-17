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


import discord
from discord.ext import commands
import json
import os
import time
import random
import asyncio
import re
import sys
import requests
from rich.console import Console,Align
from rich.text import Text
from modules.typing import TypingSimulator
import core.state as state
import aiohttp
import unicodedata

class NeuraBot(commands.Bot):
    def __init__(self, token=None, channels=None):
        self.session = None
        self.console = Console()
        self.base_dir = os.getcwd()
        self.config_file = os.path.join(self.base_dir, 'config', 'settings.json')
        
        self.config = {}
        self.accounts = []
        self._load_config()
        
        self.token = token
        self.channels = channels or []
        self._audio_count = 0
        
        if not self.token or not self.channels:
            if self.accounts:
                primary = self.accounts[0]
                self.token = self.token or primary.get('token')
                self.channels = self.channels or primary.get('channels', [])
        
        self.channel_id = int(self.channels[0]) if self.channels else None
        core_cfg = self.config.get('core', {})
        self.prefix = core_cfg.get('prefix', 'owo ')
        self.user_id = core_cfg.get('user_id')
        self.owo_bot_id = str(core_cfg.get('monitor_bot_id', '408785106942164992'))
        
        super().__init__(command_prefix=self.prefix, self_bot=True)
        
        self.username = "Bot"
        self.display_name = "Bot"
        self.nickname = None
        self.identifiers = []
        self.modules = {}
        self.active = True
        self.paused = False
        self.warmup_until = time.time() + 10
        self.throttle_until = 0.0
        self.last_sent_time = 0
        self.command_lock = asyncio.Lock()
        self.min_command_interval = 4.2
        self.command_history = []
        self.is_ready = False
        self.log_colors = {
            'SYS': 'cyan',
            'CMD': 'green',
            'INFO': 'blue',
            'SUCCESS': 'bright_green',
            'COOLDOWN': 'bright_yellow',
            'ALARM': 'bright_red',
            'ERROR': 'red',
            'SECURITY': 'red',
            'AutoHunt': 'bright_cyan'
        }
        self.cmd_cooldowns = {}
    
    async def setup_hook(self):
        self.session = aiohttp.ClientSession()
        self.log("SYS", "Initializing systems...")
        
        try:
            history = state.ht.load_history()
            state.ht.start_session(history)
        except Exception as e:
            self.log("ERROR", f"Failed to start history session: {e}")

        asyncio.create_task(self._process_pending_commands())
        await self._load_modules()
    
    async def _process_pending_commands(self):
        await asyncio.sleep(5)
        while True:
            if not self.is_ready:
                await asyncio.sleep(1)
                continue
            if 'pending_commands' in state.stats and state.stats['pending_commands']:
                pending = state.stats['pending_commands'][:]
                for cmd_data in pending:
                    if time.time() - cmd_data['timestamp'] < 300:
                        success = await self.send_message(cmd_data['command'])
                        if success:
                            state.stats['pending_commands'] = [
                                c for c in state.stats['pending_commands'] 
                                if c['timestamp'] != cmd_data['timestamp']
                            ]
                    else:
                        state.stats['pending_commands'] = [
                            c for c in state.stats['pending_commands'] 
                            if c['timestamp'] != cmd_data['timestamp']
                        ]
            await asyncio.sleep(2)
    
    async def on_ready(self):
        self.is_ready = True
        self.user_id = self.user.id
        self.username = self.user.name
        self.display_name = self.user.display_name
        self.identifiers = [
            self.username.lower(),
            self.display_name.lower(),
            f"<@{self.user_id}>",
            f"<@!{self.user_id}>"
        ]
        self.log("SYS", f"Ready as {self.username} (Display: {self.display_name})")
        self.log("INFO", f"Channel: {self.channel_id}")
    
    async def _send_safe(self, content, skip_typing=False):
        if not content or not self.is_ready:
            return False
            
        content = self._fix_command(content)
        current_time = time.time()
        
        if current_time < self.warmup_until:
             await asyncio.sleep(max(0.1, self.warmup_until - current_time))

        if current_time < self.throttle_until:
            wait = self.throttle_until - current_time
            self.log("COOLDOWN", f"Throttled. Waiting {round(wait, 1)}s")
            await asyncio.sleep(wait + 0.5)
            
        channel = self.get_channel(self.channel_id) or await self.fetch_channel(self.channel_id)
        if not channel: return False
        
        try:
            stealth = self.config.get('stealth', {}).get('typing', {})
            if stealth.get('enabled', False) and not skip_typing:
                sent_ok = await TypingSimulator.send(self, channel, content)
                if not sent_ok: return False
            else:
                await channel.send(content)
                
            short_cmd = content[:30] + "..." if len(content) > 30 else content
            self.log("CMD", f"Sent: {short_cmd}")
            return True
        except Exception as e:
            self.log("ERROR", f"Send failed: {str(e)}")
            return False
    
    def _fix_command(self, command):
        cmd = command.strip()
        if cmd.lower() == "owo": return "owo"
        if cmd.lower().startswith("owo owo"): cmd = cmd[4:]
        known = ['hunt', 'battle', 'curse', 'huntbot', 'daily', 'cookie',
                'quest', 'checklist', 'cf', 'slots', 'autohunt', 'upgrade',
                'sacrifice', 'team', 'zoo', 'use', 'inv', 'sell', 'crate',
                'lootbox', 'run', 'pup', 'piku']
        first = cmd.lower().split()[0] if cmd else ""
        if first in known and not cmd.lower().startswith(self.prefix.lower()):
            return f"{self.prefix}{cmd}"
        return cmd
    
    async def send_message(self, content, skip_typing=False, priority=False):
        if not self.active: return False
        if self.paused and "autohunt" not in content.lower() and "check" not in content.lower():
            return False
        
        wait_limit = 1.2 if priority else self.min_command_interval
        
        async with self.command_lock:
            now = time.time()
            elapsed = now - self.last_sent_time
            if elapsed < wait_limit:
                await asyncio.sleep(wait_limit - elapsed)
            
            self.last_sent_time = time.time()
            self.last_sent_command = content

        success = await self._send_safe(content, skip_typing=skip_typing)
        return success
    
    async def _load_modules(self):
        if not os.path.exists('cogs'):
            os.makedirs('cogs')
        files = os.listdir('cogs')
        for file in files:
            if file.endswith('.py'):
                try:
                    module_name = f'cogs.{file[:-3]}'
                    module = __import__(module_name, fromlist=[''])
                    if hasattr(module, 'setup'):
                        await module.setup(self)
                        self.modules[file] = module
                        self.log("SYS", f"Loaded {file}")
                except Exception as e:
                    self.log("ERROR", f"Failed to load {file}: {e}")
    
    def _load_config(self):
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    self.config = json.load(f)
            else:
                self.config = {}
            
            account_file = os.path.join(self.base_dir, 'config', 'accounts.json')
            if os.path.exists(account_file):
                with open(account_file, 'r') as f:
                    self.accounts = json.load(f)
            else:
                self.accounts = []

            self.is_mobile = self._is_termux()
        except Exception as e:
            print(f"Error loading config: {e}")
            self.config = {}

    def _is_termux(self):
        termux_prefix = os.environ.get("PREFIX")
        termux_home = os.environ.get("HOME")
        if (termux_prefix and "com.termux" in termux_prefix) or \
           (termux_home and "com.termux" in termux_home) or \
           os.path.isdir("/data/data/com.termux"):
            return True
        return False

    def check_version(self):
        CURRENT_VERSION = "2.0.0" 
        VERSION_URL = "https://raw.githubusercontent.com/routo-loop/neura_status_api/main/version.json"
        
        self.log("SYS", "Checking for updates...")
        try:
            r = requests.get(VERSION_URL, timeout=5)
            if r.status_code == 200:
                data = r.json()
                latest_version = data.get("version", "2.0.0")
                changelog = data.get("changelog", "No changes listed.")
                
                if latest_version != CURRENT_VERSION:
                    os.system('cls' if os.name == 'nt' else 'clear')
                    line = "┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈"
                    self.console.print("\n")
                    self.console.print(Align.center(f"[bold red]{line}[/bold red]"))
                    self.console.print(Align.center(f"[bold white]   NEW VERSION AVAILABLE: [yellow]{latest_version}[/yellow] (Current: {CURRENT_VERSION})[/bold white]"))
                    self.console.print(Align.center(f"[bold red]{line}[/bold red]"))
                    self.console.print(Align.center(f"\n[bold cyan]CHANGELOG:[/bold cyan]\n[white]{changelog}[/white]\n"))
                    self.console.print(Align.center(f"[bold red]{line}[/bold red]"))
                    self.console.print(Align.center("[bold yellow]PLEASE UPDATE TO CONTINUE:[/bold yellow]"))
                    self.console.print(Align.center("[bold cyan]https://github.com/routo-loop/neura-self[/bold cyan]"))
                    self.console.print(Align.center(f"[bold red]{line}[/bold red]"))
                    self.console.print("\n")
                    sys.exit(0)
                else:
                    self.log("SYS", "You are on the latest version.")
        except Exception as e:
            self.log("WARN", f"Version check failed: {e}")
    
    async def run_bot(self):
        self.check_version()
        self.log("SYS", f"Detected Platform: {'Mobile (Termux)' if self.is_mobile else 'Desktop (Windows/Linux)'}")
        self.log("SYS", "Starting bot...")
        await self.start(self.token)

    def set_cooldown(self, cmd, seconds):
        self.cmd_cooldowns[cmd.lower()] = time.time() + seconds

    def get_cooldown(self, cmd):
        return max(0, self.cmd_cooldowns.get(cmd.lower(), 0) - time.time())

    def log(self, level, msg):
        ts = time.strftime("%H:%M:%S")
        color = self.log_colors.get(level, "white")
        bracket_level = f"[{level}]"
        self.console.print(f"[{color}][{ts}] {bracket_level:<10}[/{color}] [white]{msg}[/white]")
        state.log_command(level, msg, "info")

    def get_full_content(self, message):
        if not message: return ""
        content = message.content or ""
        embed_texts = []
        if message.embeds:
            for em in message.embeds:
                parts = [
                    em.title or "",
                    em.author.name if em.author else "",
                    em.description or "",
                    " ".join([f"{f.name} {f.value}" for f in em.fields])
                ]
                embed_texts.append(" ".join(parts))
        return (content + " " + " ".join(embed_texts)).lower()


    def is_message_for_me(self, message, role="any", keyword=None):
        if not message: return False
        
        def clean_text(text):
            if not text: return ""
            clean = "".join(ch for ch in text if unicodedata.category(ch)[0] != 'C')
            clean = clean.replace('\u200b', '').replace('\u200c', '').replace('\u200d', '').replace('\ufeff', '')
            return clean.lower().strip()

        content = clean_text(message.content)
        
        if self.user.mentioned_in(message): return True

        
        idents = [self.user.name, self.display_name] + self.identifiers
        clean_idents = set()
        for i in idents:
            ci = re.sub(r'[^\w\s]', '', i.lower()).strip()
            if ci and len(ci) >= 2: clean_idents.add(ci)
            
        content = (message.content or "").lower()
        if message.guild:
            member = message.guild.get_member(self.user.id)
            if member and member.nick:
                nick = member.nick.lower()
                clean_nick = re.sub(r'[^\w\s]', '', nick).strip()
                if clean_nick: clean_idents.add(clean_nick)

        if role == "header":
            first_line = content.split('\n')[0]
            header_texts = [first_line]
            if message.embeds:
                for em in message.embeds:
                    if em.title: header_texts.append(em.title.lower())
            
            for text in header_texts:
                for ident in clean_idents:
                    if re.search(rf"\b{re.escape(ident)}\b", text): return True
            return False

        if role in ["source", "target"] and keyword:
            keyword = keyword.lower()
            if keyword in content:
                parts = content.split(keyword, 1)
                check_text = parts[0] if role == "source" else parts[1]
                for ident in clean_idents:
                    if re.search(rf"\b{re.escape(ident)}\b", check_text): return True
            return False

        texts = [content]
        if message.embeds:
            for em in message.embeds:
                fields_text = " ".join([f"{f.name} {f.value}" for f in em.fields])
                texts.append(f"{em.title or ''} {em.author.name if em.author else ''} {em.description or ''} {fields_text}".lower())

        for text in texts:
            for ident in clean_idents:
                if re.search(rf"\b{re.escape(ident)}\b", text):
                    return True

        generic_patterns = [
            "beep boop", "i am back with", "i will be back in",
            "please include your password", "password will reset in",
            "confirm your identity", "link below", "here is your password",
            "wrong password", "incorrect password"
        ]
        
        full_visible_text = " ".join(texts)
        if any(pat in full_visible_text for pat in generic_patterns):
            return True

        return False
