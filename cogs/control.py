import asyncio
import time
from core import state

class Control:
    def __init__(self, bot):
        self.bot = bot

    async def on_message(self, message):
        if message.author.id != self.bot.user_id:
            return
            
        content = message.content.lower().strip()
        
        if content == '.stop':
            if not self.bot.paused:
                self.bot.paused = True
                state.bot_paused = True
                self.bot.log("SYS", "Bot PAUSED via Chat cmd")
                
        elif content == '.start' or content == '.resume':
            if self.bot.paused:
                self.bot.paused = False
                state.bot_paused = False
                state.active_session_start = time.time()
                self.bot.log("SYS", "Bot RESUMED via Chat Command")
                await self.bot.send_message("Bot resumed.")

        elif content == '.status':
            status = "PAUSED " if self.bot.paused else "RUNNING "

            uptime = time.time() - state.stats['uptime_start']
            hours = int(uptime // 3600)
            minutes = int((uptime % 3600) // 60)
            status += f"| Uptime: {hours}h {minutes}m"

async def setup(bot):
    cog = Control(bot)
    bot.add_listener(cog.on_message, 'on_message')