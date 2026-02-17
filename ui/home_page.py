from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QComboBox
from PySide6.QtCore import Qt
from ui.styles import THEME_NAMES, DEFAULT_THEME


class HomePage(QWidget):
    def __init__(self, stack):
        super().__init__()
        self.stack = stack

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        title = QLabel("Reasoning Lab")
        title.setObjectName("title")
        title.setAlignment(Qt.AlignCenter)

        subtitle = QLabel("Multi-Model Reasoning Pipeline")
        subtitle.setObjectName("subtitle")
        subtitle.setAlignment(Qt.AlignCenter)

        start_btn = QPushButton("Start")
        start_btn.setFixedWidth(200)
        start_btn.clicked.connect(
            lambda: self.stack.setCurrentWidget(self.stack.model_select)
        )

        # Theme selector
        theme_row = QHBoxLayout()
        theme_row.setAlignment(Qt.AlignCenter)
        theme_label = QLabel("Theme:")
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(THEME_NAMES)
        self.theme_combo.setCurrentText(DEFAULT_THEME)
        self.theme_combo.setFixedWidth(160)
        self.theme_combo.currentTextChanged.connect(self._on_theme_changed)
        theme_row.addWidget(theme_label)
        theme_row.addWidget(self.theme_combo)

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addSpacing(30)
        layout.addWidget(start_btn, alignment=Qt.AlignCenter)
        layout.addSpacing(20)
        layout.addLayout(theme_row)

        self.setLayout(layout)

    def _on_theme_changed(self, name):
        self.stack.apply_theme(name)
