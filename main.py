import sys
from PySide6.QtWidgets import QApplication, QStackedWidget
from ui.home_page import HomePage
from ui.model_select_page import ModelSelectPage
from ui.run_page import RunPage
from ui.styles import get_theme, DEFAULT_THEME


class App(QStackedWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Reasoning Lab")
        self.resize(1100, 700)
        self.current_theme_name = DEFAULT_THEME

        self.home = HomePage(self)
        self.model_select = ModelSelectPage(self)
        self.run_page = RunPage(self)

        self.addWidget(self.home)
        self.addWidget(self.model_select)
        self.addWidget(self.run_page)

        self.setCurrentWidget(self.home)
        self.apply_theme(DEFAULT_THEME)

    def apply_theme(self, name):
        self.current_theme_name = name
        theme = get_theme(name)
        QApplication.instance().setStyleSheet(theme["qss"])
        self.run_page.set_theme(theme)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = App()
    window.show()
    sys.exit(app.exec())
