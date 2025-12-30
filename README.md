<div align="center">
  <h1>🧠 NeuraSelf</h1>
  
  <img src="https://readme-typing-svg.herokuapp.com/?font=Pacifico&size=40&pause=1000&color=FF0000&center=true&vCenter=true&random=false&width=600&lines=Advanced+OwO+Automation;Built+by+ROUTO" alt="NeuraSelf">
  
  <br/>
  <br/>

  <a href="https://discord.gg/mHU4bESA4p">
    <img src="https://invidget.switchblade.xyz/mHU4bESA4p" alt="Discord Community"/>
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
  <img src="https://img.shields.io/badge/Rich-14.2.0-009485?style=flat-square" />
  <img src="https://img.shields.io/badge/playsound3-3.3.0-FF6B6B?style=flat-square" />
  <img src="https://img.shields.io/badge/plyer-2.1.0-4CAF50?style=flat-square" />

</div>

---

> [!IMPORTANT]

> ⚠️🚨 WE ARE NOT responsible if you get banned using our selfbots. Selfbots are agains discord tos and also breaks owo bots rules. If you do plan on using it still then atleast take some steps to ensure that you won't be getting banned like no more than one/two account grinding in one servers, Only grinding in private servers, And not openly sharing the fact that you use selfbot to grind owo.


## 📖 What is NeuraSelf?

**NeuraSelf** is an advanced, feature-rich automation tool designed for Discord's OwO bot. Built with intelligence, stealth, and user experience in mind, it automates grinding, manages HuntBot, detects security threats, and provides a beautiful web dashboard for real-time monitoring and control.

Unlike basic automation scripts, NeuraSelf features **human-like typing simulation**, **multi-layer security detection**, **dynamic cooldown synchronization**, and a **comprehensive web interface** that puts you in complete control.

---

## ✨ Key Features

<table>
<tr>
<td width="50%">

### 🎯 **Intelligent Automation**

- ✅ Hunt, Battle, and OwO grinding
- ✅ HuntBot deployment & return tracking
- ✅ Daily rewards & cookie gifting
- ✅ Quest tracking & auto-checklist
- ✅ Level grinding with real quotes
- ✅ Auto-open crates & lootboxes
- ✅ Gem usage with tier priority

</td>
<td width="50%">

### 🛡️ **Advanced Security**

- ✅ Ban detection with instant pause
- ✅ Captcha detection & visual solver
- ✅ Desktop & webhook notifications
- ✅ Audio alerts for critical events
- ✅ Rate limit synchronization
- ✅ Security event logging
- ✅ Multi-layer protection system

</td>
</tr>
<tr>
<td width="50%">

### 🎭 **Stealth Technology**

- ✅ Human-like typing simulation
- ✅ Realistic typo generation
- ✅ Reaction time delays
- ✅ Channel rotation system
- ✅ Command spacing control
- ✅ Priority queue for manual commands
- ✅ Warmup period on startup

</td>
<td width="50%">

### 📊 **Web Dashboard**

- ✅ Real-time statistics & uptime
- ✅ Live configuration editor
- ✅ Captcha solving interface
- ✅ History analytics with charts
- ✅ System terminal with logs
- ✅ Remote bot control (pause/resume)
- ✅ Session tracking

</td>
</tr>
</table>

---

## 🚀 Quick Start

### Prerequisites

- **Python 3.10+** (Required)
- **Discord Account** (User token)
- **Windows/Linux/macOS** (Cross-platform)

### Installation

#### Option 1: Automated Setup (Windows)

```batch
# Run the setup script
neura_setup.bat
```

The setup script will:

1. ✅ Check and install Python 3.10
2. ✅ Install all required dependencies
3. ✅ Prompt for your Discord token
4. ✅ Configure channel settings
5. ✅ Launch the bot automatically

#### Option 2: Manual Setup

```bash
# Clone or download the repository
cd NeuraSelf-UwU

# Install dependencies
pip install -r requirements.txt

# Configure your settings
# Edit config/settings.json with your token and channels

# Run the bot
python main.py
```

---

## ⚙️ Configuration

NeuraSelf uses a JSON-based configuration system. Edit `config/settings.json` or use the **Dashboard Configuration** tab.

### Essential Settings

```json
{
  "accounts": [
    {
      "token": "YOUR_DISCORD_TOKEN",
      "channels": ["CHANNEL_ID_1", "CHANNEL_ID_2"],
      "enabled": true
    }
  ],
  "commands": {
    "hunt": { "enabled": true, "cooldown": [18, 20] },
    "battle": { "enabled": true, "cooldown": [18, 20] },
    "daily": { "enabled": true },
    "cookie": { "enabled": true, "userid": "USER_ID_TO_SEND_COOKIE" }
  },
  "stealth": {
    "typing": {
      "enabled": true,
      "min": 0.5,
      "max": 2.5,
      "typos": true,
      "mistake_rate": 0.1
    }
  }
}
```

