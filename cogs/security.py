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
import os
import threading
import unicodedata
import requests
import json
import discord
from discord.ext import commands
from playsound3 import playsound
from plyer import notification
import core.state as state

class Security(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        cfg = bot.config.get('security', {})
        self.enabled = cfg.get('enabled', True)
        self.notifications_enabled = cfg.get('notifications', {}).get('enabled', True)
        self.notification_title = cfg.get('notifications', {}).get('desktop_title', "Neura Security Alert")
        self.webhook_url = cfg.get('webhook_url')
        self.monitor_id = str(bot.config.get('core', {}).get('monitor_bot_id', '408785106942164992'))
        self.beep_file = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "beeps", "security_beep.mp3")
        self.ban_keywords = [
            "youhavebeenbanned",
            "bannedforbotting",
            "bannedformacros"
        ]
        self.captcha_keywords = [
            "areyouarealhuman",
            "verifythatyouarehuman",
            "pleasecompletethiswithin",
            "pleaseusethelinkbelow",
            "completeyourcaptcha",
            "pleasedmmewiththefollowing",
            "pleasedmmewithonly",
            "ifyouhavetroublesolvingthecaptcha",
            "pleasecomplete",
            "tocheckthatyouareahuman",
            "tocheck",
            "human"
        ]
        self.warning_pattern = re.compile(r'\((\d+)/(\d+)\)')
        self.image_captcha_keywords = [
            "pleasedmme",
            "dmme",
            "beepboop",
            "checkthatyouareahuman",
            "solvingthecaptcha"
        ]
        self.api_cfg = {}
        try:
            api_file = os.path.join(bot.base_dir, 'config', 'api.json')
            if os.path.exists(api_file):
                with open(api_file, 'r') as f:
                    self.api_cfg = json.load(f)
        except Exception as e:
            bot.log("ERROR", f"Failed to load api.json: {e}")

    def _normalize(self, text):
        if not text:
            return ""
        text = unicodedata.normalize("NFKD", text)
        return re.sub(r'[^a-zA-Z0-9]', '', text.lower())

    def _show_desktop_notification(self, message):
        if not self.notifications_enabled:
            return
        sec_cfg = self.bot.config.get('security', {})
        notif_cfg = sec_cfg.get('notifications', {})
        if self.bot.is_mobile:
            mobile = notif_cfg.get('mobile', {})
            if mobile.get('enabled', True):
                try:
                    os.system(f'termux-notification --title "{self.notification_title}" --content "{message}"')
                    vib = mobile.get('vibrate', {})
                    if vib.get('enabled', True):
                        duration = int(vib.get('time', 0.5) * 1000)
                        os.system(f'termux-vibrate -d {duration}')
                    toast = mobile.get('toast', {})
                    if toast.get('enabled', True):
                        bg = toast.get('bg_color', 'black')
                        fg = toast.get('text_color', 'white')
                        pos = toast.get('position', 'middle')
                        os.system(f'termux-toast -b {bg} -c {fg} -g {pos} "{message}"')
                    tts = mobile.get('tts', {})
                    if tts.get('enabled', False):
                        os.system(f'termux-tts-speak "{message}"')
                except:
                    pass
            return
        desktop = notif_cfg.get('desktop', {})
        if desktop.get('enabled', True):
            try:
                notification.notify(title=self.notification_title, message=message, timeout=10)
            except:
                pass
    
    def _send_webhook(self, title, message):
        cfg = self.bot.config.get('security', {})
        wh_cfg = cfg.get('webhook', {})
        if not wh_cfg.get('enabled', True): return
        url = wh_cfg.get('url')
        if not url: return
        payload = {
            "content": "@everyone @here",
            "embeds": [{
                "title": title,
                "description": message,
                "color": 0xFF3B3B,
                "author": {
                    "name": "NeuraSelf Security",
                    "icon_url": "https://cdn.discordapp.com/attachments/1450161614375620802/1456632606002118657/neuralogo.png"
                },
                "footer": {"text": "NeuraSelf • Captcha & Ban Protection"},
                "timestamp": time.strftime('%Y-%m-%dT%H:%M:%S')
            }]
        }
        try:
            requests.post(url, json=payload, timeout=5)
        except:
            pass

    async def play_beep(self):
        def _play():
            if os.path.exists(self.beep_file):
                try:
                     playsound(self.beep_file, block=False)
                except:
                    pass
        threading.Thread(target=_play, daemon=True).start()

    def _contains_keyword(self, text, keywords):
        cleaned = self._normalize(text)
        return any(k in cleaned for k in keywords)

    def _get_captcha_url(self, message):
        if not message.components:
            return None
        for comp in message.components:
            if not hasattr(comp, "children"): continue
            for child in comp.children:
                url = str(getattr(child, "url", "") or "")
                if "owobot.com/captcha" in url:
                    return url
        return None

    async def solve_2captcha(self, captcha_url):
        api_key = self.api_cfg.get('2captcha_api_key')
        if not api_key or api_key == "YOUR_API_KEY_HERE":
            self.bot.log("INFO", "2captcha: API Key missing.")
            return False
        if not self.api_cfg.get('solver_enabled', False):
            return False
        try:
            payload = {
                "key": api_key,
                "method": "hcaptcha",
                "sitekey": "4c672d35-0701-42b2-88c3-78380b0d3539",
                "pageurl": captcha_url,
                "json": 1
            }
            async with self.bot.session.post("http://2captcha.com/in.php", data=payload) as resp:
                data = await resp.json()
                if data.get("status") != 1: return False
                request_id = data.get("request")
            for _ in range(30):
                await asyncio.sleep(10)
                async with self.bot.session.get(f"http://2captcha.com/res.php?key={api_key}&action=get&id={request_id}&json=1") as resp:
                    res_data = await resp.json()
                    if res_data.get("status") == 1:
                        token = res_data.get("request")
                        async with self.bot.session.post(f"https://owobot.com/api/captcha/solve", json={"token": token, "url": captcha_url}) as owo_resp:
                            if owo_resp.status == 200:
                                self.bot.log("SUCCESS", "2captcha: Solved!")
                                return True
                        return True
                    if res_data.get("request") == "CAPCHA_NOT_READY": continue
                    else: return False
            return False
        except Exception as e:
            return False

    @commands.Cog.listener()
    async def on_message(self, message):
        if not self.enabled: return
        if isinstance(message.channel, discord.DMChannel) and message.author.id == int(self.monitor_id):
            if (discord.utils.utcnow() - message.created_at).total_seconds() > 30: return
            if "i have verified that you are human" in message.content.lower():
                self.bot.paused = False
                state.bot_paused = False
                self.bot.throttle_until = 0.0
                self.bot.log("SUCCESS", "Verified detected in DM. Resuming...")
                return
        if str(message.author.id) != self.monitor_id: return
        if message.channel.id != self.bot.channel_id: return
        content = message.content or ""
        embed_text = ""
        if message.embeds:
            parts = []
            for e in message.embeds:
                if e.title: parts.append(e.title)
                if e.description: parts.append(e.description)
                if e.footer and e.footer.text: parts.append(e.footer.text)
            embed_text = " ".join(parts)
        text_to_check = f"{content} {embed_text}"
        is_for_me = self.bot.is_message_for_me(message)
        if not is_for_me: return
        if self._contains_keyword(text_to_check, self.ban_keywords):
            self.bot.paused = True
            state.bot_paused = True
            self.bot.log("ALARM", "BAN DETECTED!")
            await self.play_beep()
            self._show_desktop_notification("Ban detected!")
            self._send_webhook("BAN DETECTED", f"Message:\n{content}")
            return
        warning_match = self.warning_pattern.search(content)
        if warning_match:
            current_warning = int(warning_match.group(1))
            max_warnings = int(warning_match.group(2))
            normalized = self._normalize(text_to_check)
            if any(kw in normalized for kw in ["pleasecomplete", "captcha", "verify", "human"]):
                self.bot.paused = True
                state.bot_paused = True
                self.bot.throttle_until = time.time() + 3600
                state.stats['last_captcha_msg'] = text_to_check[:200]
                self.bot.log("ALARM", f"CAPTCHA WARNING DETECTED ({current_warning}/{max_warnings})!")
                await self.play_beep()
                self._show_desktop_notification(f"Captcha warning {current_warning}/{max_warnings} detected!")
                self._send_webhook("CAPTCHA WARNING", f"Warning {current_warning}/{max_warnings}\nMessage:\n{content}")
                return
        has_image = len(message.attachments) > 0
        image_captcha_hit = self._contains_keyword(text_to_check, self.image_captcha_keywords)
        if has_image and image_captcha_hit:
            self.bot.paused = True
            state.bot_paused = True
            self.bot.throttle_until = time.time() + 3600
            state.stats['last_captcha_msg'] = text_to_check[:200]
            self.bot.log("ALARM", "IMAGE CAPTCHA DETECTED!")
            await self.play_beep()
            self._show_desktop_notification("Image captcha detected! Check DMs.")
            img_urls = "\n".join([att.url for att in message.attachments])
            self._send_webhook("IMAGE CAPTCHA DETECTED", f"Message:\n{content}\n\nImages:\n{img_urls}")
            return
        captcha_keywords_hit = self._contains_keyword(text_to_check, self.captcha_keywords)
        captcha_url = self._get_captcha_url(message)
        if captcha_url or (captcha_keywords_hit and message.components):
            self.bot.paused = True
            state.bot_paused = True
            self.bot.throttle_until = time.time() + 3600
            state.stats['last_captcha_msg'] = text_to_check[:200]
            self.bot.log("ALARM", "CAPTCHA DETECTED!")
            await self.play_beep()
            self._show_desktop_notification("Captcha detected!")
            self._send_webhook("CAPTCHA DETECTED", f"Solve: {captcha_url or 'https://owobot.com/captcha'}")
            if captcha_url and self.api_cfg.get('solver_enabled', False) and not getattr(self, '_solving', False):
                self._solving = True
                asyncio.create_task(self._run_solver(captcha_url))

    async def _run_solver(self, url):
        try:
             await self.solve_2captcha(url)
        finally:
            self._solving = False

async def setup(bot):
    await bot.add_cog(Security(bot))
