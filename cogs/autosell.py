import discord
from discord.ext import commands
import time
import core.state as state

class AutoSell(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.last_sell_time = 0
        self.is_selling = False

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.id != int(self.bot.owo_bot_id): return
        if message.channel.id != self.bot.channel_id: return
        content = message.content.lower()
        if not self.bot.is_message_for_me(message): return
        cfg = self.bot.config.get('auto_use', {}).get('autosell', {})
        if not cfg.get('enabled', False): return
        if "don't have enough cowoncy" in content or "not enough cowoncy" in content:
            if time.time() - self.last_sell_time > 300:
                self.is_selling = True
                await self.bot.send_message(f"sell {cfg.get('type', 'all')}")
                self.last_sell_time = time.time()
                self.bot.log("SYS", "Low funds detected. Triggered AutoSell.")

async def setup(bot):
    await bot.add_cog(AutoSell(bot))