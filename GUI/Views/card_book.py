from PyQt6.QtWidgets import QWidget, QLabel, QHBoxLayout, QVBoxLayout, QApplication
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt, QSize

class CardWidget(QWidget):
    def __init__(self, img_path, title_text, author_text, parent=None):
        super().__init__(parent)
        # make fixed size
        self.setFixedSize(QSize(250, 150))
        self.initUI(img_path, title_text, author_text)

    def initUI(self, img_path, title_text, author_text):
        self.img_label = QLabel(self)
        pixmap = QPixmap(img_path)
        # Maintain a 4:3 aspect ratio
        self.img_label.setPixmap(pixmap.scaled(122, 150, Qt.AspectRatioMode.KeepAspectRatioByExpanding, Qt.TransformationMode.SmoothTransformation))
        self.img_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.title_label = QLabel(title_text, self)
        self.title_label.setWordWrap(True)
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.title_label.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)

        self.author_label = QLabel(author_text, self)
        self.author_label.setWordWrap(True)
        self.author_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.author_label.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)

        # Create a widget to hold the text layout
        text_widget = QWidget(self)
        self.text_layout = QVBoxLayout(text_widget)
        self.text_layout.setContentsMargins(8, 8, 8, 8)

        self.text_layout.addWidget(self.title_label)
        self.text_layout.setAlignment(self.title_label, Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        self.text_layout.addStretch()
        self.text_layout.addWidget(self.author_label)
        self.text_layout.setAlignment(self.author_label, Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        
        # Create the main layout and add the widgets
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.addWidget(self.img_label)
        self.layout.setAlignment(self.img_label, Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(text_widget)  # Add the text widget here
        self.setLayout(self.layout)

# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     card = CardWidget("default.png", "Title Text will be here and Align to left", "Author Text")
#     card.show()
#     sys.exit(app.exec())
