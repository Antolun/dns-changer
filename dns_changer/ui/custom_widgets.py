from PyQt6.QtWidgets import (
    QFrame, QVBoxLayout, QHBoxLayout, QLabel, QWidget
)
from PyQt6.QtCore import Qt, pyqtSignal, QTimer
from PyQt6.QtGui import QCursor
from dns_changer.config.i18n import LanguageManager

class WifiCardWidget(QFrame):
    """
    Compact card widget representing a saved Wi-Fi connection in the sidebar.
    """
    card_clicked = pyqtSignal(dict)

    def __init__(self, wifi_data, parent=None):
        super().__init__(parent)
        self.wifi_data = wifi_data
        self.setObjectName("WifiCardFrame")
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.is_selected = False

        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 6, 8, 6)
        layout.setSpacing(4)

        # Top row: Wi-Fi Name + Active Badge
        top_row = QHBoxLayout()
        top_row.setContentsMargins(0, 0, 0, 0)
        top_row.setSpacing(6)

        self.title_label = QLabel(self.wifi_data['name'])
        self.title_label.setStyleSheet("font-size: 12px; font-weight: 700; color: #E2E8F0;")
        top_row.addWidget(self.title_label, stretch=1)

        # Active or Saved status badge
        if self.wifi_data.get('is_active'):
            self.status_badge = QLabel(LanguageManager.t("status_connected"))
            self.status_badge.setProperty("class", "BadgeActive")
        else:
            self.status_badge = QLabel(LanguageManager.t("status_saved"))
            self.status_badge.setProperty("class", "BadgeSaved")
        top_row.addWidget(self.status_badge)

        layout.addLayout(top_row)

        # Bottom row: Security info + Current DNS summary
        bottom_row = QHBoxLayout()
        bottom_row.setContentsMargins(0, 0, 0, 0)
        bottom_row.setSpacing(6)

        sec_type = self.wifi_data.get('security', 'WPA/WPA2')
        if sec_type == 'wpa-psk':
            sec_text = "WPA2/WPA3"
        elif sec_type == 'sae':
            sec_text = "WPA3"
        elif sec_type == 'wpa-eap':
            sec_text = "WPA Enterprise"
        elif sec_type:
            sec_text = sec_type
        else:
            sec_text = "Open"

        sec_label = QLabel(sec_text)
        sec_label.setProperty("class", "BadgeSecurity")
        bottom_row.addWidget(sec_label)

        bottom_row.addStretch()

        # DNS Summary
        dns_list = self.wifi_data.get('dns_list', [])
        ignore_auto = self.wifi_data.get('ignore_auto_dns', False)
        if dns_list and ignore_auto:
            dns_text = f"DNS: {dns_list[0]}"
        else:
            dns_text = f"DNS: {LanguageManager.t('custom_label') if ignore_auto else 'DHCP'}"

        self.dns_label = QLabel(dns_text)
        self.dns_label.setStyleSheet("font-size: 10px; color: #64748B;")
        bottom_row.addWidget(self.dns_label)

        layout.addLayout(bottom_row)

    def retranslate_ui(self):
        if self.wifi_data.get('is_active'):
            self.status_badge.setText(LanguageManager.t("status_connected"))
        else:
            self.status_badge.setText(LanguageManager.t("status_saved"))

    def set_selected(self, selected):
        self.is_selected = selected
        self.setProperty("selected", "true" if selected else "false")
        self.setProperty("active", "true" if self.wifi_data.get('is_active') else "false")
        self.style().unpolish(self)
        self.style().polish(self)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.card_clicked.emit(self.wifi_data)
        super().mousePressEvent(event)


