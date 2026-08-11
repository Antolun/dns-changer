"""
LupuS System Theme Style Sheet for PyQt6 DNS Tool.
All colors are inherited from the host operating system's native Qt palette.
"""

STYLESHEET = """
/* ── Base & Background ── */
QMainWindow, QDialog, QWidget {
    font-family: 'Inter', 'Segoe UI', 'Ubuntu', sans-serif;
    background-color: #0F1117;
    color: #E2E8F0;
}

QLabel {
    background-color: transparent;
}

/* ── Sidebar ── */
#SidebarWidget {
    background-color: #161821;
    border-right: 1px solid #272B3A;
}

/* ── Header Bar ── */
#HeaderFrame {
    background-color: #161821;
    border-bottom: 1px solid #272B3A;
    padding: 10px 18px;
}

#AppTitleLabel {
    font-size: 17px;
    font-weight: 700;
    color: #60A5FA;
    letter-spacing: 0.3px;
}

#AppSubtitleLabel {
    font-size: 11px;
    color: #64748B;
}

/* ── Section Titles ── */
.SectionTitle {
    font-size: 13px;
    font-weight: 700;
    color: #E2E8F0;
}

.SectionSubtitle {
    font-size: 11px;
    color: #64748B;
}

/* ── Search Bar & Text Inputs ── */
QLineEdit {
    background-color: transparent;
    border: 1px solid #272B3A;
    border-radius: 6px;
    padding: 6px 10px;
    font-size: 12px;
    color: #E2E8F0;
}

QLineEdit:focus {
    border: 1px solid #60A5FA;
}

QLineEdit::placeholder {
    color: #475569;
}

/* ── Scroll Area & Scrollbars ── */
QScrollArea {
    border: none;
    background-color: transparent;
}

QScrollBar:horizontal {
    height: 0px;
}

QScrollBar:vertical {
    border: none;
    background: #0F1117;
    width: 6px;
    margin: 0px;
    border-radius: 3px;
}

QScrollBar::handle:vertical {
    background: #272B3A;
    min-height: 20px;
    border-radius: 3px;
}

QScrollBar::handle:vertical:hover {
    background: #60A5FA;
}

QScrollBar::add-line, QScrollBar::sub-line {
    height: 0px;
    width: 0px;
}

/* ── Buttons ── */
QPushButton {
    background-color: #1C1F2B;
    border: 1px solid #272B3A;
    border-radius: 6px;
    padding: 6px 14px;
    font-size: 12px;
    font-weight: 600;
    color: #E2E8F0;
}

QPushButton:hover {
    border-color: #60A5FA;
    background-color: #222637;
}

/* Primary Action Button */
QPushButton#PrimaryButton {
    background-color: #3B82F6;
    color: #FFFFFF;
    border: none;
    font-weight: 700;
}

QPushButton#PrimaryButton:hover {
    background-color: #60A5FA;
}

QPushButton#SecondaryButton {
    background-color: #1C1F2B;
    border: 1px solid #272B3A;
    color: #E2E8F0;
}

QPushButton#SecondaryButton:hover {
    border-color: #60A5FA;
    background-color: #222637;
}

/* ── Wi-Fi Item Cards ── */
#WifiCardFrame {
    background-color: #1C1F2B;
    border: 1px solid #272B3A;
    border-radius: 6px;
    padding: 6px 10px;
}

#WifiCardFrame:hover {
    border-color: #60A5FA;
    background-color: #222637;
}

#WifiCardFrame[selected="true"] {
    border: 1.5px solid #60A5FA;
    background-color: rgba(96, 165, 250, 0.08);
}

#WifiCardFrame[active="true"] {
    border-left: 3px solid #34D399;
}

/* ── Badges ── */
.BadgeActive {
    background-color: rgba(16, 185, 129, 0.15);
    color: #34D399;
    border: 1px solid rgba(16, 185, 129, 0.3);
    border-radius: 4px;
    padding: 1px 6px;
    font-size: 10px;
    font-weight: 600;
}

.BadgeSaved {
    background-color: rgba(100, 116, 139, 0.1);
    border: 1px solid #272B3A;
    color: #94A3B8;
    border-radius: 4px;
    padding: 1px 6px;
    font-size: 10px;
    font-weight: 500;
}

.BadgeSecurity {
    background-color: rgba(96, 165, 250, 0.1);
    color: #60A5FA;
    border-radius: 3px;
    padding: 1px 5px;
    font-size: 10px;
}

/* ── DNS Preset Cards ── */
#PresetCardFrame {
    background-color: #1C1F2B;
    border: 1px solid #272B3A;
    border-radius: 8px;
    padding: 10px;
}

#PresetCardFrame:hover {
    border-color: #60A5FA;
    background-color: #222637;
}

#PresetCardFrame[selected="true"] {
    border: 1.5px solid #60A5FA;
    background-color: rgba(96, 165, 250, 0.08);
}

/* ── Detail Card Header ── */
#DetailCardHeader {
    background-color: #1C1F2B;
    border: 1px solid #272B3A;
    border-radius: 8px;
    padding: 12px 16px;
}
"""
