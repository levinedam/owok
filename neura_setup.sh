#!/bin/bash

clear
echo -e "\033[1;36mInitializing NeuraSelf-UwU Auto-Setup for Linux/Termux...\033[0m"
echo

if command -v python3.10 &>/dev/null; then
    PYTHON="python3.10"
elif command -v python3 &>/dev/null; then
    PYTHON="python3"
elif command -v python &>/dev/null; then
    PYTHON="python"
else
    echo -e "\033[1;31m[X] Python not found. Please install Python 3.10+ manually.\033[0m"
    exit 1
fi

echo -e "\033[1;32m[OK] Found Python: $($PYTHON --version)\033[0m"

echo -e "\033[1;34m[#] Upgrading pip...\033[0m"
$PYTHON -m pip install --upgrade pip --quiet

echo -e "\033[1;34m[#] Installing project requirements...\033[0m"
$PYTHON -m pip install -r requirements.txt --progress-bar on

if [ $? -ne 0 ]; then
    echo -e "\033[1;31m[X] Failed to install dependencies.\033[0m"
    exit 1
fi

echo -e "\033[1;32m[OK] Environment is ready.\033[0m"
echo
echo "======================================================="
echo "    SETUP COMPLETE! HOW WOULD YOU LIKE TO PROCEED?"
echo "======================================================="
echo
echo " [1] Configure Accounts Now"
echo " [2] Start NeuraSelf Directly"
echo " [3] Exit"
echo

read -p " Selection (1-3): " choice

case $choice in
    1) $PYTHON config_helper.py ;;
    2) $PYTHON neura.py ;;
    *) echo "Exiting. Run neura.py later to start." ; exit 0 ;;
esac
