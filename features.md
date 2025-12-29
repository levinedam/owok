# NeuraSelf Feature Matrix

> A comprehensive breakdown of all automation, security, and utility features built into NeuraSelf.

---

## 🎯 Core Automation Features

| Feature | Status | Description | Configuration |
|---------|--------|-------------|---------------|
| **Hunt Automation** | ✅ Active | Automatically sends hunt commands at optimized intervals | `commands.hunt.enabled` |
| **Battle Automation** | ✅ Active | Automated battle commands with cooldown management | `commands.battle.enabled` |
| **OwO Idle** | ✅ Active | Sends periodic OwO commands to maintain activity | `commands.owo.enabled` |
| **Daily Rewards** | ✅ Active | Auto-claims daily rewards with 24h cooldown sync | `commands.daily.enabled` |
| **Cookie Gifting** | ✅ Active | Sends cookies to specified users on 24h timer | `commands.cookie.enabled` |
| **Curse Command** | ✅ Active | Automatically curses target users at intervals | `commands.curse.enabled` |
| **Quest Tracking** | ✅ Active | Monitors quest progress and auto-checks checklist | `commands.quest.enabled` |

---

## 🤖 HuntBot Intelligence

| Feature | Status | Description | Behavior |
|---------|--------|-------------|----------|
| **Auto-Deploy** | ✅ Active | Deploys HuntBot with configured cash amount | Sends `huntbot <amount>` every 15 minutes |
| **Return Detection** | ✅ Active | Detects when HuntBot returns with rewards | Logs rewards and resets timer |
| **Cooldown Sync** | ✅ Active | Syncs with HuntBot's return time (D/H/M format) | Adjusts check interval dynamically |
| **Password Handling** | ✅ Active | Detects password requirements and waits for reset | Pauses checks until password resets |
| **Captcha Detection** | ✅ Active | Identifies HuntBot captchas with image extraction | Triggers audio alert + dashboard notification |
| **Error Recovery** | ✅ Active | Handles wrong password attempts gracefully | Auto-adjusts retry timing |

---

## 🎰 Gambling & Economy

| Feature | Status | Type | Configuration |
|---------|--------|------|---------------|
| **Coinflip** | ⚙️ Optional | Automated coinflip betting | `commands.coinflip.enabled` |
| **Slot Machine** | ⚙️ Optional | Automated slots gambling | `commands.slots.enabled` |
| **Auto-Open Crates** | ✅ Active | Opens weapon crates when found | `auto_use.autoCrate` |
| **Auto-Open Lootboxes** | ✅ Active | Opens lootboxes automatically | `auto_use.autoLootbox` |
| **Gem Usage** | ✅ Active | Uses gems by tier and type priority | `auto_use.gems.enabled` |
| **Auto-Sell** | ✅ Active | Sells animals automatically | `auto_use.autosell.enabled` |

---

## 🛡️ Security & Detection

| Feature | Status | Detection Method | Response |
|---------|--------|------------------|----------|
| **Ban Detection** | ✅ Active | Keyword: "You have been banned" | Immediate bot pause + audio alert |
| **Captcha Detection** | ✅ Active | Keywords + "Verify" button detection | Pause bot + desktop notification |
| **Rate Limit Sync** | ✅ Active | Parses "slow down" messages | Auto-adjusts command cooldowns |
| **Security Logs** | ✅ Active | Tracks all security events | Stored in dashboard history |
| **Webhook Alerts** | ⚙️ Optional | Sends alerts to Discord webhook | Configurable via `security.webhook_url` |
| **Desktop Notifications** | ✅ Active | System tray notifications | Uses `plyer` library |
| **Audio Alerts** | ✅ Active | Plays beep sounds for critical events | Separate beeps for ban/captcha/huntbot |

---

## 🎭 Stealth & Anti-Detection

| Feature | Status | Description | Impact |
|---------|--------|-------------|--------|
| **Typing Simulation** | ✅ Active | Simulates human typing with delays | Randomized character-by-character typing |
| **Typo Generation** | ✅ Active | Introduces realistic typos and corrections | Configurable mistake rate |
| **Reaction Time** | ✅ Active | Adds human-like delay before responding | 0.8-2s random delay |
| **Channel Rotation** | ✅ Active | Switches between configured channels | Prevents single-channel pattern |
| **Command Spacing** | ✅ Active | Enforces minimum 4.2s between commands | Prevents spam detection |
| **Priority Queue** | ✅ Active | Manual commands use faster 1.2s interval | Responsive to user input |
| **Warmup Period** | ✅ Active | 10-second delay on startup | Prevents instant automation |

---

## 📊 Dashboard & Monitoring

| Feature | Status | Description | Access |
|---------|--------|-------------|--------|
| **Real-Time Stats** | ✅ Active | Live bot status, uptime, and command counts | `http://localhost:8000` |
| **Configuration Editor** | ✅ Active | Web-based settings modification | Dashboard → Configuration |
| **Security Panel** | ✅ Active | Captcha solving interface with image display | Dashboard → Security |
| **History Analytics** | ✅ Active | Charts for cash growth and command usage | Dashboard → History |
| **Live Terminal** | ✅ Active | Real-time log feed with color coding | Dashboard → System Terminal |
| **Bot Control** | ✅ Active | Pause/Resume/Send commands remotely | Dashboard → Control |
| **Session Tracking** | ✅ Active | Tracks sessions with timestamps | Stored in `utils/history_tracker.py` |

