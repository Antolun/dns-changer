from PyQt6.QtCore import QThread, pyqtSignal
from dns_changer.core.dns_backend import NetworkManagerBackend

class SinglePingTask(QThread):
    """
    QThread to ping a single IP asynchronously.
    """
    result_signal = pyqtSignal(str, float) # ip, ms (or -1 if unreachable)

    def __init__(self, ip, parent=None):
        super().__init__(parent)
        self.ip = ip

    def run(self):
        ms = NetworkManagerBackend.ping_host(self.ip, count=1, timeout=1.5)
        self.result_signal.emit(self.ip, ms if ms is not None else -1.0)


class MultiPingWorker(QThread):
    """
    QThread to ping multiple DNS preset IPs concurrently and report results.
    """
    preset_ping_signal = pyqtSignal(str, float) # preset_id, ms
    finished_signal = pyqtSignal()

    def __init__(self, presets, parent=None):
        super().__init__(parent)
        self.presets = presets # list of dicts with 'id', 'primary', 'secondary'

    def run(self):
        for preset in self.presets:
            primary_ip = preset.get('primary')
            if not primary_ip:
                continue
            preset_id = preset['id']
            
            # Ping primary IP
            ms = NetworkManagerBackend.ping_host(primary_ip, count=1, timeout=1.5)
            if ms is not None:
                self.preset_ping_signal.emit(preset_id, ms)
            else:
                self.preset_ping_signal.emit(preset_id, -1.0)

        self.finished_signal.emit()
