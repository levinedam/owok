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

import json
import os
from rich.console import Console
from rich.prompt import Prompt

console = Console()

def setup_config():
    acc_path = 'config/accounts.json'
    
    if not os.path.exists(acc_path):
        os.makedirs('config', exist_ok=True)
        with open(acc_path, 'w') as f:
            json.dump({"accounts": []}, f, indent=4)

    with open(acc_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            console.print("[bold red]Error:[/] Failed to parse accounts.json")
            return

    accounts = data.get('accounts', [])
    modified = False
    
    if not accounts:
        accounts = [{"name": "Selfbot-1", "token": "YOUR_TOKEN", "channels": ["CHANNEL_ID"], "enabled": True}]
        data['accounts'] = accounts
        modified = True

    acc = accounts[0]

    if acc.get('token') in ["YOUR_TOKEN", "", None]:
        console.print("\n[bold yellow]--- NEURASELF SETUP: ACCOUNT TOKEN ---[/]")
        token = Prompt.ask("[cyan]Please enter your Discord Token[/]").strip()
        if token:
            acc['token'] = token
            modified = True
        else:
            console.print("[bold red]Warning:[/] Token not provided.")

    if not acc.get('channels') or acc['channels'][0] in ["CHANNEL_ID", "", None]:
        console.print("\n[bold yellow]--- NEURASELF SETUP: CHANNEL ID ---[/]")
        channel = Prompt.ask("[cyan]Please enter a Target Channel ID[/]").strip()
        if channel:
            acc['channels'] = [channel]
            modified = True
        else:
            console.print("[bold red]Warning:[/] Channel ID not provided.")

    if modified:
        with open(acc_path, 'w') as f:
            json.dump(data, f, indent=4)
        console.print("\n[bold green]Accounts configuration updated successfully![/]")
        console.print("[white]You can now run [bold cyan]python neura.py[/bold cyan] to start the bot.[/]")
    else:
        console.print("\n[bold green]Configuration is already set. Skipping prompts.[/]")

if __name__ == "__main__":
    setup_config()
