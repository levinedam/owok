# NeuraSelf - Mobile Guide (Termux)

Run NeuraSelf on your Android phone using Termux.

## 📥 1. Installation

1. **Download Termux** from F-Droid (do NOT use the Play Store version, it is outdated).
    * [Download Link](https://f-droid.org/repo/com.termux_118.apk)

2. **Open Termux** and copy-paste these commands one by one:

    * **Update Termux:**

        ```bash
        pkg update -y && pkg upgrade -y
        ```

    * **Install Python & Git:**

        ```bash
        pkg install python git termux-api -y
        ```

        *(Type `y` and Enter if asked)*

    * **Download NeuraSelf:**

        ```bash
        git clone https://github.com/routo-loop/NeuraSelf-UwU
        cd NeuraSelf-UwU
        ```

        *(Replace the link above if you have your own private repo link, or just copy your files to a folder)*

    * **Install Requirements:**

        ```bash
        pip install -r requirements.txt
        ```

## 2. Starting the Bot

Every time you open Termux, just type:

```bash
cd NeuraSelf-UwU
python neura.py
```

## 3. Mobile Configuration

To enable vibrations and notifications on your phone, edit `config/settings.json`.

**Recommended Settings:**

```json
"mobile": {
    "enabled": true,
    "toast": {
        "enabled": true,
        "position": "middle",
        "bg_color": "black",
        "text_color": "white"
    },
    "vibrate": {
        "enabled": true,
        "time": 0.5
    },
    "tts": {
        "enabled": false
    }
}
```

**What this does:**

* **Toast:** Shows a small popup text at the bottom of your screen for events.
* **Vibrate:** Vibrates your phone when a Captcha or Ban is detected (Critical!).
