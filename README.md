<div align="center">
  <h1>🧠 NeuraSelf</h1>
  
  <img src="https://readme-typing-svg.herokuapp.com/?font=Pacifico&size=40&pause=1000&color=FF0000&center=true&vCenter=true&random=false&width=600&lines=Advanced+OwO+Automation;Built+by+ROUTO" alt="NeuraSelf">
  
  <br/>
  <br/>

  <a href="https://discord.gg/BnrnHzjeNj">
    <img src="https://invidget.switchblade.xyz/BnrnHzjeNj" alt="Discord Community"/>
  </a>
  
  <br/>
  <br/>

  <img src="https://img.shields.io/badge/NeuraSelf-Advanced_Automation-red?style=for-the-badge&logo=discord&logoColor=white" />
  <img src="https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/License-Private-green?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Status-Active-success?style=for-the-badge" />
  
  <br/>
  <br/>

  <img src="https://img.shields.io/badge/discord.py--self-Latest-5865F2?style=flat-square&logo=discord&logoColor=white" />
  <img src="https://img.shields.io/badge/Flask-2.3.0-000000?style=flat-square&logo=flask&logoColor=white" />
  <img src="https://img.shields.io/badge/aiohttp-3.12.15-2C5BB4?style=flat-square&logo=aiohttp&logoColor=white" />

</div>

---

> [!IMPORTANT]
> ⚠️🚨 **WE ARE NOT responsible if you get banned using our selfbots.** Selfbots are against Discord ToS and break OwO bot rules. Use only in private servers and do not openly share that you are using automation.

## What is NeuraSelf?

**NeuraSelf** is a powerful automation tool designed for Discord's OwO bot. It features human-like behavior, multi-layer security, and a premium web dashboard for real-time monitoring.

---

## Key Features

-**Advanced AutoGems**: Intelligent gem sets (Fabled/Legendary) or mixed tiers.
-**Dynamic Quest Intelligence**: Auto-completes checklists and tracks progression.
-**Undetectable Stealth**: Realistic typing simulation with mistakes and backspacing.
-**Premium Dashboard**: Real-time stats, charts, and live configuration editor.
-**HuntBot Solver**: Automatically deploys and tracks HuntBots with captcha sensing.
-**Channel Switcher**: Automatic rotation between multiple channels for safety.

---

## Installation & Setup

### Option 1: One-Click Setup (Windows)

1. Run `neura_setup.bat`.
2. Follow the on-screen prompts to install Python and dependencies.
3. Enter your **Discord Token** and **Channel ID** when asked.
4. The bot will launch automatically.

### Option 2: Manual Setup

1. Download **Python 3.10** or higher.
2. Download **Git** and clone the repository:

   ```bash
   git clone https://github.com/routo-loop/neura-self
   cd neura-self
   ```

3. Install the required libraries:

   ```bash
   pip install -r requirements.txt
   ```

4. Run the configuration helper:

   ```bash
   python config_helper.py
   ```

5. Start the bot:

   ```bash
   python neura.py
   ```

---

## How to Configure

NeuraSelf uses two main configuration files:

### 1. `config/accounts.json` (Master List)

This is where you store your account credentials.

- **Token**: Your Discord account token.
- **Channels**: The list of channel IDs where the bot is allowed to grind.

> **Note**: For the "Channel Switcher" to work, make sure all channel IDs are added here first.

### 2. `config/settings.json` (Behavior)

This controls how the bot behaves (cooldowns, autosell, types of gems to use).

- **AutoChannel**: Add the channel IDs here to rotate between them. They must match IDs in `accounts.json`.
- **Stealth**: Configure typing speed and mistake rates.

---

## Dashboard Access

Once the bot is running, open your browser and go to:
`http://localhost:8000`

---

## ⚠️ Disclaimer

This tool is for **educational purposes only**. Using self-bots violates Discord's Terms of Service and may result in account termination.

<div align="center">

### NeuraSelf

**Advanced OwO Automation** • Built by **ROUTO** • Made with ❤️

**Star ⭐ this project if you find it useful!**

</div>
