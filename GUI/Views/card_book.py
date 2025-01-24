from PyQt6.QtWidgets import QWidget, QLabel, QHBoxLayout, QVBoxLayout, QApplication
from PyQt6.QtGui import QPixmap, QFont, QColor
from PyQt6.QtCore import Qt, QSize, pyqtSignal

class CardWidget(QWidget):
    clicked = pyqtSignal(object)

    def __init__(self, book, parent=None):
        super().__init__(parent)
        self.book = book
        img_path = book.get_thumbnail()
        title_text = book.get_title()
        author_text = book.get_author()[0] if isinstance(book.get_author(), tuple) else book.get_author()
        self.pages = book.get_pages()
        self.genre = book.get_genre()

        self.setFixedSize(QSize(350, 150))
        self.initUI(img_path, title_text, author_text, book.get_subtitle(), self.pages, self.genre)

        self.setStyleSheet("background-color: transparent;")  # Initial background color

    def initUI(self, img_path, title_text, author_text, subtitle_text="", pages=None, genre=None):
        # Image Label
        self.img_label = QLabel(self)
        pixmap = QPixmap(img_path)
        if pixmap.isNull():
            pixmap = QPixmap("default.png")
        self.img_label.setPixmap(pixmap.scaled(122, 150, Qt.AspectRatioMode.KeepAspectRatioByExpanding, Qt.TransformationMode.SmoothTransformation))
        self.img_label.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)

        # Title Label
        self.title_label = QLabel(title_text, self)
        self.title_label.setWordWrap(True)
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.title_label.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.title_label.setStyleSheet("font: 14pt Arial;")
        self.title_label.setMinimumWidth(350 - 122 - 8)

        # Subtitle Label
        self.subtitle_label = QLabel(subtitle_text, self)
        self.subtitle_label.setWordWrap(True)
        self.subtitle_label.setStyleSheet("font: 8pt Arial")
        self.subtitle_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.subtitle_label.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)

        # Author Label
        self.author_label = QLabel(author_text, self)
        self.author_label.setWordWrap(True)
        self.author_label.setStyleSheet("font: 12pt Arial")
        self.author_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.author_label.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)

        # Pages and Genre Labels on the same line
        self.pages_label = QLabel(f"Pages: {pages}", self)
        self.pages_label.setStyleSheet("font: 10pt Arial")
        self.pages_label.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.genre_label = QLabel(f"Genre: {genre}", self)
        self.genre_label.setStyleSheet("font: 10pt Arial")
        self.genre_label.setAlignment(Qt.AlignmentFlag.AlignLeft)

        # Create a horizontal layout for pages and genre
        self.pages_genre_layout = QHBoxLayout()
        self.pages_genre_layout.addWidget(self.pages_label)
        self.pages_genre_layout.addWidget(self.genre_label)
        self.pages_genre_layout.setContentsMargins(0, 0, 0, 0)
        self.pages_genre_layout.setSpacing(10)

        # Text Layout (for title, subtitle, author, and pages/genre)
        text_widget = QWidget(self)
        self.text_layout = QVBoxLayout(text_widget)
        self.text_layout.setContentsMargins(8, 8, 8, 8)
        self.text_layout.addWidget(self.title_label)
        self.text_layout.addWidget(self.subtitle_label)
        self.text_layout.addWidget(self.author_label)
        self.text_layout.addStretch()
        self.text_layout.addLayout(self.pages_genre_layout)


        # Main Layout (Image and Text)
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.addWidget(self.img_label)
        self.layout.addWidget(text_widget)
        self.layout.setAlignment(self.img_label, Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        self.layout.setAlignment(text_widget, Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        


        self.setLayout(self.layout)

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        self.clicked.emit(self.book)
        print(self.book.get_title())

    # Hover Effect
    def enterEvent(self, event):
        self.setStyleSheet("background-color: #e0e0e0;")  # Change background color on hover
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.setStyleSheet("background-color: transparent;")  # Revert to original background color
        super().leaveEvent(event)
