from PyQt6.QtWidgets import QApplication, QFrame, QVBoxLayout, QPushButton, QWidget

class MyWidget(QWidget):
    def __init__(self):
        super().__init__()

        # Create a frame
        self.frame = QFrame(self)
        self.frame.setObjectName("MyFrame")

        # Create a layout
        layout = QVBoxLayout(self)
        layout.addWidget(self.frame)

        # Create a push button to toggle the state
        self.toggle_button = QPushButton("Toggle State", self)
        layout.addWidget(self.toggle_button)

        # Connect the button click event to toggle the state
        self.toggle_button.clicked.connect(self.toggleState)

        # Set the initial style sheet
        self.setStyleSheet(
            """
            QFrame {
                border: 0px solid #000;
                border-radius: 20px;
                background-color: #bce0fd;
            }
            QFrame[alternateState="true"] {
                background-color: #ff0000;  /* Change this to your desired color */
            }
            """
        )

    def toggleState(self):
        # Toggle the alternate state of the frame
        current_state = self.frame.property("alternateState")
        self.frame.setProperty("alternateState", not current_state)
        self.frame.style().unpolish(self.frame)
        self.frame.style().polish(self.frame)

if __name__ == "__main__":
    app = QApplication([])

    # Set up and show the main window
    main_window = MyWidget()
    main_window.show()

    app.exec()
