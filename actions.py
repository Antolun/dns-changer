#!/usr/bin/python3
from luppo.actionsapi import luppotools
from luppo.actionsapi import shelltools
import os

WorkDir = "."

def build():
    pass

def install():
    src_dir = os.environ.get("DNS_CHANGER_SRC_DIR", os.getcwd())

    icon_path = os.path.join(src_dir, "dns-changer.png")

    # Copy application main entry and package directory
    main_py = os.path.join(src_dir, "main.py")
    if not os.path.isfile(main_py):
        main_py = "main.py"
    if os.path.isfile(main_py):
        luppotools.insinto("/usr/share/dns-changer", main_py)

    dns_changer_dir = os.path.join(src_dir, "dns_changer")
    if not os.path.isdir(dns_changer_dir):
        dns_changer_dir = "dns_changer"
    if os.path.isdir(dns_changer_dir):
        luppotools.insinto("/usr/share/dns-changer", dns_changer_dir)
        luppotools.insinto("/usr/share/dns-changer", icon_path)

    # Launcher script (/usr/bin/dns-changer)
    launcher_path = os.path.join(src_dir, "dns-changer")
    if not os.path.isfile(launcher_path):
        launcher_path = "dns-changer"

    if not os.path.isfile(launcher_path):
        with open("dns-changer", "w") as f:
            f.write("#!/bin/bash\nexec python3 /usr/share/dns-changer/main.py \"$@\"\n")
        os.chmod("dns-changer", 0o755)
        launcher_path = "dns-changer"

    luppotools.dobin(launcher_path)

    # Desktop entry
    desktop_path = os.path.join(src_dir, "dns-changer.desktop")
    if not os.path.isfile(desktop_path):
        desktop_path = "dns-changer.desktop"
    if os.path.isfile(desktop_path):
        luppotools.insinto("/usr/share/applications", desktop_path)

    # App icon
    if not os.path.isfile(icon_path):
        icon_path = os.path.join("dns-changer.png")
    if os.path.isfile(icon_path):
        luppotools.insinto("/usr/share/icons/hicolor/128x128/apps", icon_path, "dns-changer.png")

    # Documentation & License
    readme_path = os.path.join(src_dir, "README.md")
    if not os.path.isfile(readme_path):
        readme_path = "README.md"
    if os.path.isfile(readme_path):
        luppotools.dodoc(readme_path)

    license_path = os.path.join(src_dir, "LICENSE")
    if not os.path.isfile(license_path):
        license_path = "LICENSE"
    if os.path.isfile(license_path):
        luppotools.dodoc(license_path)
