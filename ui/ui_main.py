import ipaddress
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QScrollArea, QFrame, QGridLayout
)
from PyQt6.QtCore import Qt, pyqtSlot

from core.dns_backend import NetworkManagerBackend
from config.dns_presets import get_dns_presets
from config.i18n import LanguageManager
from ui.custom_widgets import WifiCardWidget, DnsPresetCardWidget, NotificationToast
from workers.ping_worker import MultiPingWorker
from ui.styles import STYLESHEET

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(1200, 680)
        self.setMinimumSize(880, 580)

        # Detect system language automatically (Default: English)
        LanguageManager.detect_and_set_system_language()

        self.wifi_connections = []
        self.wifi_card_widgets = []
        self.preset_card_widgets = []
        self.selected_wifi = None
        self.selected_preset = None
        self.ping_worker = None

        self._init_ui()
        self.apply_styles()
        self.retranslate_ui()
        self.load_wifi_networks()
        self.trigger_all_pings()

    def apply_styles(self):
        self.setStyleSheet(STYLESHEET)

    def _init_ui(self):
        main_central = QWidget(self)
        self.setCentralWidget(main_central)

        main_vbox = QVBoxLayout(main_central)
        main_vbox.setContentsMargins(0, 0, 0, 0)
        main_vbox.setSpacing(0)

        # -----------------------------
        # 1. Header Bar
        # -----------------------------
        header_frame = QFrame()
        header_frame.setObjectName("HeaderFrame")
        header_layout = QHBoxLayout(header_frame)
        header_layout.setContentsMargins(18, 10, 18, 10)

        # Title & Subtitle
        title_box = QVBoxLayout()
        title_box.setSpacing(2)

        self.title_lbl = QLabel()
        self.title_lbl.setObjectName("AppTitleLabel")
        title_box.addWidget(self.title_lbl)

        self.sub_lbl = QLabel()
        self.sub_lbl.setObjectName("AppSubtitleLabel")
        title_box.addWidget(self.sub_lbl)

        header_layout.addLayout(title_box)
        header_layout.addStretch()

        # Header Action Buttons (No manual language dropdown, auto-detected!)
        self.btn_refresh = QPushButton()
        self.btn_refresh.clicked.connect(self.load_wifi_networks)
        header_layout.addWidget(self.btn_refresh)

        self.btn_ping_all = QPushButton()
        self.btn_ping_all.clicked.connect(self.trigger_all_pings)
        header_layout.addWidget(self.btn_ping_all)

        self.btn_flush = QPushButton()
        self.btn_flush.clicked.connect(self.on_flush_cache)
        header_layout.addWidget(self.btn_flush)

        main_vbox.addWidget(header_frame)

        # -----------------------------
        # 2. Main Content Body
        # -----------------------------
        body_widget = QWidget()
        body_layout = QHBoxLayout(body_widget)
        body_layout.setContentsMargins(14, 14, 14, 14)
        body_layout.setSpacing(14)

        # --- LEFT SIDEBAR: Wi-Fi Networks ---
        sidebar_frame = QFrame()
        sidebar_frame.setObjectName("SidebarWidget")
        sidebar_frame.setFixedWidth(300)
        sidebar_layout = QVBoxLayout(sidebar_frame)
        sidebar_layout.setContentsMargins(12, 12, 12, 12)
        sidebar_layout.setSpacing(10)

        # Sidebar Header
        sidebar_title_box = QVBoxLayout()
        sidebar_title_box.setSpacing(2)

        self.s_title = QLabel()
        self.s_title.setProperty("class", "SectionTitle")
        sidebar_title_box.addWidget(self.s_title)

        self.s_desc = QLabel()
        self.s_desc.setProperty("class", "SectionSubtitle")
        sidebar_title_box.addWidget(self.s_desc)

        sidebar_layout.addLayout(sidebar_title_box)

        # Search Input Filter
        self.search_input = QLineEdit()
        self.search_input.textChanged.connect(self.filter_wifi_cards)
        sidebar_layout.addWidget(self.search_input)

        # Scroll Area for Wi-Fi Cards
        self.wifi_scroll = QScrollArea()
        self.wifi_scroll.setWidgetResizable(True)
        self.wifi_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        
        self.wifi_scroll_container = QWidget()
        self.wifi_scroll_layout = QVBoxLayout(self.wifi_scroll_container)
        self.wifi_scroll_layout.setContentsMargins(0, 0, 0, 0)
        self.wifi_scroll_layout.setSpacing(6)
        self.wifi_scroll_layout.addStretch()

        self.wifi_scroll.setWidget(self.wifi_scroll_container)
        sidebar_layout.addWidget(self.wifi_scroll, stretch=1)

        body_layout.addWidget(sidebar_frame)

        # --- RIGHT PANEL: DNS Configuration & Presets ---
        right_panel = QFrame()
        right_panel.setObjectName("MainContentWidget")
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(6, 0, 6, 0)
        right_layout.setSpacing(12)

        # Header Detail Card (Current Selected Network)
        self.detail_card = QFrame()
        self.detail_card.setObjectName("DetailCardHeader")
        detail_layout = QVBoxLayout(self.detail_card)
        detail_layout.setContentsMargins(14, 10, 14, 10)
        detail_layout.setSpacing(4)

        d_top = QHBoxLayout()
        d_top.setSpacing(8)

        self.selected_name_lbl = QLabel()
        self.selected_name_lbl.setStyleSheet("font-size: 15px; font-weight: 700; color: #E2E8F0;")
        d_top.addWidget(self.selected_name_lbl)

        self.selected_status_badge = QLabel()
        self.selected_status_badge.setProperty("class", "BadgeSaved")
        d_top.addWidget(self.selected_status_badge)

        d_top.addStretch()
        detail_layout.addLayout(d_top)

        self.current_dns_lbl = QLabel()
        self.current_dns_lbl.setStyleSheet("font-size: 11px; color: #60A5FA; font-weight: 600;")
        detail_layout.addWidget(self.current_dns_lbl)

        right_layout.addWidget(self.detail_card)

        # DNS Presets Grid Title
        preset_title_box = QHBoxLayout()
        self.preset_title_lbl = QLabel()
        self.preset_title_lbl.setProperty("class", "SectionTitle")
        preset_title_box.addWidget(self.preset_title_lbl)
        preset_title_box.addStretch()
        right_layout.addLayout(preset_title_box)

        # Presets Scroll Grid
        preset_scroll = QScrollArea()
        preset_scroll.setWidgetResizable(True)
        preset_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        
        preset_container = QWidget()
        self.preset_grid = QGridLayout(preset_container)
        self.preset_grid.setContentsMargins(0, 0, 0, 0)
        self.preset_grid.setSpacing(8)

        # Populate DNS Presets
        col_count = 2
        presets = get_dns_presets()
        for idx, preset in enumerate(presets):
            card = DnsPresetCardWidget(preset)
            card.preset_selected.connect(self.on_preset_selected)
            self.preset_card_widgets.append(card)
            row = idx // col_count
            col = idx % col_count
            self.preset_grid.addWidget(card, row, col)

        preset_scroll.setWidget(preset_container)
        right_layout.addWidget(preset_scroll, stretch=1)

        # Custom DNS Input Section (Visible when "Custom" is selected)
        self.custom_dns_group = QFrame()
        self.custom_dns_group.setStyleSheet("""
            background-color: #1C1F2B;
            border: 1px solid #272B3A;
            border-radius: 8px;
            padding: 10px 14px;
        """)
        custom_layout = QVBoxLayout(self.custom_dns_group)
        custom_layout.setContentsMargins(10, 8, 10, 8)
        custom_layout.setSpacing(6)

        self.c_title = QLabel()
        self.c_title.setStyleSheet("font-size: 12px; font-weight: 700; color: #60A5FA;")
        custom_layout.addWidget(self.c_title)

        inputs_layout = QHBoxLayout()
        inputs_layout.setSpacing(10)

        # Primary DNS Input
        p_box = QVBoxLayout()
        p_box.setSpacing(2)
        self.p_label = QLabel()
        self.p_label.setStyleSheet("font-size: 11px; color: #64748B;")
        self.custom_primary_input = QLineEdit()
        p_box.addWidget(self.p_label)
        p_box.addWidget(self.custom_primary_input)
        inputs_layout.addLayout(p_box)

        # Secondary DNS Input
        s_box = QVBoxLayout()
        s_box.setSpacing(2)
        self.s_label = QLabel()
        self.s_label.setStyleSheet("font-size: 11px; color: #64748B;")
        self.custom_secondary_input = QLineEdit()
        s_box.addWidget(self.s_label)
        s_box.addWidget(self.custom_secondary_input)
        inputs_layout.addLayout(s_box)

        custom_layout.addLayout(inputs_layout)
        right_layout.addWidget(self.custom_dns_group)
        self.custom_dns_group.hide()

        # Bottom Action Bar
        action_bar = QHBoxLayout()
        action_bar.setSpacing(10)

        self.btn_apply = QPushButton()
        self.btn_apply.setObjectName("PrimaryButton")
        self.btn_apply.setFixedHeight(38)
        self.btn_apply.clicked.connect(self.on_apply_dns)
        action_bar.addWidget(self.btn_apply, stretch=2)

        self.btn_reset_dhcp = QPushButton()
        self.btn_reset_dhcp.setObjectName("SecondaryButton")
        self.btn_reset_dhcp.setFixedHeight(38)
        self.btn_reset_dhcp.clicked.connect(self.on_reset_dhcp)
        action_bar.addWidget(self.btn_reset_dhcp, stretch=1)

        right_layout.addLayout(action_bar)
        body_layout.addWidget(right_panel, stretch=1)

        main_vbox.addWidget(body_widget, stretch=1)

        # Toast notification component
        self.toast = NotificationToast(self)

    def retranslate_ui(self):
        t = LanguageManager.t
        self.setWindowTitle(t("app_title"))
        self.title_lbl.setText(t("app_title"))
        self.sub_lbl.setText(t("app_subtitle"))

        self.btn_refresh.setText(t("refresh"))
        self.btn_ping_all.setText(t("ping_test"))
        self.btn_flush.setText(t("flush_cache"))

        self.s_title.setText(t("saved_networks"))
        self.s_desc.setText(t("select_network_subtitle"))
        self.search_input.setPlaceholderText(t("search_placeholder"))

        self.preset_title_lbl.setText(t("dns_options_title"))
        self.c_title.setText(t("custom_dns_section_title"))
        self.p_label.setText(t("primary_dns_label"))
        self.s_label.setText(t("secondary_dns_label"))
        self.custom_primary_input.setPlaceholderText(t("primary_placeholder"))
        self.custom_secondary_input.setPlaceholderText(t("secondary_placeholder"))

        self.btn_apply.setText(t("apply_dns_btn"))
        self.btn_reset_dhcp.setText(t("reset_dhcp_btn"))

        # Retranslate presets
        localized_presets = get_dns_presets()
        for idx, card in enumerate(self.preset_card_widgets):
            if idx < len(localized_presets):
                card.retranslate_preset(localized_presets[idx])

        # Retranslate Wi-Fi cards
        for card in self.wifi_card_widgets:
            if isinstance(card, WifiCardWidget):
                card.retranslate_ui()

        self.update_detail_card()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.toast.move(self.width() - self.toast.width() - 20, 60)

    def load_wifi_networks(self):
        self.wifi_connections = NetworkManagerBackend.get_saved_wifi_connections(only_secured=True)

        for card in self.wifi_card_widgets:
            card.deleteLater()
        self.wifi_card_widgets.clear()

        if not self.wifi_connections:
            empty_lbl = QLabel(LanguageManager.t("no_networks_found"))
            empty_lbl.setStyleSheet("color: #475569; font-size: 12px; padding: 10px;")
            self.wifi_scroll_layout.insertWidget(0, empty_lbl)
            self.wifi_card_widgets.append(empty_lbl)
            self.selected_wifi = None
            self.update_detail_card()
            return

        selected_still_exists = False
        for wifi_data in self.wifi_connections:
            card = WifiCardWidget(wifi_data)
            card.card_clicked.connect(self.on_wifi_selected)
            self.wifi_card_widgets.append(card)
            self.wifi_scroll_layout.insertWidget(self.wifi_scroll_layout.count() - 1, card)

            if self.selected_wifi and self.selected_wifi['uuid'] == wifi_data['uuid']:
                self.on_wifi_selected(wifi_data)
                selected_still_exists = True

        if not selected_still_exists and self.wifi_connections:
            self.on_wifi_selected(self.wifi_connections[0])

    def filter_wifi_cards(self, text):
        query = text.strip().lower()
        for card in self.wifi_card_widgets:
            if isinstance(card, WifiCardWidget):
                name = card.wifi_data['name'].lower()
                card.setVisible(query in name)

    def on_wifi_selected(self, wifi_data):
        self.selected_wifi = wifi_data

        for card in self.wifi_card_widgets:
            if isinstance(card, WifiCardWidget):
                card.set_selected(card.wifi_data['uuid'] == wifi_data['uuid'])

        self.update_detail_card()

    def update_detail_card(self):
        t = LanguageManager.t
        if not self.selected_wifi:
            self.selected_name_lbl.setText(t("select_a_network"))
            self.selected_status_badge.setText("--")
            self.current_dns_lbl.setText(t("current_dns_prefix") + "--")
            return

        self.selected_name_lbl.setText(self.selected_wifi['name'])

        if self.selected_wifi.get('is_active'):
            self.selected_status_badge.setText(t("status_connected"))
            self.selected_status_badge.setProperty("class", "BadgeActive")
        else:
            self.selected_status_badge.setText(t("status_saved"))
            self.selected_status_badge.setProperty("class", "BadgeSaved")

        self.selected_status_badge.style().unpolish(self.selected_status_badge)
        self.selected_status_badge.style().polish(self.selected_status_badge)

        dns_list = self.selected_wifi.get('dns_list', [])
        ignore_auto = self.selected_wifi.get('ignore_auto_dns', False)

        if dns_list and ignore_auto:
            self.current_dns_lbl.setText(f"{t('current_dns_prefix')}{', '.join(dns_list)} ({t('custom_label')})")
        else:
            self.current_dns_lbl.setText(f"{t('current_dns_prefix')}{t('dhcp_auto_label')}")

        presets = get_dns_presets()
        matched_preset = None
        if dns_list and ignore_auto:
            p_ip = dns_list[0] if len(dns_list) > 0 else ""
            s_ip = dns_list[1] if len(dns_list) > 1 else ""
            for preset in presets:
                if preset['primary'] == p_ip and (not preset['secondary'] or preset['secondary'] == s_ip):
                    matched_preset = preset
                    break

        if not matched_preset:
            if not ignore_auto or not dns_list:
                matched_preset = presets[0]
            else:
                matched_preset = presets[-1]
                if len(dns_list) > 0:
                    self.custom_primary_input.setText(dns_list[0])
                if len(dns_list) > 1:
                    self.custom_secondary_input.setText(dns_list[1])

        self.on_preset_selected(matched_preset)

    def on_preset_selected(self, preset_data):
        self.selected_preset = preset_data

        for card in self.preset_card_widgets:
            card.set_selected(card.preset_data['id'] == preset_data['id'])

        if preset_data['id'] == 'custom':
            self.custom_dns_group.show()
        else:
            self.custom_dns_group.hide()

    def trigger_all_pings(self):
        if self.ping_worker and self.ping_worker.isRunning():
            return

        presets = get_dns_presets()
        self.ping_worker = MultiPingWorker(presets)
        self.ping_worker.preset_ping_signal.connect(self.on_ping_result)
        self.ping_worker.start()

    @pyqtSlot(str, float)
    def on_ping_result(self, preset_id, ms):
        for card in self.preset_card_widgets:
            if card.preset_data['id'] == preset_id:
                card.set_ping_result(ms)

    def on_apply_dns(self):
        t = LanguageManager.t
        if not self.selected_wifi:
            self.toast.show_toast(t("toast_select_network_err"), "error")
            return

        if not self.selected_preset:
            self.toast.show_toast(t("toast_select_preset_err"), "error")
            return

        dns_servers = []
        preset_id = self.selected_preset['id']

        if preset_id == 'dhcp':
            dns_servers = []
        elif preset_id == 'custom':
            primary = self.custom_primary_input.text().strip()
            secondary = self.custom_secondary_input.text().strip()

            if not primary:
                self.toast.show_toast(t("toast_enter_primary_err"), "error")
                return

            if not self._is_valid_ipv4(primary):
                self.toast.show_toast(f"{t('toast_invalid_primary_err')} '{primary}'", "error")
                return

            dns_servers.append(primary)

            if secondary:
                if not self._is_valid_ipv4(secondary):
                    self.toast.show_toast(f"{t('toast_invalid_secondary_err')} '{secondary}'", "error")
                    return
                dns_servers.append(secondary)
        else:
            primary = self.selected_preset.get('primary')
            secondary = self.selected_preset.get('secondary')
            if primary:
                dns_servers.append(primary)
            if secondary:
                dns_servers.append(secondary)

        wifi_uuid = self.selected_wifi['uuid']
        is_active = self.selected_wifi.get('is_active', False)

        success, msg = NetworkManagerBackend.set_connection_dns(
            wifi_uuid, dns_servers, is_active=is_active
        )

        if success:
            dns_summary = ", ".join(dns_servers) if dns_servers else t("dhcp_auto_label")
            self.toast.show_toast(f"'{self.selected_wifi['name']}' {t('toast_dns_updated_success')} {dns_summary}", "success")
            self.load_wifi_networks()
        else:
            self.toast.show_toast(f"Error: {msg}", "error")

    def on_reset_dhcp(self):
        presets = get_dns_presets()
        dhcp_preset = presets[0]
        self.on_preset_selected(dhcp_preset)
        self.on_apply_dns()

    def on_flush_cache(self):
        t = LanguageManager.t
        ok = NetworkManagerBackend.flush_dns_cache()
        if ok:
            self.toast.show_toast(t("toast_cache_flushed_success"), "success")
        else:
            self.toast.show_toast(t("toast_cache_flushed_info"), "info")

    @staticmethod
    def _is_valid_ipv4(ip_str):
        try:
            ip = ipaddress.IPv4Address(ip_str.strip())
            return not ip.is_multicast and not ip.is_loopback
        except ValueError:
            return False
