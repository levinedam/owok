#!/bin/bash

set -e

GREEN="\e[1;32m"
RESET="\e[0m"

echo -e "${GREEN}==================== NEURA SELF SETUP ====================${RESET}"
echo ""

# detect OS
OS="$(uname)"
echo "Detected OS: $OS"
echo ""

# check for py 3.10
if command -v python3.10 >/dev/null 2>&1; then
    echo "Python 3.10 is already installed."
else
    echo "Python 3.10 not found. Installing..."

    if [ "$OS" = "Darwin" ]; then
        # macOS
        if ! command -v brew >/dev/null 2>&1; then
            echo "Homebrew not found. Please install Homebrew first:"
            echo "https://brew.sh/"
            exit 1
        fi

        brew update
        brew install python@3.10

    elif [ "$OS" = "Linux" ]; then
        # Linux
        if command -v apt >/dev/null 2>&1; then
            sudo apt update
            sudo apt install -y python3.10 python3.10-venv python3.10-distutils
        elif command -v pacman >/dev/null 2>&1; then
            sudo pacman -S --noconfirm python
        else
            echo "Unsupported Linux distribution. Install Python 3.10 manually."
            exit 1
        fi
    else
        echo "Unsupported OS."
        exit 1
    fi
fi

# ensure pip
echo ""
echo "Installing dependencies..."
python3.10 -m ensurepip --upgrade
python3.10 -m pip install --upgrade pip --quiet
python3.10 -m pip install -r requirements.txt --quiet

echo "Dependencies installed successfully."
echo ""


python3.10 config_helper.py

echo ""
echo "Setup complete! Starting Neura-Self..."
echo ""
python3.10 main.py
