import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QTextEdit, QFileDialog,
    QMessageBox, QSplitter
)
from PySide6.QtGui import QAction
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtCore import Qt
import markdown


class MarkdownEditor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Live Markdown Editor")
        self.resize(1200, 800)
        self.current_file = None
        self.is_dark = False

        splitter = QSplitter(Qt.Horizontal)
        self.editor = QTextEdit()
        self.editor.setPlaceholderText("Enter Markdown here...")
        self.editor.setStyleSheet("font-family: Consolas; font-size: 14px;")
        splitter.addWidget(self.editor)

        self.preview = QWebEngineView()
        splitter.addWidget(self.preview)

        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 1)
        self.setCentralWidget(splitter)

        self.editor.textChanged.connect(self.update_preview)

        self._create_actions()
        self._create_menus()

        self.update_preview()

    def _create_actions(self):
        self.open_action = QAction("&Open...", self, shortcut="Ctrl+O", triggered=self.open_file)
        self.save_action = QAction("&Save", self, shortcut="Ctrl+S", triggered=self.save_file)
        self.save_as_action = QAction("Save &As...", self, triggered=self.save_file_as)
        self.export_html_action = QAction("Export &HTML...", self, triggered=self.export_html)
        self.exit_action = QAction("E&xit", self, shortcut="Ctrl+Q", triggered=self.close)
        self.toggle_theme_action = QAction("&Toggle Dark Mode", self, shortcut="Ctrl+T", triggered=self.toggle_theme)
        self.about_action = QAction("&About", self, triggered=self.show_about)

    def _create_menus(self):
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu("&File")
        file_menu.addAction(self.open_action)
        file_menu.addAction(self.save_action)
        file_menu.addAction(self.save_as_action)
        file_menu.addSeparator()
        file_menu.addAction(self.export_html_action)
        file_menu.addSeparator()
        file_menu.addAction(self.exit_action)

        view_menu = menu_bar.addMenu("&View")
        view_menu.addAction(self.toggle_theme_action)

        help_menu = menu_bar.addMenu("&Help")
        help_menu.addAction(self.about_action)

    def update_preview(self):
        md = self.editor.toPlainText()
        html_body = markdown.markdown(md, extensions=['fenced_code', 'tables', 'codehilite'])
        css = self.dark_css if self.is_dark else self.light_css
        full_html = f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <style>{css}</style>
</head>
<body>
{html_body}
</body>
</html>"""
        self.preview.setHtml(full_html)

    def open_file(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Open Markdown File", "", "Markdown Files (*.md *.markdown);;All Files (*)"
        )
        if path:
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    text = f.read()
                self.editor.setPlainText(text)
                self.current_file = path
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Could not open file:\n{e}")

    def save_file(self):
        if self.current_file:
            try:
                with open(self.current_file, 'w', encoding='utf-8') as f:
                    f.write(self.editor.toPlainText())
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Could not save file:\n{e}")
        else:
            self.save_file_as()

    def save_file_as(self):
        path, _ = QFileDialog.getSaveFileName(
            self, "Save Markdown File As", "", "Markdown Files (*.md *.markdown);;All Files (*)"
        )
        if path:
            self.current_file = path
            self.save_file()

    def export_html(self):
        path, _ = QFileDialog.getSaveFileName(
            self, "Export HTML", "", "HTML Files (*.html *.htm);;All Files (*)"
        )
        if path:
            try:
                md = self.editor.toPlainText()
                html_body = markdown.markdown(md, extensions=['fenced_code', 'tables', 'codehilite'])
                css = self.dark_css if self.is_dark else self.light_css
                full_html = f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <style>{css}</style>
</head>
<body>
{html_body}
</body>
</html>"""
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(full_html)
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Could not export HTML:\n{e}")

    def toggle_theme(self):
        self.is_dark = not self.is_dark
        self.update_preview()

    def show_about(self):
        QMessageBox.about(
            self, "About Live Markdown Editor",
            "Live Markdown Editor\nBuilt with PySide6 and Python"
        )

    @property
    def light_css(self):
        return """
body { font-family: Arial, sans-serif; background-color: #ffffff; color: #000000; padding: 1em; }
code { background-color: #f4f4f4; padding: 2px 4px; }
pre { background-color: #f4f4f4; padding: 1em; overflow-x: auto; }
"""

    @property
    def dark_css(self):
        return """
body { font-family: Arial, sans-serif; background-color: #2b2b2b; color: #e6e6e6; padding: 1em; }
code { background-color: #3c3f41; padding: 2px 4px; color: #f8f8f2; }
pre { background-color: #3c3f41; padding: 1em; overflow-x: auto; }
"""


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MarkdownEditor()
    window.show()
    sys.exit(app.exec())