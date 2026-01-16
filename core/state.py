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


from collections import deque
import time
import json
import utils.history_tracker as ht

bot_instances = []
bot_paused = False
active_session_start = time.time()
log_config = {}
try:
    with open('config/logmisc.json', 'r') as f:
        log_config = json.load(f)
except:
    pass

stats = {
    'uptime_start': time.time(),
    'start_cash': 0,
    'current_cash': 0,
    'cowoncy_history': [],
    'gems_used': 0,
    'captchas_solved': 0,
    'bans_detected': 0,
    'warnings_detected': 0,
    'hunt_count': 0,
    'battle_count': 0,
    'last_captcha_msg': '',
    'accounts': [],
    'current_captcha': None,
    'captchas_solved_today': 0,
    'captcha_success_count': 0,
    'pending_commands': [],
    'last_cooldown': {},
    'total_cmd_count': 0,
    'other_count': 0
}

command_logs = deque(maxlen=500)
full_session_history = []

def log_command(type, message, status="info"):
    hex_color = log_config.get("colors", {}).get(type, "#ffffff")
    if "Sent: owo " in message:
        split_msg = message.split("Sent: owo ")
        if len(split_msg) > 1:
            cmd_part = split_msg[1].split(" ")[0].lower()
            if cmd_part in log_config.get("commands", {}):
                hex_color = log_config["commands"][cmd_part]
    elif "RPP: owo " in message:
        hex_color = log_config.get("commands", {}).get("rpp", "#00ffff")
    entry = {
        "time": time.strftime("%I:%M:%S %p"),
        "timestamp": time.time(),
        "type": type,
        "message": message,
        "status": status,
        "color": hex_color
    }
    command_logs.appendleft(entry)
    if len(full_session_history) >= 500:
        full_session_history.pop(0)
    full_session_history.append(entry)
    if type == "CMD":
        cmd = "other"
        parts = message.split("Sent: ")
        if len(parts) > 1:
            full_text = parts[1].lower().strip()
            if full_text.startswith("owo "):
                cmd_parts = full_text.split()
                cmd_text = cmd_parts[1] if len(cmd_parts) > 1 else "owo"
            else:
                cmd_text = full_text.split()[0]
            
            if cmd_text in ["hunt", "h"]: 
                cmd = "hunt"
                stats['hunt_count'] += 1
            elif cmd_text in ["battle", "b"]: 
                cmd = "battle"
                stats['battle_count'] += 1
            elif "autohunt" in cmd_text: 
                cmd = "captcha"
            elif cmd_text == "owo":
                cmd = "other"
                stats['other_count'] += 1
            else:
                stats['other_count'] += 1
            
            stats['total_cmd_count'] += 1

        history = ht.load_history()
        ht.track_command(history, cmd)

def record_snapshot():
    now = time.time()
    stats['cowoncy_history'].append((now, stats['current_cash']))
    history = ht.load_history()
    ht.track_cash(history, stats['current_cash'])
    if len(stats['cowoncy_history']) > 100:
        stats['cowoncy_history'].pop(0)