"""
Predefined DNS server configurations with complete i18n support.
"""
from dns_changer.config.i18n import LanguageManager

RAW_DNS_PRESETS = [
    {
        "id": "dhcp",
        "name_key": "preset_dhcp_name",
        "provider_key": "preset_dhcp_provider",
        "desc_key": "preset_dhcp_desc",
        "badge_key": "preset_dhcp_badge",
        "primary": "",
        "secondary": "",
        "color": "#64748B"
    },
    {
        "id": "google",
        "name_key": "preset_google_name",
        "provider_key": "preset_google_provider",
        "desc_key": "preset_google_desc",
        "badge_key": "preset_google_badge",
        "primary": "8.8.8.8",
        "secondary": "8.8.4.4",
        "color": "#3B82F6"
    },
    {
        "id": "cloudflare",
        "name_key": "preset_cloudflare_name",
        "provider_key": "preset_cloudflare_provider",
        "desc_key": "preset_cloudflare_desc",
        "badge_key": "preset_cloudflare_badge",
        "primary": "1.1.1.1",
        "secondary": "1.0.0.1",
        "color": "#F97316"
    },
    {
        "id": "adguard",
        "name_key": "preset_adguard_name",
        "provider_key": "preset_adguard_provider",
        "desc_key": "preset_adguard_desc",
        "badge_key": "preset_adguard_badge",
        "primary": "94.140.14.14",
        "secondary": "94.140.15.15",
        "color": "#10B981"
    },
    {
        "id": "quad9",
        "name_key": "preset_quad9_name",
        "provider_key": "preset_quad9_provider",
        "desc_key": "preset_quad9_desc",
        "badge_key": "preset_quad9_badge",
        "primary": "9.9.9.9",
        "secondary": "149.112.112.112",
        "color": "#8B5CF6"
    },
    {
        "id": "opendns",
        "name_key": "preset_opendns_name",
        "provider_key": "preset_opendns_provider",
        "desc_key": "preset_opendns_desc",
        "badge_key": "preset_opendns_badge",
        "primary": "208.67.222.222",
        "secondary": "208.67.220.220",
        "color": "#06B6D4"
    },
    {
        "id": "cleanbrowsing",
        "name_key": "preset_cleanbrowsing_name",
        "provider_key": "preset_cleanbrowsing_provider",
        "desc_key": "preset_cleanbrowsing_desc",
        "badge_key": "preset_cleanbrowsing_badge",
        "primary": "185.228.168.168",
        "secondary": "185.228.169.168",
        "color": "#EC4899"
    },
    {
        "id": "level3",
        "name_key": "preset_level3_name",
        "provider_key": "preset_level3_provider",
        "desc_key": "preset_level3_desc",
        "badge_key": "preset_level3_badge",
        "primary": "4.2.2.1",
        "secondary": "4.2.2.2",
        "color": "#6366F1"
    },
    {
        "id": "custom",
        "name_key": "preset_custom_name",
        "provider_key": "preset_custom_provider",
        "desc_key": "preset_custom_desc",
        "badge_key": "preset_custom_badge",
        "primary": "",
        "secondary": "",
        "color": "#F59E0B"
    }
]

def get_dns_presets():
    """
    Returns localized list of DNS presets based on current language.
    """
    presets = []
    for raw in RAW_DNS_PRESETS:
        presets.append({
            "id": raw["id"],
            "name": LanguageManager.t(raw["name_key"]),
            "provider": LanguageManager.t(raw["provider_key"]),
            "desc": LanguageManager.t(raw["desc_key"]),
            "badge": LanguageManager.t(raw["badge_key"]),
            "primary": raw["primary"],
            "secondary": raw["secondary"],
            "color": raw["color"]
        })
    return presets