📚 **For detailed configuration guide, see [guide.md](guide.md)**

---

## 📊 Dashboard Access

Once the bot is running, access the web dashboard at:

```
http://localhost:8000
```

### Dashboard Features

| Tab | Description |
|-----|-------------|
| **Dashboard** | Real-time stats, uptime, and bot status |
| **Configuration** | Edit all settings without restarting |
| **Security** | Solve captchas and view security logs |
| **History** | Analytics charts for cash and commands |
| **System Terminal** | Live log feed with color coding |

---

## 🎯 Feature Highlights

### 🤖 HuntBot Intelligence

NeuraSelf includes advanced HuntBot automation:

- **Auto-Deploy**: Sends HuntBot with configured cash amount
- **Return Detection**: Automatically detects when HuntBot returns
- **Cooldown Sync**: Syncs with HuntBot's return time (Days/Hours/Minutes)
- **Password Handling**: Detects password requirements and waits for reset
- **Captcha Detection**: Identifies HuntBot captchas with image extraction
- **Audio Alerts**: Plays distinct beep sounds for HuntBot events

### 🎭 Typing Simulation

Mimics human typing behavior:

- Character-by-character typing with random delays
- Realistic typo generation and correction
- Reaction time delays before responding
- Configurable typing speed and mistake rate

### 🛡️ Security System

Multi-layer protection:

- **Ban Detection**: Instant pause on ban message
- **Captcha Detection**: Keyword + button detection
- **Desktop Notifications**: System tray alerts
- **Webhook Integration**: Send alerts to Discord
- **Audio Alerts**: Different beeps for ban/captcha/huntbot

---

## 📈 Performance

| Metric | Value |
|--------|-------|
| Command Interval | 4.2s minimum |
| Priority Commands | 1.2s interval |
| Hunt/Battle Cooldown | 18-20s (configurable) |
| OwO Idle Frequency | 10-13s (configurable) |
| Channel Rotation | 300-350s (configurable) |
| Daily/Cookie Sync | 24h (auto-synced) |

---

## 🔧 Technology Stack

<div align="center">

| Component | Technology | Version |
|-----------|-----------|---------|
| **Discord Library** | discord.py-self | Latest |
| **Web Framework** | Flask | 2.3.0 |
| **HTTP Client** | aiohttp | 3.12.15 |
| **Console UI** | Rich | 14.2.0 |
| **Notifications** | plyer | 2.1.0 |
| **Audio** | playsound3 | 3.3.0 |
| **Environment** | python-dotenv | 1.2.1 |

</div>

---

## 📚 Documentation

- **[features.md](features.md)** - Complete feature matrix and comparison
- **[guide.md](guide.md)** - Comprehensive setup and usage guide
- **config/settings.json** - Configuration reference

---

## 🎨 Screenshots

### Terminal Interface

```
     ▄   ▄███▄     ▄   █▄▄▄▄ ██  
      █  █▀   ▀     █  █  ▄▀ █ █ 
  ██   █ ██▄▄    █   █ █▀▀▌  █▄▄█
  █ █  █ █▄   ▄▀ █   █ █  █  █  █
  █  █ █ ▀███▀   █▄ ▄█   █      █
  █   ██          ▀▀▀   ▀      █ 
                              ▀  
┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈
 N E U R A   S E L F  •  Made by ROUTO
┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈

[16:22:45] [SYS]      Ready as Username (Display: DisplayName)
[16:22:45] [INFO]     Channel: 123456789012345678
[16:22:46] [CMD]      Sent: hunt
[16:22:50] [SUCCESS]  Hunt successful!
```

---

## ⚠️ Disclaimer

This tool is for **educational purposes only**. Using self-bots violates Discord's Terms of Service and may result in account termination. Use at your own risk.

**NeuraSelf** is not affiliated with Discord or OwO bot. All trademarks belong to their respective owners.

---

## 🤝 Community & Support

<div align="center">

### Join our Discord community for support, updates, and discussions

<a href="https://discord.gg/mHU4bESA4p">
  <img src="https://invidget.switchblade.xyz/mHU4bESA4p" alt="Join Discord"/>
</a>

<br/>
<br/>

**Questions?** Check [guide.md](guide.md) or ask in our Discord server!

**Feature Requests?** See [features.md](features.md) for current capabilities!

</div>

 
---

<div align="center">

### 🧠 NeuraSelf

**Advanced OwO Automation** • Built by **ROUTO** • Made with ❤️

<br/>

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Discord](https://img.shields.io/badge/Discord-5865F2?style=for-the-badge&logo=discord&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)

<br/>

**Star ⭐ this project if you find it useful!**

</div>
