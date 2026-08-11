import subprocess
import re
import shutil

class NetworkManagerBackend:
    """
    Backend module to interact with NetworkManager via nmcli and resolvectl.
    """
    
    @staticmethod
    def is_nmcli_available():
        return shutil.which('nmcli') is not None

    @staticmethod
    def get_saved_wifi_connections(only_secured=True):
        """
        Retrieves saved Wi-Fi connections from NetworkManager.
        If only_secured=True, filters for networks with saved password security (wpa-psk, sae, wpa-eap, etc.).
        """
        if not NetworkManagerBackend.is_nmcli_available():
            return []

        # Get all connections
        cmd = ['nmcli', '-t', '-f', 'NAME,UUID,TYPE,DEVICE,STATE', 'connection', 'show']
        res = subprocess.run(cmd, capture_output=True, text=True, check=False)
        if res.returncode != 0:
            return []

        lines = res.stdout.strip().split('\n')
        connections = []

        for line in lines:
            if not line:
                continue
            parts = line.split(':')
            if len(parts) >= 3 and parts[2] == '802-11-wireless':
                name = parts[0]
                uuid = parts[1]
                device = parts[3] if len(parts) > 3 else ''
                state = parts[4] if len(parts) > 4 else ''
                is_active = (state == 'activated')

                # Check security key management
                sec_cmd = ['nmcli', '-g', '802-11-wireless-security.key-mgmt', 'connection', 'show', uuid]
                sec_res = subprocess.run(sec_cmd, capture_output=True, text=True, check=False)
                security = sec_res.stdout.strip()

                # Filter password-protected networks if requested
                is_secured = bool(security) and security.lower() not in ['none', '']

                if only_secured and not is_secured:
                    continue

                # Fetch current IPv4 DNS settings
                dns_cmd = ['nmcli', '-g', 'ipv4.dns', 'connection', 'show', uuid]
                dns_res = subprocess.run(dns_cmd, capture_output=True, text=True, check=False)
                dns_raw = dns_res.stdout.strip()
                
                # Format DNS string
                dns_list = []
                if dns_raw:
                    for raw_ip in dns_raw.replace(',', ' ').split():
                        ip_clean = raw_ip.split('#')[0].strip()
                        if ip_clean:
                            dns_list.append(ip_clean)

                ignore_auto_cmd = ['nmcli', '-g', 'ipv4.ignore-auto-dns', 'connection', 'show', uuid]
                ignore_res = subprocess.run(ignore_auto_cmd, capture_output=True, text=True, check=False)
                ignore_auto_dns = ignore_res.stdout.strip().lower() in ['yes', 'evet', '1', 'true']

                connections.append({
                    'name': name,
                    'uuid': uuid,
                    'device': device,
                    'is_active': is_active,
                    'security': security if security else 'Open',
                    'is_secured': is_secured,
                    'dns_list': dns_list,
                    'ignore_auto_dns': ignore_auto_dns
                })

        # Sort: Active connection first, then alphabetically by name
        connections.sort(key=lambda x: (not x['is_active'], x['name'].lower()))
        return connections

    @staticmethod
    def set_connection_dns(uuid_or_name, dns_servers, is_active=False):
        """
        Sets the IPv4 DNS servers for a given connection UUID or Name.
        """
        if not dns_servers:
            cmd = ['nmcli', 'connection', 'modify', uuid_or_name, 'ipv4.dns', '', 'ipv4.ignore-auto-dns', 'no']
        else:
            dns_str = " ".join(dns_servers)
            cmd = ['nmcli', 'connection', 'modify', uuid_or_name, 'ipv4.dns', dns_str, 'ipv4.ignore-auto-dns', 'yes']

        res = subprocess.run(cmd, capture_output=True, text=True, check=False)
        if res.returncode != 0:
            return False, res.stderr.strip() or "nmcli connection modify hatası."

        if is_active:
            up_cmd = ['nmcli', 'connection', 'up', uuid_or_name]
            up_res = subprocess.run(up_cmd, capture_output=True, text=True, check=False)
            if up_res.returncode != 0:
                return False, f"DNS değiştirildi fakat bağlantı yenilenemedi: {up_res.stderr.strip()}"

        NetworkManagerBackend.flush_dns_cache()
        return True, "DNS ayarları başarıyla uygulandı."

    @staticmethod
    def flush_dns_cache():
        methods = [
            ['resolvectl', 'flush-caches'],
            ['systemd-resolve', '--flush-caches'],
            ['nscd', '-i', 'hosts']
        ]
        for cmd in methods:
            if shutil.which(cmd[0]):
                res = subprocess.run(cmd, capture_output=True, text=True, check=False)
                if res.returncode == 0:
                    return True
        return False

    @staticmethod
    def ping_host(ip, count=1, timeout=1.5):
        try:
            cmd = ['ping', f'-c{count}', f'-W{int(timeout)}', ip]
            res = subprocess.run(cmd, capture_output=True, text=True, check=False)
            if res.returncode == 0:
                match = re.search(r'time=([\d.]+)\s*ms', res.stdout)
                if match:
                    return float(match.group(1))
                match_rtt = re.search(r'rtt min/avg/max/mdev = [\d.]+/([\d.]+)/', res.stdout)
                if match_rtt:
                    return float(match_rtt.group(1))
        except Exception:
            pass
        return None
