import asyncio
import re
import time
import core.state as state

class CooldownManager:
    def __init__(self, bot):
        self.bot = bot
        self.config = bot.config
        
    async def on_message(self, message):
        monitor_id = str(self.bot.config.get('monitor_bot_id', '408785106942164992'))
        if str(message.author.id) != monitor_id:
            return
        if message.channel.id != self.bot.channel_id:
            return
        
        content = message.content.lower()
        
        # Handle "slow down" messages
        if "slow down" in content or "try the command again" in content:
            # Extract time (handle "1 seconds" typo)
            seconds = 1
            match = re.search(r'(\d+)\s*seconds?', content, re.I)
            if match:
                seconds = int(match.group(1))
            elif "1 seconds" in content:
                seconds = 1
            
            # Set throttle with buffer
            self.bot.throttle_until = time.time() + seconds + 3.0
            
            # Log to state
            state.stats['last_cooldown'] = {
                'seconds': seconds,
                'command': getattr(self.bot, 'last_sent_command', ''),
                'message': content,
                'timestamp': time.time()
            }
            
            self.bot.log("COOLDOWN", f"SLOW DOWN: {seconds}s (waiting {seconds + 3}s)")
            
        elif "too tired to run" in content:
            self.bot.user_status['too_tired_run'] = True
            self.bot.log("COOLDOWN", "Too tired to run")
            
        elif "again in" in content:
            match = re.search(r'again in (\d+)\s*s', content)
            if match:
                seconds = int(match.group(1))
                self.bot.throttle_until = time.time() + seconds + 2.0
                self.bot.log("COOLDOWN", f"Wait {seconds}s (+2s buffer)")

async def setup(bot):
    cog = CooldownManager(bot)
    bot.add_listener(cog.on_message, 'on_message')