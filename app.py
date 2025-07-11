from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setFixedSize(800, 600)
        self.setWindowTitle("Markdown Editor")

        self.button = QPushButton("Click Me")

        self.button.clicked.connect(self.button_clicked)
        self.button.clicked.connect(self.button_toggled)

        self.setCentralWidget(self.button)

    def button_clicked(self):
        self.button.setText("You already clicked me.")
        self.button.setEnabled(False)
        self.setWindowTitle("A new window title")

    def button_toggled(self, checked):
        print("Check State:", checked)


app = QApplication([])

window = MainWindow()
window.show()

app.exec()