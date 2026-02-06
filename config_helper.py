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
import sys
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt, Confirm

import core.state as state

console = Console()

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def load_accounts():
    path = os.path.join(state.CONFIG_DIR, 'accounts.json')
    if not os.path.exists(state.CONFIG_DIR):
        os.makedirs(state.CONFIG_DIR)
    if not os.path.exists(path):
        return []
    try:
        with open(path, 'r') as f:
            data = json.load(f)
            return data.get('accounts', [])
    except:
        return []

def save_accounts(accounts):
    path = os.path.join(state.CONFIG_DIR, 'accounts.json')
    with open(path, 'w') as f:
        json.dump({"accounts": accounts}, f, indent=4)

def list_accounts(accounts):
    if not accounts:
        console.print("[yellow]No accounts found.[/yellow]")
        return
    table = Table(title="Manage Accounts")
    table.add_column("ID", justify="center", style="cyan")
    table.add_column("Name", style="green")
    table.add_column("Token", style="magenta")
    table.add_column("Channels", style="blue")
    table.add_column("Status", justify="center")

    for i, acc in enumerate(accounts):
        token_preview = f"{acc['token'][:10]}...{acc['token'][-5:]}" if len(acc['token']) > 15 else acc['token']
        channels = ", ".join(acc.get('channels', []))
        status = "[green]ON[/green]" if acc.get('enabled', True) else "[red]OFF[/red]"
        table.add_row(str(i + 1), acc.get('name', 'N/A'), token_preview, channels, status)
    
    console.print(table)

def add_account(accounts):
    # Check for placeholder account first
    placeholder_idx = -1
    for i, acc in enumerate(accounts):
        if acc.get('token') == "YOUR_TOKEN_HERE":
            placeholder_idx = i
            break

    if placeholder_idx != -1:
        console.print(f"[yellow]Placeholder account detected at index {placeholder_idx+1}. Replacing it...[/yellow]")

    name = Prompt.ask("Account Name (e.g. MyAccount)")
    token = Prompt.ask("User Token").strip()
    ch1 = Prompt.ask("Main Channel ID (Channel 1)").strip()
    ch2 = Prompt.ask("Secondary Channel ID (Channel 2, optional)", default="").strip()
    
    channels_set = set()
    if ch1: channels_set.add(ch1)
    if ch2: channels_set.add(ch2)
    channels = list(channels_set)
    
    new_acc = {
        "name": name,
        "token": token,
        "channels": channels,
        "enabled": True
    }

    if placeholder_idx != -1:
        accounts[placeholder_idx] = new_acc
        console.print("[green]Placeholder account updated successfully![/green]")
    else:
        accounts.append(new_acc)
        console.print("[green]Account added successfully![/green]")

    save_accounts(accounts)

def remove_account(accounts):
    list_accounts(accounts)
    if not accounts: return
    idx = Prompt.ask("Enter the ID of the account to remove", default="0")
    try:
        idx = int(idx) - 1
        if 0 <= idx < len(accounts):
            removed = accounts.pop(idx)
            save_accounts(accounts)
            console.print(f"[red]Removed account:[/] {removed.get('name')}")
        else:
            console.print("[yellow]Invalid ID.[/yellow]")
    except:
        console.print("[red]Error: Please enter a number.[/red]")

def menu():
    while True:
        clear()
        console.print(Panel.fit("[bold cyan]NEURASELF CONFIG HELPER[/bold cyan]\n[white]Easy account management[/white]\n [red]By Routo[/red]", border_style="blue"))
        accounts = load_accounts()
        list_accounts(accounts)
        
        console.print("\n[bold yellow]Options:[/bold yellow]")
        console.print(" 1. Add Account")
        console.print(" 2. Remove Account")
        console.print(" 3. Toggle Account Status")
        console.print(" 4. Back/Exit")
        
        choice = Prompt.ask("Select an option", choices=["1", "2", "3", "4"], default="4")
        
        if choice == "1":
            add_account(accounts)
            input("\nPress Enter to continue...")
        elif choice == "2":
            remove_account(accounts)
            input("\nPress Enter to continue...")
        elif choice == "3":
            if not accounts: continue
            idx = Prompt.ask("Enter ID to toggle", default="0")
            try:
                idx = int(idx) - 1
                if 0 <= idx < len(accounts):
                    accounts[idx]['enabled'] = not accounts[idx].get('enabled', True)
                    save_accounts(accounts)
                else:
                    console.print("[yellow]Invalid ID.[/yellow]")
            except: pass
        else:
            break

if __name__ == "__main__":
    menu()