---

## ⚡ Automation Utilities

| Feature | Status | Description | Configuration |
|---------|--------|-------------|---------------|
| **Level Grinding** | ✅ Active | Sends quotes or OwO spam for XP | `automation.level_grind.enabled` |
| **Quote Fetching** | ✅ Active | Fetches real quotes from FavQs API | Uses `aiohttp` for async requests |
| **RPP Commands** | ✅ Active | Runs run/pup/piku commands periodically | `automation.rpp.enabled` |
| **Cooldown Manager** | ✅ Active | Tracks and syncs all command cooldowns | Centralized in `cogs/cooldown_manager.py` |
| **Response Handler** | ✅ Active | Parses OwO bot responses for triggers | Handles embeds, attachments, and text |

---

## 🔧 Advanced Configuration

| Feature | Status | Description | Benefit |
|---------|--------|-------------|---------|
| **Multi-Account Support** | ✅ Active | Supports multiple Discord accounts | Switch between accounts on startup |
| **Multi-Channel Support** | ✅ Active | Operates across multiple channels | Defined in `accounts.channels` array |
| **Dynamic Cooldowns** | ✅ Active | Adjusts based on OwO bot responses | Prevents rate limiting |
| **Persistent Stats** | ✅ Active | Saves daily/cookie timers to JSON | Survives bot restarts |
| **Modular Cog System** | ✅ Active | All features are separate modules | Easy to enable/disable features |
| **Auto-Reload Config** | ✅ Active | Dashboard changes apply without restart | Hot-reload configuration |

---

## 📈 Performance Metrics

| Metric | Value | Description |
|--------|-------|-------------|
| **Command Interval** | 4.2s | Minimum time between automated commands |
| **Priority Interval** | 1.2s | Time between manual/priority commands |
| **Hunt/Battle Cooldown** | 18-20s | Configurable range for grinding |
| **OwO Cooldown** | 10-13s | Idle command frequency |
| **Level Quote Interval** | 40-80s | Random interval for XP grinding |
| **Channel Switch Interval** | 300-350s | Stealth rotation timing |
| **Daily/Cookie Cooldown** | 24h | Synced with OwO bot responses |

---

## 🎨 User Experience

| Feature | Status | Description |
|---------|--------|-------------|
| **Rich Console Output** | ✅ Active | Color-coded logs with timestamps |
| **ASCII Art Banner** | ✅ Active | Custom "NEURA" ASCII art on startup |
| **Account Selector** | ✅ Active | Interactive account selection menu |
| **Progress Indicators** | ✅ Active | Real-time status updates in terminal |
| **Error Handling** | ✅ Active | Graceful error recovery with logging |
| **Setup Automation** | ✅ Active | `neura_setup.bat` for one-click install |

---

## 🔐 Safety Features

| Feature | Status | Description | Protection Level |
|---------|--------|-------------|------------------|
| **Throttle Protection** | ✅ Active | Prevents sending during rate limits | High |
| **Pause on Security Event** | ✅ Active | Stops all automation when captcha/ban detected | Critical |
| **Message Validation** | ✅ Active | Verifies messages are for the correct user | Medium |
| **Channel Verification** | ✅ Active | Only operates in configured channels | High |
| **Command Lock** | ✅ Active | Prevents concurrent command sending | High |
| **Warmup Protection** | ✅ Active | Delays automation on startup | Medium |

---

## 📦 Technology Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Discord Library** | discord.py-self | Self-bot functionality |
| **Web Framework** | Flask | Dashboard backend |
| **HTTP Client** | aiohttp | Async API requests |
| **Console UI** | Rich | Beautiful terminal output |
| **Notifications** | plyer | Desktop notifications |
| **Audio** | playsound3 | Alert sound playback |
| **Data Storage** | JSON | Configuration and stats |

---

## 🎯 Feature Comparison

### vs. Basic OwO Bots

| Feature | NeuraSelf | Basic Bots |
|---------|-----------|------------|
| HuntBot Automation | ✅ Full Support | ❌ None |
| Typing Simulation | ✅ Advanced | ❌ None |
| Security Detection | ✅ Multi-Layer | ⚠️ Basic |
| Dashboard | ✅ Full Web UI | ❌ None |
| Channel Rotation | ✅ Automatic | ❌ None |
| Cooldown Sync | ✅ Dynamic | ⚠️ Static |
| Captcha Handling | ✅ Visual Interface | ⚠️ Text Only |

---

## 🚀 Quick Feature Reference

**Want to enable a feature?** Edit `config/settings.json` or use the Dashboard Configuration tab.

**Need help?** Check `guide.md` for detailed setup instructions.

**Found a bug?** Check the System Terminal in the dashboard for error logs.

---

<div align="center">

**NeuraSelf** • Built by ROUTO • Made with ❤️ for the OwO community

</div>
