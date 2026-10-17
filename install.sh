#!/bin/bash
# ============================================
#  ANONFACE - Auto Installer v1.2
#  Created by Mr.virus138 Team
#  The Anonymous Tanzania Hackers
#  Cooperation: Binno World Hacker
# ============================================

GREEN="\033[1;32m"; RED="\033[1;31m"; CYAN="\033[1;36m"; YELLOW="\033[1;33m"; RESET="\033[0m"

echo -e "${CYAN}[*] ANONFACE Installer - starting...${RESET}"

# --- Detect package manager ---
if command -v apt >/dev/null 2>&1; then
    PKG="apt"; SUDO="sudo"
elif command -v pkg >/dev/null 2>&1; then
    PKG="pkg"; SUDO=""
else
    echo -e "${RED}[-] Unsupported OS (need apt or pkg/Termux).${RESET}"
    exit 1
fi

echo -e "${YELLOW}[*] Installing system packages...${RESET}"
$SUDO $PKG update -y
$SUDO $PKG install -y exiftool steghide curl xdg-utils python3 python3-pip git

echo -e "${YELLOW}[*] Installing Python requirements...${RESET}"
pip3 install --upgrade pip
# PEP 668 fix for Kali/Ubuntu 23.04+
pip3 install -r requirements.txt --break-system-packages 2>/dev/null || pip3 install -r requirements.txt

echo -e "${YELLOW}[*] Installing Sherlock (from official repo)...${RESET}"
if [ ! -d "sherlock" ]; then
    git clone https://github.com/sherlock-project/sherlock.git
fi
cd sherlock && pip3 install -r requirements.txt --break-system-packages 2>/dev/null || pip3 install -r requirements.txt
cd ..

echo -e "${YELLOW}[*] Installing Maigret...${RESET}"
pip3 install maigret --break-system-packages 2>/dev/null || pip3 install maigret

echo -e "${YELLOW}[*] Making script executable...${RESET}"
chmod +x anonface.py

echo -e "${GREEN}[+] Installation complete!${RESET}"
echo -e "${GREEN}[+] Run the tool with:  python3 anonface.py${RESET}"
echo -e "${CYAN}    Created by Mr.virus138 Team | The Anonymous Tanzania Hackers${RESET}"
