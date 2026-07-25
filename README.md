# LupuS DNS Changer

A DNS management tool for Linux NetworkManager-based systems, built with PyQt6.

## Features

- **Wi-Fi Network Management** — Lists all saved Wi-Fi profiles, filters them, and changes DNS settings for the selected network.
- **Built-in DNS Presets** — Popular DNS providers can be applied with a single click.
- **Custom DNS Support** — Manually enter any primary and secondary IPv4 addresses.
- **Live Ping Test** — Measures response times of all DNS servers simultaneously and displays results on each card.
- **DNS Cache Flush** — Runs `resolvectl flush-caches` with one click.
- **Multi-language** — Automatic Turkish / English interface based on system locale.
- **Dark Theme** — Entire interface is designed on a dark background.

## Supported DNS Providers

| Provider | Primary | Secondary |
|---|---|---|
| Google Public DNS | `8.8.8.8` | `8.8.4.4` |
| Cloudflare DNS | `1.1.1.1` | `1.0.0.1` |
| AdGuard DNS | `94.140.14.14` | `94.140.15.15` |
| Quad9 DNS | `9.9.9.9` | `149.112.112.112` |
| Cisco OpenDNS | `208.67.222.222` | `208.67.220.220` |
| CleanBrowsing Family | `185.228.168.168` | `185.228.169.168` |
| Level3 (Lumen) | `4.2.2.1` | `4.2.2.2` |
| Automatic (DHCP) | — | — |
| Custom | User defined | User defined |

## Requirements

- Python 3.10+
- PyQt6
- NetworkManager (`nmcli`)

## Installation

```bash
bash install.sh install
```

The application is installed to `~/.local/share/dns-changer` and added to PATH as `/usr/local/bin/dns-changer`.

## Uninstall

```bash
bash install.sh uninstall
```

## Reinstall

```bash
bash install.sh reinstall
```

## Usage

After installation, run from terminal:

```bash
dns-changer
```

Or directly from the source directory:

```bash
python3 dns-changer
```

> **Note:** The application requires root privileges to modify DNS settings. It automatically escalates via `pkexec`, `kdesu`, or `sudo` when launched.

## Project Structure

```
dns-changer/
├── dns-changer          # Main entry point
├── install.sh           # Install / uninstall script
├── config/
│   ├── dns_presets.py   # DNS provider definitions
│   ├── i18n.py          # Translation manager (TR/EN)
│   └── translations.ts  # Translation data
├── core/
│   └── dns_backend.py   # NetworkManager (nmcli) backend
├── ui/
│   ├── ui_main.py       # Main window
│   ├── custom_widgets.py # Wi-Fi & DNS cards, notification components
│   └── styles.py        # QSS style definitions
└── workers/
    └── ping_worker.py   # Background ping thread
```
