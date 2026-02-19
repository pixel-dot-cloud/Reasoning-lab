import os

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QTextEdit,
    QLineEdit,
    QPushButton,
    QLabel,
    QMessageBox,
    QInputDialog,
    QScrollArea,
    QSplitter,
    QFrame,
    QListWidget,
    QListWidgetItem,
    QFileDialog,
)
from PySide6.QtGui import QFont, QTextCursor
from PySide6.QtCore import Qt, QSize, QTimer
from pipeline.controller import PipelineThread
from pipeline.persistence import list_chats, save_chat, delete_chat, new_chat_record
from ui.styles import get_theme, DEFAULT_THEME


class RunPage(QWidget):
    def __init__(self, stack):
        super().__init__()
        self.stack = stack
        self.config = None
        self.thread = None
        self._streaming_final = False
        self._final_buffer = ""
        self._theme = get_theme(DEFAULT_THEME)
        self._chat_history = []
        self._current_chat = None
        self._saved_chats = []
        self._attached_file = None
        self._streaming_label = None

        layout = QVBoxLayout()
        layout.setSpacing(6)
        layout.setContentsMargins(8, 8, 8, 8)

        # --- Top bar ---
        top_bar = QHBoxLayout()

        self.back_btn = QPushButton("Back")
        self.back_btn.setObjectName("backBtn")
        self.back_btn.clicked.connect(
            lambda: self.stack.setCurrentWidget(self.stack.home)
        )
        top_bar.addWidget(self.back_btn)

        self.chats_btn = QPushButton("\u2630 Chats")
        self.chats_btn.setObjectName("chatsBtn")
        self.chats_btn.setCheckable(True)
        self.chats_btn.clicked.connect(self._toggle_chats_panel)
        top_bar.addWidget(self.chats_btn)

        self.new_chat_btn = QPushButton("+ New Chat")
        self.new_chat_btn.setObjectName("newChatBtn")
        self.new_chat_btn.clicked.connect(self._new_chat)
        top_bar.addWidget(self.new_chat_btn)

        top_bar.addStretch()

        self.mode_label = QLabel("No models selected — click 'Select Models'")
        self.mode_label.setObjectName("modeLabel")
        top_bar.addWidget(self.mode_label)

        self.models_btn = QPushButton("Select Models")
        self.models_btn.setObjectName("modelsBtn")
        self.models_btn.clicked.connect(
            lambda: self.stack.setCurrentWidget(self.stack.model_select)
        )
        top_bar.addWidget(self.models_btn)

        layout.addLayout(top_bar)

        # --- Main splitter: Chats panel | Chat area | Reasoning panel ---
        self.splitter = QSplitter(Qt.Horizontal)

        # Chats history side panel
        self.chats_panel = QFrame()
        self.chats_panel.setObjectName("chatsPanel")
        chats_panel_layout = QVBoxLayout()
        chats_panel_layout.setContentsMargins(4, 4, 4, 4)
        chats_panel_layout.setSpacing(4)

        chats_header = QLabel("History")
        chats_header.setObjectName("reasoningHeader")
        chats_panel_layout.addWidget(chats_header)

        self.chats_list = QListWidget()
        self.chats_list.setObjectName("chatsList")
        self.chats_list.itemClicked.connect(self._open_chat_from_panel)
        chats_panel_layout.addWidget(self.chats_list, 1)

        chat_actions = QHBoxLayout()
        chat_actions.setSpacing(4)

        self.rename_chat_btn = QPushButton("Rename")
        self.rename_chat_btn.clicked.connect(self._rename_chat_from_panel)
        chat_actions.addWidget(self.rename_chat_btn)

        self.delete_chat_btn = QPushButton("Delete")
        self.delete_chat_btn.clicked.connect(self._delete_chat_from_panel)
        chat_actions.addWidget(self.delete_chat_btn)

        chats_panel_layout.addLayout(chat_actions)

        self.chats_panel.setLayout(chats_panel_layout)
        self.chats_panel.setVisible(False)
        self.splitter.addWidget(self.chats_panel)

        # Chat area — scroll area with individual message widgets
        self.chat_scroll = QScrollArea()
        self.chat_scroll.setObjectName("chatArea")
        self.chat_scroll.setWidgetResizable(True)
        self.chat_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.chat_container = QWidget()
        self.chat_container.setObjectName("chatContainer")
        self.chat_layout = QVBoxLayout(self.chat_container)
        self.chat_layout.setAlignment(Qt.AlignTop)
        self.chat_layout.setSpacing(4)
        self.chat_layout.setContentsMargins(8, 8, 8, 8)
        self.chat_scroll.setWidget(self.chat_container)
        self.splitter.addWidget(self.chat_scroll)

        # Reasoning panel
        reasoning_frame = QFrame()
        reasoning_frame.setObjectName("reasoningFrame")
        reasoning_layout = QVBoxLayout()
        reasoning_layout.setContentsMargins(0, 0, 0, 0)
        reasoning_layout.setSpacing(4)

        reasoning_header = QLabel("Intermediate Reasoning")
        reasoning_header.setObjectName("reasoningHeader")
        reasoning_layout.addWidget(reasoning_header)

        self.reasoning_area = QTextEdit()
        self.reasoning_area.setReadOnly(True)
        self.reasoning_area.setFont(QFont("Monospace", 10))
        self.reasoning_area.setObjectName("reasoningArea")
        reasoning_layout.addWidget(self.reasoning_area)

        reasoning_frame.setLayout(reasoning_layout)
        self.splitter.addWidget(reasoning_frame)

        self.splitter.setSizes([0, 500, 400])
        layout.addWidget(self.splitter, 1)

        # --- Status ---
        self.status_label = QLabel("Ready")
        self.status_label.setObjectName("statusLabel")
        layout.addWidget(self.status_label)

        # --- Input bar ---
        input_bar = QHBoxLayout()
        input_bar.setSpacing(6)

        self.attach_btn = QPushButton("Attach")
        self.attach_btn.setObjectName("attachBtn")
        self.attach_btn.clicked.connect(self._attach_file)
        input_bar.addWidget(self.attach_btn)

        self.input_field = QLineEdit()
        self.input_field.setObjectName("chatInput")
        self.input_field.setPlaceholderText("Type your question and press Enter...")
        self.input_field.returnPressed.connect(self.run_pipeline)
        input_bar.addWidget(self.input_field, 1)

        self.send_btn = QPushButton("Send")
        self.send_btn.setObjectName("sendBtn")
        self.send_btn.clicked.connect(self.run_pipeline)
        input_bar.addWidget(self.send_btn)

        self.stop_btn = QPushButton("Stop")
        self.stop_btn.setObjectName("stopBtn")
        self.stop_btn.setEnabled(False)
        self.stop_btn.clicked.connect(self.stop_pipeline)
        input_bar.addWidget(self.stop_btn)

        layout.addLayout(input_bar)

        # --- Attachment label ---
        self.attachment_label = QLabel("")
        self.attachment_label.setObjectName("attachmentLabel")
        self.attachment_label.setVisible(False)
        layout.addWidget(self.attachment_label)
        self.setLayout(layout)

    # ------------------------------------------------------------------ theme

    def set_theme(self, theme):
        self._theme = theme
        self._rebuild_chat()

    # ----------------------------------------------------------- mode helpers

    def _update_mode_label(self, config):
        mode = config.get("mode", "single")
        if mode == "single":
            self.mode_label.setText(
                f"Single: {config.get('reasoning_model', '')} + "
                f"{config.get('judge_model', '')} + "
                f"{config.get('final_model', '')}"
            )
        else:
            n = len(config.get("debate_models", []))
            self.mode_label.setText(
                f"Debate: {n} models + {config.get('judge_model', '')} + "
                f"{config.get('final_model', '')}"
            )

    # ----------------------------------------------------------- config / chat

    def set_config(self, config):
        self.config = config
        self._update_mode_label(config)
        self._new_chat()

    def load_chat(self, chat: dict):
        self._current_chat = chat
        self._chat_history = list(chat.get("messages", []))
        self._final_buffer = ""
        self._streaming_final = False
        self._streaming_label = None
        self._rebuild_chat()
        self.reasoning_area.clear()
        self.status_label.setText("Ready")
        if self.config:
            self._update_mode_label(self.config)

    def _new_chat(self):
        self._current_chat = None
        self._chat_history = []
        self._final_buffer = ""
        self._streaming_final = False
        self._streaming_label = None
        self._rebuild_chat()
        self.reasoning_area.clear()
        self.status_label.setText("Ready")

    # ----------------------------------------------------- chats side panel

    def _toggle_chats_panel(self):
        visible = self.chats_panel.isVisible()
        if not visible:
            self._reload_chats_panel()
            self.chats_panel.setVisible(True)
            self.splitter.setSizes([220, 480, 400])
        else:
            self.chats_panel.setVisible(False)
            self.splitter.setSizes([0, 500, 400])
        self.chats_btn.setChecked(not visible)

    def _reload_chats_panel(self):
        self._saved_chats = list_chats()
        self.chats_list.clear()
        for chat in self._saved_chats:
            msgs = len(chat.get("messages", []))
            updated = chat.get("updated_at", "")[:16].replace("T", " ")
            mode = chat.get("config", {}).get("mode", "?")
            display = (
                f"{chat['name']}\n"
                f"{updated}  \u2022  {msgs} msg{'s' if msgs != 1 else ''}  \u2022  {mode}"
            )
            item = QListWidgetItem(display)
            item.setData(Qt.UserRole, chat["id"])
            item.setSizeHint(QSize(0, 52))
            self.chats_list.addItem(item)

    def _open_chat_from_panel(self, item):
        cid = item.data(Qt.UserRole)
        chat = next((c for c in self._saved_chats if c["id"] == cid), None)
        if chat:
            self.load_chat(chat)

    def _rename_chat_from_panel(self):
        item = self.chats_list.currentItem()
        if not item:
            return
        cid = item.data(Qt.UserRole)
        chat = next((c for c in self._saved_chats if c["id"] == cid), None)
        if not chat:
            return
        new_name, ok = QInputDialog.getText(
            self, "Rename Chat", "New name:", text=chat["name"]
        )
        if ok and new_name.strip():
            chat["name"] = new_name.strip()
            save_chat(chat)
            if self._current_chat and self._current_chat.get("id") == cid:
                self._current_chat["name"] = chat["name"]
            self._reload_chats_panel()

    def _delete_chat_from_panel(self):
        item = self.chats_list.currentItem()
        if not item:
            return
        cid = item.data(Qt.UserRole)
        chat = next((c for c in self._saved_chats if c["id"] == cid), None)
        name = chat["name"] if chat else "this chat"
        reply = QMessageBox.question(
            self, "Delete Chat",
            f"Delete '{name}'?",
            QMessageBox.Yes | QMessageBox.No,
        )
        if reply == QMessageBox.Yes:
            if self._current_chat and self._current_chat.get("id") == cid:
                self._new_chat()
            delete_chat(cid)
            self._reload_chats_panel()

    # ---------------------------------------------------------- chat widgets

    def _clear_chat_layout(self):
        while self.chat_layout.count():
            item = self.chat_layout.takeAt(0)
            w = item.widget()
            if w:
                w.deleteLater()

    def _make_bubble(self, text, is_user):
        """Return (row_widget, label, bubble_layout) for a message bubble."""
        bg = self._theme["user_bubble_bg" if is_user else "bot_bubble_bg"]
        fg = self._theme["user_bubble_fg" if is_user else "bot_bubble_fg"]

        bubble = QFrame()
        bubble.setStyleSheet(
            f"QFrame {{ background-color: {bg}; border-radius: 8px; }}"
            f" QLabel {{ color: {fg}; background: transparent; font-size: 14px; }}"
            f" QPushButton {{ background: transparent; border: none;"
            f" color: {fg}; font-size: 11px; padding: 0 2px; font-weight: normal; }}"
            f" QPushButton:hover {{ text-decoration: underline; }}"
        )
        bubble_layout = QVBoxLayout(bubble)
        bubble_layout.setContentsMargins(10, 7, 10, 7)
        bubble_layout.setSpacing(3)

        label = QLabel(text)
        label.setWordWrap(True)
        label.setTextInteractionFlags(Qt.TextSelectableByMouse)
        label.setMinimumWidth(60)
        bubble_layout.addWidget(label)

        row = QWidget()
        row_layout = QHBoxLayout(row)
        row_layout.setContentsMargins(0, 0, 0, 0)
        row_layout.setSpacing(4)

        if is_user:
            row_layout.addStretch(3)
            row_layout.addWidget(bubble, 7)
        else:
            row_layout.addWidget(bubble, 7)
            row_layout.addStretch(3)

        return row, label, bubble_layout

    def _add_message_widget(self, index, msg):
        is_user = msg["role"] == "user"
        row, label, bubble_layout = self._make_bubble(msg["text"], is_user)

        if is_user:
            edit_btn = QPushButton("edit")
            edit_btn.setFlat(True)
            edit_btn.setCursor(Qt.PointingHandCursor)
            edit_btn.clicked.connect(lambda checked, idx=index: self._edit_message(idx))
            bubble_layout.addWidget(edit_btn, 0, Qt.AlignRight)

        self.chat_layout.addWidget(row)

    def _add_streaming_widget(self):
        """Add a bot bubble for the in-progress response and return its label."""
        row, label, _ = self._make_bubble("", is_user=False)
        self.chat_layout.addWidget(row)
        return label

    def _rebuild_chat(self):
        self._streaming_label = None
        self._clear_chat_layout()
        for i, msg in enumerate(self._chat_history):
            self._add_message_widget(i, msg)
        self._scroll_to_bottom()

    def _scroll_to_bottom(self):
        QTimer.singleShot(0, lambda: self.chat_scroll.verticalScrollBar().setValue(
            self.chat_scroll.verticalScrollBar().maximum()
        ))

    # ------------------------------------------------------------ edit message

    def _edit_message(self, index):
        msg = self._chat_history[index]
        new_text, ok = QInputDialog.getMultiLineText(
            self, "Edit Message", "Edit your message:", msg["text"]
        )
        if not ok or not new_text.strip():
            return
        # Truncate history from this point and re-run from the edited message
        self._chat_history = self._chat_history[:index]
        if self._current_chat is not None:
            self._current_chat["messages"] = list(self._chat_history)
            save_chat(self._current_chat)
        self._rebuild_chat()
        self.input_field.setText(new_text.strip())
        self.run_pipeline()

    # ----------------------------------------------------------- file attachment

    def _attach_file(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Attach File", "",
            "Text files (*.txt *.md *.py *.js *.ts *.json *.csv *.html *.xml *.yaml *.yml *.toml *.ini *.cfg *.log);;All files (*)"
        )
        if not path:
            return
        try:
            with open(path, "r", encoding="utf-8", errors="replace") as f:
                content = f.read()
        except Exception as e:
            QMessageBox.warning(self, "File Error", f"Could not read file:\n{e}")
            return
        name = os.path.basename(path)
        self._attached_file = {"name": name, "content": content}
        self.attachment_label.setText(f"Attached: {name}  [click to remove]")
        self.attachment_label.setVisible(True)
        self.attachment_label.mousePressEvent = lambda _: self._clear_attachment()

    def _clear_attachment(self):
        self._attached_file = None
        self.attachment_label.setText("")
        self.attachment_label.setVisible(False)

    # --------------------------------------------------------------- pipeline

    def run_pipeline(self):
        question = self.input_field.text().strip()
        if not question:
            return
        if not self.config:
            QMessageBox.warning(self, "No Config", "Click 'Select Models' to set up models first.")
            return

        self.config["question"] = question
        self.config["chat_context"] = self.get_chat_context()
        self.config["file_context"] = (
            f"[File: {self._attached_file['name']}]\n{self._attached_file['content']}"
            if self._attached_file else ""
        )
        self.input_field.clear()
        self.reasoning_area.clear()
        self._final_buffer = ""
        self._streaming_final = False
        self._streaming_label = None

        user_text = question
        if self._attached_file:
            user_text = f"[{self._attached_file['name']}] {question}"
        self._chat_history.append({"role": "user", "text": user_text})
        self._clear_attachment()

        # Add the user bubble immediately without full rebuild
        self._add_message_widget(len(self._chat_history) - 1, self._chat_history[-1])
        self._scroll_to_bottom()

        if self._current_chat is None:
            self._current_chat = new_chat_record()
        self._current_chat["messages"] = list(self._chat_history)
        save_chat(self._current_chat)

        self.send_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        self.back_btn.setEnabled(False)
        self.models_btn.setEnabled(False)
        self.input_field.setEnabled(False)
        self.attach_btn.setEnabled(False)
        self.status_label.setText("Running pipeline...")

        self.thread = PipelineThread(self.config)
        self.thread.token_update.connect(self._on_token)
        self.thread.final_token.connect(self._on_final_token)
        self.thread.stage_complete.connect(self._on_stage_complete)
        self.thread.finished_signal.connect(self._on_finished)
        self.thread.error_signal.connect(self._on_error)
        self.thread.finished.connect(self._on_thread_finished)
        self.thread.start()

    def stop_pipeline(self):
        if self.thread:
            self.thread.stop()
            self.status_label.setText("Stopping...")
            self.stop_btn.setEnabled(False)

    def _on_token(self, text):
        self.reasoning_area.moveCursor(QTextCursor.End)
        self.reasoning_area.insertPlainText(text)
        self.reasoning_area.moveCursor(QTextCursor.End)

    def _on_final_token(self, text):
        self._final_buffer += text
        if not self._streaming_final:
            self._streaming_final = True
            self._streaming_label = self._add_streaming_widget()
        self._streaming_label.setText(self._final_buffer)
        self._scroll_to_bottom()

    def _on_stage_complete(self, stage, _text):
        self.status_label.setText(f"Completed: {stage}")

    def _on_finished(self, final_answer):
        self._streaming_final = False
        self._streaming_label = None
        self._chat_history.append({"role": "bot", "text": final_answer})
        self._rebuild_chat()
        self._reset_controls()
        self.status_label.setText("Done")

        if self._current_chat is not None:
            if len(self._current_chat["messages"]) == 1:
                first_q = self._current_chat["messages"][0]["text"]
                self._current_chat["name"] = first_q[:60].strip()
            self._current_chat["messages"] = list(self._chat_history)
            save_chat(self._current_chat)
            if self.chats_panel.isVisible():
                self._reload_chats_panel()

    def _on_error(self, error_msg):
        self._streaming_final = False
        self._streaming_label = None
        if self._final_buffer:
            self._chat_history.append(
                {"role": "bot", "text": self._final_buffer + "\n[interrupted]"}
            )
        self._rebuild_chat()
        self._reset_controls()
        self.status_label.setText("Error")

        if self._current_chat is not None and self._chat_history:
            self._current_chat["messages"] = list(self._chat_history)
            save_chat(self._current_chat)

        QMessageBox.critical(self, "Pipeline Error", error_msg)

    def _on_thread_finished(self):
        if self.thread is not None:
            self._streaming_label = None
            self._reset_controls()
            self.status_label.setText("Stopped")

    def _reset_controls(self):
        self.send_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        self.back_btn.setEnabled(True)
        self.models_btn.setEnabled(True)
        self.input_field.setEnabled(True)
        self.attach_btn.setEnabled(True)
        self.input_field.setFocus()
        self.thread = None

    def get_chat_context(self):
        if not self._chat_history:
            return ""
        lines = []
        for msg in self._chat_history:
            role = "User" if msg["role"] == "user" else "Assistant"
            lines.append(f"{role}: {msg['text']}")
        return "\n".join(lines)