class DnsPresetCardWidget(QFrame):
    """
    Clean clickable card widget representing a DNS provider preset.
    """
    preset_selected = pyqtSignal(dict)

    def __init__(self, preset_data, parent=None):
        super().__init__(parent)
        self.preset_data = preset_data
        self.setObjectName("PresetCardFrame")
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.is_selected = False

        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 10, 12, 10)
        layout.setSpacing(6)

        # Header Row: Name + Badge + Ping
        header_row = QHBoxLayout()
        header_row.setContentsMargins(0, 0, 0, 0)
        header_row.setSpacing(6)

        # Title
        self.name_lbl = QLabel(self.preset_data['name'])
        self.name_lbl.setStyleSheet("font-size: 13px; font-weight: 700; color: #E2E8F0;")
        header_row.addWidget(self.name_lbl)

        # Badge
        badge_text = self.preset_data.get('badge', '')
        if badge_text:
            self.badge_lbl = QLabel(badge_text)
            color = self.preset_data.get('color', '#06B6D4')
            self.badge_lbl.setStyleSheet(f"""
                background-color: rgba({int(color[1:3], 16)}, {int(color[3:5], 16)}, {int(color[5:7], 16)}, 0.15);
                color: {color};
                border: 1px solid rgba({int(color[1:3], 16)}, {int(color[3:5], 16)}, {int(color[5:7], 16)}, 0.3);
                border-radius: 4px;
                padding: 1px 5px;
                font-size: 10px;
                font-weight: 600;
            """)
            header_row.addWidget(self.badge_lbl)

        header_row.addStretch()

        # Ping badge label
        self.ping_lbl = QLabel("--")
        self.ping_lbl.setProperty("class", "PingBadgeOffline")
        header_row.addWidget(self.ping_lbl)

        layout.addLayout(header_row)

        # IPs Row
        ip_row = QHBoxLayout()
        ip_row.setContentsMargins(0, 0, 0, 0)
        ip_row.setSpacing(8)

        p_ip = self.preset_data.get('primary')
        s_ip = self.preset_data.get('secondary')

        if p_ip:
            ip_str = f"<b>{p_ip}</b>"
            if s_ip:
                ip_str += f" &nbsp;|&nbsp; <b>{s_ip}</b>"
        else:
            ip_str = LanguageManager.t("dhcp_auto_label")

        self.ip_lbl = QLabel(ip_str)
        self.ip_lbl.setStyleSheet("font-size: 11px; color: #60A5FA;")
        ip_row.addWidget(self.ip_lbl)
        ip_row.addStretch()

        layout.addLayout(ip_row)

        # Description
        self.desc_lbl = QLabel(self.preset_data.get('desc', ''))
        self.desc_lbl.setWordWrap(True)
        self.desc_lbl.setStyleSheet("font-size: 11px; color: #64748B; line-height: 1.2;")
        layout.addWidget(self.desc_lbl)

    def retranslate_preset(self, preset_data):
        self.preset_data = preset_data
        self.name_lbl.setText(preset_data['name'])
        if hasattr(self, 'badge_lbl'):
            self.badge_lbl.setText(preset_data.get('badge', ''))
        self.desc_lbl.setText(preset_data.get('desc', ''))
        p_ip = preset_data.get('primary')
        s_ip = preset_data.get('secondary')
        if p_ip:
            ip_str = f"<b>{p_ip}</b>"
            if s_ip:
                ip_str += f" &nbsp;|&nbsp; <b>{s_ip}</b>"
        else:
            ip_str = LanguageManager.t("dhcp_auto_label")
        self.ip_lbl.setText(ip_str)

    def set_ping_result(self, ms):
        if ms < 0:
            self.ping_lbl.setText(LanguageManager.t("timeout"))
            self.ping_lbl.setProperty("class", "PingBadgeOffline")
        else:
            self.ping_lbl.setText(f"{int(ms)} ms")
            if ms < 40:
                self.ping_lbl.setProperty("class", "PingBadge")
            else:
                self.ping_lbl.setProperty("class", "PingBadgeSlow")
        self.ping_lbl.style().unpolish(self.ping_lbl)
        self.ping_lbl.style().polish(self.ping_lbl)

    def set_selected(self, selected):
        self.is_selected = selected
        self.setProperty("selected", "true" if selected else "false")
        self.style().unpolish(self)
        self.style().polish(self)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.preset_selected.emit(self.preset_data)
        super().mousePressEvent(event)


class NotificationToast(QFrame):
    """
    Clean notification alert widget.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.hide()
        self.setFixedWidth(340)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 8, 12, 8)
        layout.setSpacing(8)

        self.msg_lbl = QLabel("")
        self.msg_lbl.setWordWrap(True)
        self.msg_lbl.setStyleSheet("font-size: 12px; font-weight: 600; color: #FFFFFF;")
        layout.addWidget(self.msg_lbl, stretch=1)

        self.timer = QTimer(self)
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.hide)

    def show_toast(self, message, toast_type="success", duration_ms=3500):
        self.msg_lbl.setText(message)
        if toast_type == "success":
            self.setStyleSheet("""
                background-color: #065F46;
                border: 1px solid #10B981;
                border-radius: 6px;
            """)
        elif toast_type == "error":
            self.setStyleSheet("""
                background-color: #991B1B;
                border: 1px solid #EF4444;
                border-radius: 6px;
            """)
        else:
            self.setStyleSheet("""
                background-color: #1E293B;
                border: 1px solid #334155;
                border-radius: 6px;
            """)

        self.show()
        self.raise_()
        self.timer.start(duration_ms)
