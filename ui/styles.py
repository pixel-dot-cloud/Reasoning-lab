THEMES = {
    "Light": {
        "user_bubble_bg": "#dce0e8",
        "user_bubble_fg": "#4c4f69",
        "bot_bubble_bg": "#e6e9ef",
        "bot_bubble_fg": "#5c3d99",
        "qss": """
QWidget {
    background-color: #eff1f5;
    color: #4c4f69;
    font-family: 'Ubuntu', 'Segoe UI', sans-serif;
    font-size: 14px;
}
QPushButton {
    background-color: #ccd0da;
    border: 1px solid #bcc0cc;
    border-radius: 6px;
    padding: 8px 20px;
    color: #4c4f69;
    font-weight: bold;
}
QPushButton:hover { background-color: #bcc0cc; }
QPushButton:pressed { background-color: #acb0be; }
QPushButton:disabled { background-color: #dce0e8; color: #9ca0b0; }
QPushButton#sendBtn {
    background-color: #7287fd; color: #eff1f5; border: none; padding: 8px 24px;
}
QPushButton#sendBtn:hover { background-color: #8839ef; }
QPushButton#sendBtn:disabled { background-color: #ccd0da; color: #9ca0b0; }
QPushButton#stopBtn {
    background-color: #d20f39; color: #eff1f5; border: none; padding: 8px 24px;
}
QPushButton#stopBtn:hover { background-color: #e64553; }
QPushButton#stopBtn:disabled { background-color: #ccd0da; color: #9ca0b0; }
QTextEdit {
    background-color: #eff1f5; border: 1px solid #ccd0da;
    border-radius: 4px; padding: 6px; color: #4c4f69;
    selection-background-color: #bcc0cc;
}
QTextEdit#chatArea {
    background-color: #eff1f5; border: 1px solid #ccd0da;
    border-radius: 8px; padding: 10px; font-size: 14px;
}
QTextEdit#reasoningArea {
    background-color: #2a2b3d; border: 1px solid #45475a;
    border-radius: 6px; padding: 8px; color: #bac2de;
}
QLineEdit#chatInput {
    background-color: #eff1f5; border: 1px solid #bcc0cc;
    border-radius: 8px; padding: 10px 14px; color: #4c4f69; font-size: 14px;
}
QLineEdit#chatInput:focus { border-color: #7287fd; }
QComboBox {
    background-color: #eff1f5; border: 1px solid #ccd0da;
    border-radius: 4px; padding: 6px 10px; color: #4c4f69;
}
QComboBox::drop-down { border: none; width: 24px; }
QComboBox QAbstractItemView {
    background-color: #eff1f5; border: 1px solid #bcc0cc;
    color: #4c4f69; selection-background-color: #ccd0da;
}
QSpinBox {
    background-color: #eff1f5; border: 1px solid #ccd0da;
    border-radius: 4px; padding: 6px 10px; color: #4c4f69;
}
QCheckBox, QRadioButton { spacing: 8px; color: #4c4f69; }
QCheckBox::indicator, QRadioButton::indicator {
    width: 16px; height: 16px; border: 2px solid #bcc0cc; background-color: #eff1f5;
}
QCheckBox::indicator { border-radius: 3px; }
QRadioButton::indicator { border-radius: 10px; }
QCheckBox::indicator:checked, QRadioButton::indicator:checked {
    background-color: #7287fd; border-color: #7287fd;
}
QGroupBox {
    border: 1px solid #ccd0da; border-radius: 6px;
    margin-top: 10px; padding-top: 14px; font-weight: bold;
}
QGroupBox::title { subcontrol-origin: margin; left: 12px; padding: 0 6px; color: #7287fd; }
QListWidget {
    background-color: #eff1f5; border: 1px solid #ccd0da;
    border-radius: 4px; color: #4c4f69;
}
QListWidget::item { padding: 4px; }
QListWidget::item:hover { background-color: #ccd0da; }
QSplitter::handle { background-color: #bcc0cc; width: 3px; margin: 0 4px; border-radius: 1px; }
QSplitter::handle:hover { background-color: #7287fd; }
QLabel#statusLabel { color: #6c6f85; font-style: italic; padding: 2px 0; }
QLabel#modeLabel { color: #8c8fa1; font-size: 12px; }
QLabel#reasoningHeader { color: #7287fd; font-weight: bold; font-size: 13px; padding: 4px 0; }
QLabel#title { font-size: 36px; font-weight: bold; color: #7287fd; }
QLabel#subtitle { font-size: 16px; color: #6c6f85; }
QFrame#reasoningFrame { background-color: transparent; }
QFrame#chatsPanel { background-color: transparent; border-right: 1px solid #bcc0cc; }
""",
    },

    "Light Grey": {
        "user_bubble_bg": "#c0c4ce",
        "user_bubble_fg": "#3b3f51",
        "bot_bubble_bg": "#d1d5e0",
        "bot_bubble_fg": "#5c3d99",
        "qss": """
QWidget {
    background-color: #d8dce6;
    color: #3b3f51;
    font-family: 'Ubuntu', 'Segoe UI', sans-serif;
    font-size: 14px;
}
QPushButton {
    background-color: #b8bcca;
    border: 1px solid #a8acba;
    border-radius: 6px;
    padding: 8px 20px;
    color: #3b3f51;
    font-weight: bold;
}
QPushButton:hover { background-color: #a8acba; }
QPushButton:pressed { background-color: #989caa; }
QPushButton:disabled { background-color: #c8ccd6; color: #8a8e9e; }
QPushButton#sendBtn {
    background-color: #6c5ce7; color: #eff1f5; border: none; padding: 8px 24px;
}
QPushButton#sendBtn:hover { background-color: #5a4bd1; }
QPushButton#sendBtn:disabled { background-color: #b8bcca; color: #8a8e9e; }
QPushButton#stopBtn {
    background-color: #d63031; color: #eff1f5; border: none; padding: 8px 24px;
}
QPushButton#stopBtn:hover { background-color: #e04545; }
QPushButton#stopBtn:disabled { background-color: #b8bcca; color: #8a8e9e; }
QTextEdit {
    background-color: #c8ccd6; border: 1px solid #b8bcca;
    border-radius: 4px; padding: 6px; color: #3b3f51;
    selection-background-color: #a8acba;
}
QTextEdit#chatArea {
    background-color: #c8ccd6; border: 1px solid #b8bcca;
    border-radius: 8px; padding: 10px; font-size: 14px;
}
QTextEdit#reasoningArea {
    background-color: #282a36; border: 1px solid #44475a;
    border-radius: 6px; padding: 8px; color: #b8c0d8;
}
QLineEdit#chatInput {
    background-color: #c8ccd6; border: 1px solid #a8acba;
    border-radius: 8px; padding: 10px 14px; color: #3b3f51; font-size: 14px;
}
QLineEdit#chatInput:focus { border-color: #6c5ce7; }
QComboBox {
    background-color: #c8ccd6; border: 1px solid #b8bcca;
    border-radius: 4px; padding: 6px 10px; color: #3b3f51;
}
QComboBox::drop-down { border: none; width: 24px; }
QComboBox QAbstractItemView {
    background-color: #c8ccd6; border: 1px solid #a8acba;
    color: #3b3f51; selection-background-color: #b8bcca;
}
QSpinBox {
    background-color: #c8ccd6; border: 1px solid #b8bcca;
    border-radius: 4px; padding: 6px 10px; color: #3b3f51;
}
QCheckBox, QRadioButton { spacing: 8px; color: #3b3f51; }
QCheckBox::indicator, QRadioButton::indicator {
    width: 16px; height: 16px; border: 2px solid #a8acba; background-color: #c8ccd6;
}
QCheckBox::indicator { border-radius: 3px; }
QRadioButton::indicator { border-radius: 10px; }
QCheckBox::indicator:checked, QRadioButton::indicator:checked {
    background-color: #6c5ce7; border-color: #6c5ce7;
}
QGroupBox {
    border: 1px solid #b8bcca; border-radius: 6px;
    margin-top: 10px; padding-top: 14px; font-weight: bold;
}
QGroupBox::title { subcontrol-origin: margin; left: 12px; padding: 0 6px; color: #6c5ce7; }
QListWidget {
    background-color: #c8ccd6; border: 1px solid #b8bcca;
    border-radius: 4px; color: #3b3f51;
}
QListWidget::item { padding: 4px; }
QListWidget::item:hover { background-color: #b8bcca; }
QSplitter::handle { background-color: #a8acba; width: 3px; margin: 0 4px; border-radius: 1px; }
QSplitter::handle:hover { background-color: #6c5ce7; }
QLabel#statusLabel { color: #6a6e80; font-style: italic; padding: 2px 0; }
QLabel#modeLabel { color: #7a7e90; font-size: 12px; }
QLabel#reasoningHeader { color: #6c5ce7; font-weight: bold; font-size: 13px; padding: 4px 0; }
QLabel#title { font-size: 36px; font-weight: bold; color: #6c5ce7; }
QLabel#subtitle { font-size: 16px; color: #6a6e80; }
QFrame#reasoningFrame { background-color: transparent; }
QFrame#chatsPanel { background-color: transparent; border-right: 1px solid #a8acba; }
""",
    },

    "Dark": {
        "user_bubble_bg": "#45475a",
        "user_bubble_fg": "#cdd6f4",
        "bot_bubble_bg": "#313244",
        "bot_bubble_fg": "#a6e3a1",
        "qss": """
QWidget {
    background-color: #1e1e2e;
    color: #cdd6f4;
    font-family: 'Ubuntu', 'Segoe UI', sans-serif;
    font-size: 14px;
}
QPushButton {
    background-color: #45475a;
    border: 1px solid #585b70;
    border-radius: 6px;
    padding: 8px 20px;
    color: #cdd6f4;
    font-weight: bold;
}
QPushButton:hover { background-color: #585b70; }
QPushButton:pressed { background-color: #313244; }
QPushButton:disabled { background-color: #313244; color: #6c7086; }
QPushButton#sendBtn {
    background-color: #89b4fa; color: #1e1e2e; border: none; padding: 8px 24px;
}
QPushButton#sendBtn:hover { background-color: #8839ef; }
QPushButton#sendBtn:disabled { background-color: #45475a; color: #6c7086; }
QPushButton#stopBtn {
    background-color: #f38ba8; color: #1e1e2e; border: none; padding: 8px 24px;
}
QPushButton#stopBtn:hover { background-color: #eba0ac; }
QPushButton#stopBtn:disabled { background-color: #45475a; color: #6c7086; }
QTextEdit {
    background-color: #313244; border: 1px solid #45475a;
    border-radius: 4px; padding: 6px; color: #cdd6f4;
    selection-background-color: #585b70;
}
QTextEdit#chatArea {
    background-color: #181825; border: 1px solid #313244;
    border-radius: 8px; padding: 10px; font-size: 14px;
}
QTextEdit#reasoningArea {
    background-color: #11111b; border: 1px solid #313244;
    border-radius: 6px; padding: 8px; color: #a6adc8;
}
QLineEdit#chatInput {
    background-color: #313244; border: 1px solid #585b70;
    border-radius: 8px; padding: 10px 14px; color: #cdd6f4; font-size: 14px;
}
QLineEdit#chatInput:focus { border-color: #89b4fa; }
QComboBox {
    background-color: #313244; border: 1px solid #45475a;
    border-radius: 4px; padding: 6px 10px; color: #cdd6f4;
}
QComboBox::drop-down { border: none; width: 24px; }
QComboBox QAbstractItemView {
    background-color: #313244; border: 1px solid #585b70;
    color: #cdd6f4; selection-background-color: #45475a;
}
QSpinBox {
    background-color: #313244; border: 1px solid #45475a;
    border-radius: 4px; padding: 6px 10px; color: #cdd6f4;
}
QCheckBox, QRadioButton { spacing: 8px; color: #cdd6f4; }
QCheckBox::indicator, QRadioButton::indicator {
    width: 16px; height: 16px; border: 2px solid #585b70; background-color: #313244;
}
QCheckBox::indicator { border-radius: 3px; }
QRadioButton::indicator { border-radius: 10px; }
QCheckBox::indicator:checked, QRadioButton::indicator:checked {
    background-color: #89b4fa; border-color: #89b4fa;
}
QGroupBox {
    border: 1px solid #45475a; border-radius: 6px;
    margin-top: 10px; padding-top: 14px; font-weight: bold;
}
QGroupBox::title { subcontrol-origin: margin; left: 12px; padding: 0 6px; color: #89b4fa; }
QListWidget {
    background-color: #313244; border: 1px solid #45475a;
    border-radius: 4px; color: #cdd6f4;
}
QListWidget::item { padding: 4px; }
QListWidget::item:hover { background-color: #45475a; }
QSplitter::handle { background-color: #45475a; width: 3px; margin: 0 4px; border-radius: 1px; }
QSplitter::handle:hover { background-color: #89b4fa; }
QLabel#statusLabel { color: #a6adc8; font-style: italic; padding: 2px 0; }
QLabel#modeLabel { color: #6c7086; font-size: 12px; }
QLabel#reasoningHeader { color: #89b4fa; font-weight: bold; font-size: 13px; padding: 4px 0; }
QLabel#title { font-size: 36px; font-weight: bold; color: #89b4fa; }
QLabel#subtitle { font-size: 16px; color: #a6adc8; }
QFrame#reasoningFrame { background-color: transparent; }
QFrame#chatsPanel { background-color: transparent; border-right: 1px solid #45475a; }
""",
    },

    "Dark Grey": {
        "user_bubble_bg": "#4a4a5a",
        "user_bubble_fg": "#d4d4e0",
        "bot_bubble_bg": "#3a3a4a",
        "bot_bubble_fg": "#8be9fd",
        "qss": """
QWidget {
    background-color: #2c2c3a;
    color: #d4d4e0;
    font-family: 'Ubuntu', 'Segoe UI', sans-serif;
    font-size: 14px;
}
QPushButton {
    background-color: #4a4a5a;
    border: 1px solid #5a5a6a;
    border-radius: 6px;
    padding: 8px 20px;
    color: #d4d4e0;
    font-weight: bold;
}
QPushButton:hover { background-color: #5a5a6a; }
QPushButton:pressed { background-color: #3a3a4a; }
QPushButton:disabled { background-color: #3a3a4a; color: #6a6a7a; }
QPushButton#sendBtn {
    background-color: #7c6ff0; color: #e8e8f0; border: none; padding: 8px 24px;
}
QPushButton#sendBtn:hover { background-color: #6c5fd0; }
QPushButton#sendBtn:disabled { background-color: #4a4a5a; color: #6a6a7a; }
QPushButton#stopBtn {
    background-color: #e05565; color: #e8e8f0; border: none; padding: 8px 24px;
}
QPushButton#stopBtn:hover { background-color: #f06575; }
QPushButton#stopBtn:disabled { background-color: #4a4a5a; color: #6a6a7a; }
QTextEdit {
    background-color: #363646; border: 1px solid #4a4a5a;
    border-radius: 4px; padding: 6px; color: #d4d4e0;
    selection-background-color: #5a5a6a;
}
QTextEdit#chatArea {
    background-color: #242434; border: 1px solid #363646;
    border-radius: 8px; padding: 10px; font-size: 14px;
}
QTextEdit#reasoningArea {
    background-color: #1a1a28; border: 1px solid #363646;
    border-radius: 6px; padding: 8px; color: #9a9ab0;
}
QLineEdit#chatInput {
    background-color: #363646; border: 1px solid #5a5a6a;
    border-radius: 8px; padding: 10px 14px; color: #d4d4e0; font-size: 14px;
}
QLineEdit#chatInput:focus { border-color: #7c6ff0; }
QComboBox {
    background-color: #363646; border: 1px solid #4a4a5a;
    border-radius: 4px; padding: 6px 10px; color: #d4d4e0;
}
QComboBox::drop-down { border: none; width: 24px; }
QComboBox QAbstractItemView {
    background-color: #363646; border: 1px solid #5a5a6a;
    color: #d4d4e0; selection-background-color: #4a4a5a;
}
QSpinBox {
    background-color: #363646; border: 1px solid #4a4a5a;
    border-radius: 4px; padding: 6px 10px; color: #d4d4e0;
}
QCheckBox, QRadioButton { spacing: 8px; color: #d4d4e0; }
QCheckBox::indicator, QRadioButton::indicator {
    width: 16px; height: 16px; border: 2px solid #5a5a6a; background-color: #363646;
}
QCheckBox::indicator { border-radius: 3px; }
QRadioButton::indicator { border-radius: 10px; }
QCheckBox::indicator:checked, QRadioButton::indicator:checked {
    background-color: #7c6ff0; border-color: #7c6ff0;
}
QGroupBox {
    border: 1px solid #4a4a5a; border-radius: 6px;
    margin-top: 10px; padding-top: 14px; font-weight: bold;
}
QGroupBox::title { subcontrol-origin: margin; left: 12px; padding: 0 6px; color: #7c6ff0; }
QListWidget {
    background-color: #363646; border: 1px solid #4a4a5a;
    border-radius: 4px; color: #d4d4e0;
}
QListWidget::item { padding: 4px; }
QListWidget::item:hover { background-color: #4a4a5a; }
QSplitter::handle { background-color: #4a4a5a; width: 3px; margin: 0 4px; border-radius: 1px; }
QSplitter::handle:hover { background-color: #7c6ff0; }
QLabel#statusLabel { color: #8a8aa0; font-style: italic; padding: 2px 0; }
QLabel#modeLabel { color: #7a7a90; font-size: 12px; }
QLabel#reasoningHeader { color: #7c6ff0; font-weight: bold; font-size: 13px; padding: 4px 0; }
QLabel#title { font-size: 36px; font-weight: bold; color: #7c6ff0; }
QLabel#subtitle { font-size: 16px; color: #8a8aa0; }
QFrame#reasoningFrame { background-color: transparent; }
QFrame#chatsPanel { background-color: transparent; border-right: 1px solid #4a4a5a; }
""",
    },
}

THEME_NAMES = list(THEMES.keys())
DEFAULT_THEME = "Light Grey"


def get_theme(name):
    return THEMES.get(name, THEMES[DEFAULT_THEME])
