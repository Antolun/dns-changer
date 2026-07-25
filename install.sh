#!/usr/bin/env bash

# DNS Changer KDE Plasma Desktop Installer & Uninstaller
# Installs application to ~/.local/share/dns-changer

# Colors for modern terminal output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Directories
SOURCE_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
if [ -n "$SUDO_USER" ]; then
    REAL_HOME=$(getent passwd "$SUDO_USER" | cut -d: -f6)
else
    REAL_HOME="$HOME"
fi
INSTALL_DIR="$REAL_HOME/.local/share/dns-changer"

# Show usage help
show_usage() {
    echo -e "Usage: $0 [OPTION]"
    echo -e "Options:"
    echo -e "  install     Installs the application to '$INSTALL_DIR' and integrates with menu (Default)"
    echo -e "  uninstall   Completely uninstalls the application and menu entries"
    echo -e "  reinstall   Completely reinstalls the application and menu entries"
    echo -e "  help        Shows this help message"
}

# Perform installation
install_app() {
    echo -e "${CYAN}====================================================${NC}"
    echo -e "${CYAN}        DNS Changer KDE Desktop Installation Wizard    ${NC}"
    echo -e "${CYAN}====================================================${NC}"

    # 1. Dependency checks
    echo -e "${BLUE}[1/5] Checking requirements...${NC}"
    if python3 -c "import PyQt6" &> /dev/null; then
        echo -e "${GREEN}✓ PyQt6 library is installed.${NC}"
    else
        echo -e "${RED}✗ Error: PyQt6 not found. Please install it first: pip install PyQt6${NC}"
        exit 1
    fi

    # 2. Create target directories
    echo -e "${BLUE}[2/5] Creating installation directories...${NC}"
    echo -e "Target Directory: $INSTALL_DIR"
    mkdir -p "$INSTALL_DIR"
    mkdir -p "$INSTALL_DIR/workers"
    mkdir -p "$INSTALL_DIR/ui"
    mkdir -p "$INSTALL_DIR/core"
    mkdir -p "$INSTALL_DIR/config"
    echo -e "${GREEN}✓ Directories created.${NC}"

    # 3. Copy application files
    echo -e "${BLUE}[3/5] Copying application files...${NC}"
    
    # Copy main code files
    cp "$SOURCE_DIR/dns-changer" "$INSTALL_DIR/"
    cp "$SOURCE_DIR/workers/__init__.py" "$INSTALL_DIR/workers/"
    cp "$SOURCE_DIR/workers/ping_worker.py" "$INSTALL_DIR/workers/"
    cp "$SOURCE_DIR/ui/__init__.py" "$INSTALL_DIR/ui/"
    cp "$SOURCE_DIR/ui/custom_widgets.py" "$INSTALL_DIR/ui/"
    cp "$SOURCE_DIR/ui/ui_main.py" "$INSTALL_DIR/ui/"
    cp "$SOURCE_DIR/ui/styles.py" "$INSTALL_DIR/ui/"
    cp "$SOURCE_DIR/core/__init__.py" "$INSTALL_DIR/core/"
    cp "$SOURCE_DIR/core/dns_backend.py" "$INSTALL_DIR/core/"
    cp "$SOURCE_DIR/config/__init__.py" "$INSTALL_DIR/config/"
    cp "$SOURCE_DIR/config/dns_presets.py" "$INSTALL_DIR/config/"
    cp "$SOURCE_DIR/config/i18n.py" "$INSTALL_DIR/config/"
    cp "$SOURCE_DIR/config/translations.ts" "$INSTALL_DIR/config/"

    sudo cp "$SOURCE_DIR/dns-changer" "/usr/local/bin/"
    chmod +x "/usr/local/bin/dns-changer"

    echo -e "${CYAN}====================================================${NC}"
    echo -e "${GREEN}🎉 DNS Changer successfully installed to '$INSTALL_DIR'!${NC}"
    echo -e "${CYAN}====================================================${NC}"
}

# Perform uninstallation
uninstall_app() {
    # Remove binary from /usr/local/bin
    if [ -f "/usr/local/bin/dns-changer" ]; then
        echo -e "${BLUE}[1/3] Removing binary from /usr/local/bin...${NC}"
        sudo rm -f "/usr/local/bin/dns-changer"
    fi

    # 2. Remove installation folder
    if [ -d "$INSTALL_DIR" ]; then
        echo -e "${BLUE}[2/3] Cleaning up installation folder...${NC}"
        echo -e "Removing directory: $INSTALL_DIR"
        
        rm -rf "$INSTALL_DIR"
        echo -e "${GREEN}✓ Application files and directory successfully removed.${NC}"
    else
        echo -e "${YELLOW}! Info: Installation directory ($INSTALL_DIR) not found.${NC}"
    fi

    echo -e "${YELLOW}====================================================${NC}"
    echo -e "${GREEN}✓ DNS Changer has been completely removed from your system!${NC}"
    echo -e "${YELLOW}====================================================${NC}"
}

# Parse command line options
ACTION="install"

while [[ "$#" -gt 0 ]]; do
    case $1 in
        install) ACTION="install"; shift ;;
        uninstall) ACTION="uninstall"; shift ;;
        reinstall) ACTION="reinstall"; shift ;;
        help) show_usage; exit 0 ;;
        *) echo -e "${RED}Invalid option: $1${NC}"; show_usage; exit 1 ;;
    esac
done

if [ "$ACTION" == "install" ]; then
    install_app
elif [ "$ACTION" == "uninstall" ]; then
    uninstall_app
elif [ "$ACTION" == "reinstall" ]; then
    uninstall_app
    install_app
fi
