from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QScrollArea, QGridLayout, QPushButton, QLineEdit, QSizePolicy, QHBoxLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap

from Views.card_book import CardWidget

class HomeView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.main_layout = QVBoxLayout(self)

        # Search bar
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search for books")
        self.main_layout.addWidget(self.search_bar)

        self.home_graphics = QHBoxLayout()

        # Add Text to graphics layout
        self.text = QLabel("Oragnize your books here")
        self.text.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.text.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        self.text.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        font = self.text.font()
        font.setPointSize(30)
        self.text.setFont(font)
        self.text.setWordWrap(True)
        self.home_graphics.addWidget(self.text)

        # Add image to graphics layout
        self.image = QLabel(self)
        pixmap = QPixmap("Screenshot.png")
        self.image.setPixmap(pixmap.scaled(400, 400, Qt.AspectRatioMode.KeepAspectRatio))
        self.image.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.home_graphics.addWidget(self.image)

        self.main_layout.addLayout(self.home_graphics)

        # Recent Books section
        self.add_section("Recent Books", self.add_recent_books)

        # My Queue section
        self.add_section("My Queue", self.add_my_queue)

        self.setLayout(self.main_layout)

    def add_section(self, title, add_func):
        label = QLabel(title)
        label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.main_layout.addWidget(label)

        scroll_area = self.create_scroll_area()
        scroll_area.setSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Fixed)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setMinimumHeight(150+8+8+8)
        self.main_layout.addWidget(scroll_area)

        button = QPushButton(f"Add {title}")
        button.clicked.connect(lambda: self.add_items(scroll_area, add_func))
        self.main_layout.addWidget(button)

    def create_scroll_area(self):
        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)
        scroll_content = QWidget()
        scroll_area.setWidget(scroll_content)
        scroll_area.grid_layout = QGridLayout(scroll_content)
        return scroll_area

    def add_recent_books(self, scroll_area):
        self.add_items(scroll_area, "Recent Books")

    def add_my_queue(self, scroll_area):
        self.add_items(scroll_area, "Queue books")

    def add_items(self, area, add_func):
        for i in range(10):
            book = CardWidget("default.png","Title of the Book","Author",self)
            area.grid_layout.addWidget(book, 0, i, Qt.AlignmentFlag.AlignTop)
