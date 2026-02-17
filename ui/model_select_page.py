from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QComboBox,
    QPushButton,
    QSpinBox,
    QRadioButton,
    QButtonGroup,
    QListWidget,
    QListWidgetItem,
    QMessageBox,
    QGroupBox,
)
from PySide6.QtCore import Qt, QThread, Signal
from pipeline.persistence import load_settings, save_settings


class ModelFetchThread(QThread):
    models_ready = Signal(list)
    error = Signal(str)

    def __init__(self, port):
        super().__init__()
        self.port = port

    def run(self):
        try:
            from pipeline.ollama_client import list_models

            models = list_models(self.port)
            self.models_ready.emit(models)
        except Exception as e:
            self.error.emit(str(e))


class ModelSelectPage(QWidget):
    def __init__(self, stack):
        super().__init__()
        self.stack = stack
        self._pending_settings = {}

        layout = QVBoxLayout()
        layout.setSpacing(12)

        # --- Port config ---
        port_layout = QHBoxLayout()
        port_layout.addWidget(QLabel("Ollama Port:"))
        self.port_spin = QSpinBox()
        self.port_spin.setRange(1024, 65535)
        self.port_spin.setValue(11434)
        port_layout.addWidget(self.port_spin)

        self.refresh_btn = QPushButton("Refresh Models")
        self.refresh_btn.clicked.connect(self.fetch_models)
        port_layout.addWidget(self.refresh_btn)
        port_layout.addStretch()
        layout.addLayout(port_layout)

        # --- Pipeline mode ---
        mode_group_box = QGroupBox("Pipeline Mode")
        mode_layout = QHBoxLayout()
        self.single_radio = QRadioButton("Single Reasoning")
        self.debate_radio = QRadioButton("Multi-Debate")
        self.single_radio.setChecked(True)

        self.mode_group = QButtonGroup()
        self.mode_group.addButton(self.single_radio)
        self.mode_group.addButton(self.debate_radio)

        mode_layout.addWidget(self.single_radio)
        mode_layout.addWidget(self.debate_radio)
        mode_layout.addStretch()
        mode_group_box.setLayout(mode_layout)
        layout.addWidget(mode_group_box)

        self.single_radio.toggled.connect(self._update_mode_visibility)

        # --- Single mode section ---
        self.single_group = QGroupBox("Model Selection")
        single_layout = QVBoxLayout()

        single_layout.addWidget(QLabel("Reasoning Model (initial idea)"))
        self.reasoning_combo = QComboBox()
        single_layout.addWidget(self.reasoning_combo)

        single_layout.addWidget(QLabel("Judge Model (complements with knowledge)"))
        self.single_judge_combo = QComboBox()
        single_layout.addWidget(self.single_judge_combo)

        single_layout.addWidget(QLabel("Final Model (synthesizes answer)"))
        self.single_final_combo = QComboBox()
        single_layout.addWidget(self.single_final_combo)

        self.single_group.setLayout(single_layout)
        layout.addWidget(self.single_group)

        # --- Debate mode section ---
        self.debate_group = QGroupBox("Model Selection")
        debate_layout = QVBoxLayout()

        debate_layout.addWidget(QLabel("Debate Models (check 2 or more)"))
        self.debate_list = QListWidget()
        self.debate_list.setMaximumHeight(150)
        debate_layout.addWidget(self.debate_list)

        debate_layout.addWidget(QLabel("Judge Model"))
        self.judge_combo = QComboBox()
        debate_layout.addWidget(self.judge_combo)

        debate_layout.addWidget(QLabel("Final Model"))
        self.final_combo = QComboBox()
        debate_layout.addWidget(self.final_combo)

        self.debate_group.setLayout(debate_layout)
        layout.addWidget(self.debate_group)

        self.debate_group.setVisible(False)

        # --- Buttons ---
        btn_layout = QHBoxLayout()
        back_btn = QPushButton("Back")
        back_btn.clicked.connect(lambda: self.stack.setCurrentWidget(self.stack.run_page))
        btn_layout.addWidget(back_btn)
        btn_layout.addStretch()

        self.next_btn = QPushButton("Continue")
        self.next_btn.clicked.connect(self.go_next)
        btn_layout.addWidget(self.next_btn)
        layout.addLayout(btn_layout)

        self.setLayout(layout)

    def showEvent(self, event):
        super().showEvent(event)
        s = load_settings()
        if s.get("port"):
            self.port_spin.setValue(s["port"])
        if s.get("mode") == "debate":
            self.debate_radio.setChecked(True)
        else:
            self.single_radio.setChecked(True)
        self._pending_settings = s
        if self.reasoning_combo.count() == 0 and self.refresh_btn.isEnabled():
            self.fetch_models()

    def _update_mode_visibility(self):
        is_single = self.single_radio.isChecked()
        self.single_group.setVisible(is_single)
        self.debate_group.setVisible(not is_single)

    def fetch_models(self):
        self.refresh_btn.setEnabled(False)
        self.refresh_btn.setText("Loading...")
        self._fetch_thread = ModelFetchThread(self.port_spin.value())
        self._fetch_thread.models_ready.connect(self._on_models_loaded)
        self._fetch_thread.error.connect(self._on_fetch_error)
        self._fetch_thread.start()

    def _apply_settings(self, s):
        def set_combo(combo, key):
            val = s.get(key, "")
            idx = combo.findText(val)
            if idx >= 0:
                combo.setCurrentIndex(idx)

        set_combo(self.reasoning_combo, "reasoning_model")
        set_combo(self.single_judge_combo, "judge_model")
        set_combo(self.single_final_combo, "final_model")
        set_combo(self.judge_combo, "judge_model_debate")
        set_combo(self.final_combo, "final_model_debate")

        saved_debate = set(s.get("debate_models", []))
        for i in range(self.debate_list.count()):
            item = self.debate_list.item(i)
            item.setCheckState(
                Qt.Checked if item.text() in saved_debate else Qt.Unchecked
            )

    def _on_models_loaded(self, models):
        self.refresh_btn.setEnabled(True)
        self.refresh_btn.setText("Refresh Models")

        self.reasoning_combo.clear()
        self.single_judge_combo.clear()
        self.single_final_combo.clear()
        self.judge_combo.clear()
        self.final_combo.clear()
        self.debate_list.clear()

        self.reasoning_combo.addItems(models)
        self.single_judge_combo.addItems(models)
        self.single_final_combo.addItems(models)
        self.judge_combo.addItems(models)
        self.final_combo.addItems(models)

        for name in models:
            item = QListWidgetItem(name)
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
            item.setCheckState(Qt.Unchecked)
            self.debate_list.addItem(item)

        if self._pending_settings:
            self._apply_settings(self._pending_settings)

    def _on_fetch_error(self, error_msg):
        self.refresh_btn.setEnabled(True)
        self.refresh_btn.setText("Refresh Models")
        QMessageBox.warning(
            self,
            "Connection Error",
            f"Cannot connect to Ollama on port {self.port_spin.value()}.\n\n"
            f"Is Ollama running?\n\n{error_msg}",
        )

    def _get_checked_debate_models(self):
        checked = []
        for i in range(self.debate_list.count()):
            item = self.debate_list.item(i)
            if item.checkState() == Qt.Checked:
                checked.append(item.text())
        return checked

    def go_next(self):
        if self.single_radio.isChecked():
            if (
                not self.reasoning_combo.currentText()
                or not self.single_judge_combo.currentText()
                or not self.single_final_combo.currentText()
            ):
                QMessageBox.warning(self, "No Model", "Please select all three models.")
                return
            config = {
                "mode": "single",
                "port": self.port_spin.value(),
                "reasoning_model": self.reasoning_combo.currentText(),
                "judge_model": self.single_judge_combo.currentText(),
                "final_model": self.single_final_combo.currentText(),
                "question": "",
            }
            save_settings({
                "port": self.port_spin.value(),
                "mode": "single",
                "reasoning_model": config["reasoning_model"],
                "judge_model": config["judge_model"],
                "final_model": config["final_model"],
            })
        else:
            debate_models = self._get_checked_debate_models()
            if len(debate_models) < 2:
                QMessageBox.warning(
                    self, "Not Enough Models", "Select at least 2 debate models."
                )
                return
            if not self.judge_combo.currentText() or not self.final_combo.currentText():
                QMessageBox.warning(self, "No Model", "Please select judge and final models.")
                return
            config = {
                "mode": "debate",
                "port": self.port_spin.value(),
                "debate_models": debate_models,
                "judge_model": self.judge_combo.currentText(),
                "final_model": self.final_combo.currentText(),
                "question": "",
            }
            save_settings({
                "port": self.port_spin.value(),
                "mode": "debate",
                "debate_models": debate_models,
                "judge_model_debate": config["judge_model"],
                "final_model_debate": config["final_model"],
            })

        self.stack.run_page.set_config(config)
        self.stack.setCurrentWidget(self.stack.run_page)
