"""
Multi-language translation manager supporting Turkish (TR) and English (EN).
Defaults to English (EN) and automatically detects system locale.
Includes complete translations for all DNS services.
"""
import os
from PyQt6.QtCore import QLocale

TRANSLATIONS = {
    "tr": {
        # App UI Labels
        "app_title": "DNS Değiştirici",
        "app_subtitle": "Wi-Fi Ağları İçin DNS Yönetim Paneli",
        "refresh": "Yenile",
        "ping_test": "Ping Testi",
        "flush_cache": "Önbelleği Temizle",
        "saved_networks": "Kayıtlı Wi-Fi Ağları",
        "select_network_subtitle": "DNS değiştirmek istediğiniz ağı seçin",
        "search_placeholder": "Ağ ara...",
        "no_networks_found": "Kayıtlı Wi-Fi ağı bulunamadı.",
        "select_a_network": "Bir Wi-Fi Ağı Seçiniz",
        "status_connected": "Bağlı",
        "status_saved": "Kayıtlı Profil",
        "current_dns_prefix": "Mevcut DNS: ",
        "dhcp_auto_label": "Otomatik (DHCP / Servis Sağlayıcı)",
        "custom_label": "Özel",
        "dns_options_title": "DNS Sunucusu Seçenekleri",
        "custom_dns_section_title": "Özel (Custom) DNS Adresleri",
        "primary_dns_label": "Birincil DNS (IPv4):",
        "secondary_dns_label": "İkincil DNS (İsteğe Bağlı):",
        "primary_placeholder": "Örn: 1.1.1.1 veya 8.8.8.8",
        "secondary_placeholder": "Örn: 1.0.0.1 veya 8.8.4.4",
        "apply_dns_btn": "DNS Adresini Uygula",
        "reset_dhcp_btn": "Otomatik DNS'e Dön (DHCP)",
        "toast_select_network_err": "Lütfen önce bir Wi-Fi ağı seçin.",
        "toast_select_preset_err": "Lütfen bir DNS seçeneği belirleyin.",
        "toast_enter_primary_err": "Birincil DNS adresini giriniz.",
        "toast_invalid_primary_err": "Geçersiz Birincil IP Adresi:",
        "toast_invalid_secondary_err": "Geçersiz İkincil IP Adresi:",
        "toast_dns_updated_success": "DNS güncellendi:",
        "toast_cache_flushed_success": "DNS önbelleği (resolvectl) temizlendi.",
        "toast_cache_flushed_info": "DNS önbelleği temizlendi veya sistem servisleri yenilendi.",
        "timeout": "Zamanaşımı",
        "theme_system": "Sistem Teması",
        "theme_dark": "Koyu Mod",
        "theme_light": "Açık Mod",

        # DNS Presets Translations
        "preset_dhcp_name": "Otomatik (DHCP)",
        "preset_dhcp_provider": "Modem / Servis Sağlayıcı",
        "preset_dhcp_badge": "Varsayılan",
        "preset_dhcp_desc": "Varsayılan DNS ayarlarını kullanır. İSS veya modem tarafından atanan adresi dinler.",

        "preset_google_name": "Google Public DNS",
        "preset_google_provider": "Google LLC",
        "preset_google_badge": "Popüler",
        "preset_google_desc": "Dünya genelinde yüksek erişilebilirlik ve performans sunan varsayılan DNS servisi.",

        "preset_cloudflare_name": "Cloudflare DNS",
        "preset_cloudflare_provider": "Cloudflare Inc.",
        "preset_cloudflare_badge": "Hızlı",
        "preset_cloudflare_desc": "Gizlilik odaklı, kayıt tutmayan ve en düşük gecikme süresine sahip DNS.",

        "preset_adguard_name": "AdGuard DNS",
        "preset_adguard_provider": "AdGuard Software Ltd",
        "preset_adguard_badge": "Reklam Engelleyici",
        "preset_adguard_desc": "Reklamları, takipçileri ve bilinen kimlik avı sitelerini engeller.",

        "preset_quad9_name": "Quad9 DNS",
        "preset_quad9_provider": "Quad9 Foundation",
        "preset_quad9_badge": "Güvenlik",
        "preset_quad9_desc": "Kötü amaçlı yazılımları ve siber tehdit içeren alan adlarını otomatik engeller.",

        "preset_opendns_name": "Cisco OpenDNS",
        "preset_opendns_provider": "Cisco Systems",
        "preset_opendns_badge": "Kurumsal",
        "preset_opendns_desc": "Yüksek performanslı ve phishing koruması sunan kurumsal seviyede DNS.",

        "preset_cleanbrowsing_name": "CleanBrowsing Family",
        "preset_cleanbrowsing_provider": "CleanBrowsing",
        "preset_cleanbrowsing_badge": "Aile Koruması",
        "preset_cleanbrowsing_desc": "Yetişkin içerikli siteleri süzerek güvenli ve aile dostu gezinti sağlar.",

        "preset_level3_name": "Level3 (Lumen)",
        "preset_level3_provider": "Lumen Technologies",
        "preset_level3_badge": "Omurga",
        "preset_level3_desc": "Küresel omurga sağlayıcısı tarafından sunulan doğrudan erişimli DNS sunucuları.",

        "preset_custom_name": "Diğer (Özel DNS)",
        "preset_custom_provider": "Kullanıcı Tanımlı",
        "preset_custom_badge": "Özel",
        "preset_custom_desc": "Manuel gireceğiniz Birincil ve İkincil IPv4 DNS adreslerini kullanır."
    },
    "en": {
        # App UI Labels
        "app_title": "DNS Changer",
        "app_subtitle": "DNS Management Panel for Wi-Fi Networks",
        "refresh": "Refresh",
        "ping_test": "Ping Test",
        "flush_cache": "Flush Cache",
        "saved_networks": "Saved Wi-Fi Networks",
        "select_network_subtitle": "Select the network you want to configure",
        "search_placeholder": "Search network...",
        "no_networks_found": "No saved Wi-Fi networks found.",
        "select_a_network": "Select a Wi-Fi Network",
        "status_connected": "Connected",
        "status_saved": "Saved Profile",
        "current_dns_prefix": "Current DNS: ",
        "dhcp_auto_label": "Automatic (DHCP / Provider)",
        "custom_label": "Custom",
        "dns_options_title": "DNS Server Options",
        "custom_dns_section_title": "Custom DNS Addresses",
        "primary_dns_label": "Primary DNS (IPv4):",
        "secondary_dns_label": "Secondary DNS (Optional):",
        "primary_placeholder": "e.g.: 1.1.1.1 or 8.8.8.8",
        "secondary_placeholder": "e.g.: 1.0.0.1 or 8.8.4.4",
        "apply_dns_btn": "Apply DNS Address",
        "reset_dhcp_btn": "Reset to Automatic (DHCP)",
        "toast_select_network_err": "Please select a Wi-Fi network first.",
        "toast_select_preset_err": "Please select a DNS option.",
        "toast_enter_primary_err": "Please enter a Primary DNS address.",
        "toast_invalid_primary_err": "Invalid Primary IP Address:",
        "toast_invalid_secondary_err": "Invalid Secondary IP Address:",
        "toast_dns_updated_success": "DNS updated:",
        "toast_cache_flushed_success": "DNS cache (resolvectl) flushed.",
        "toast_cache_flushed_info": "DNS cache flushed or system services restarted.",
        "timeout": "Timeout",
        "theme_system": "System Theme",
        "theme_dark": "Dark Mode",
        "theme_light": "Light Mode",

        # DNS Presets Translations
        "preset_dhcp_name": "Automatic (DHCP)",
        "preset_dhcp_provider": "Router / ISP",
        "preset_dhcp_badge": "Default",
        "preset_dhcp_desc": "Uses default DNS settings assigned by your ISP or router.",

        "preset_google_name": "Google Public DNS",
        "preset_google_provider": "Google LLC",
        "preset_google_badge": "Popular",
        "preset_google_desc": "Popular default DNS service offering global high availability and reliable performance.",

        "preset_cloudflare_name": "Cloudflare DNS",
        "preset_cloudflare_provider": "Cloudflare Inc.",
        "preset_cloudflare_badge": "Ultra Fast",
        "preset_cloudflare_desc": "Privacy-focused, non-logging DNS provider with extremely low latency.",

        "preset_adguard_name": "AdGuard DNS",
        "preset_adguard_provider": "AdGuard Software Ltd",
        "preset_adguard_badge": "Ad Blocker",
        "preset_adguard_desc": "Blocks advertisements, online trackers, and known phishing websites.",

        "preset_quad9_name": "Quad9 DNS",
        "preset_quad9_provider": "Quad9 Foundation",
        "preset_quad9_badge": "Security",
        "preset_quad9_desc": "Automatically blocks malware, phishing, ransomware, and cyber threat domains.",

        "preset_opendns_name": "Cisco OpenDNS",
        "preset_opendns_provider": "Cisco Systems",
        "preset_opendns_badge": "Enterprise",
        "preset_opendns_desc": "High-performance enterprise-grade DNS with phishing and threat protection.",

        "preset_cleanbrowsing_name": "CleanBrowsing Family",
        "preset_cleanbrowsing_provider": "CleanBrowsing",
        "preset_cleanbrowsing_badge": "Family Filter",
        "preset_cleanbrowsing_desc": "Filters adult content and inappropriate material for safe family browsing.",

        "preset_level3_name": "Level3 (Lumen)",
        "preset_level3_provider": "Lumen Technologies",
        "preset_level3_badge": "Backbone",
        "preset_level3_desc": "Direct access DNS servers hosted by global tier-1 internet backbone provider.",

        "preset_custom_name": "Custom DNS",
        "preset_custom_provider": "User Defined",
        "preset_custom_badge": "Custom",
        "preset_custom_desc": "Uses Primary and Secondary IPv4 DNS addresses specified manually."
    }
}


class LanguageManager:
    """
    Language manager with auto system locale detection and English default fallback.
    """
    _current_lang = "en"

    @classmethod
    def detect_and_set_system_language(cls):
        try:
            sys_locale = QLocale.system().name().lower()
            if sys_locale.startswith("tr"):
                cls._current_lang = "tr"
                return "tr"
        except Exception:
            pass

        lang_env = (os.environ.get("LANG") or "").lower()
        if lang_env.startswith("tr"):
            cls._current_lang = "tr"
            return "tr"

        cls._current_lang = "en"
        return "en"

    @classmethod
    def get_lang(cls):
        return cls._current_lang

    @classmethod
    def set_lang(cls, lang_code):
        if lang_code in TRANSLATIONS:
            cls._current_lang = lang_code

    @classmethod
    def t(cls, key, default=""):
        lang_dict = TRANSLATIONS.get(cls._current_lang, TRANSLATIONS["en"])
        return lang_dict.get(key, default or key)
