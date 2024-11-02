from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QScrollArea, QGridLayout, QGroupBox, QPushButton, QLineEdit, QHBoxLayout, QSizePolicy
from PyQt6.QtCore import Qt

from GUI.Views.card_book import CardWidget

class LibraryView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.search_bucket = {}
        self.initUI()

    def initUI(self):
        self.main_layout = QVBoxLayout()
        
        # Add Search bar
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search for books")
        self.main_layout.addWidget(self.search_bar)

        # Search features layout in horizontal layout
        self.search_features = QHBoxLayout()
        
        # Add search features to layout
        self.search_author = QPushButton("Author")
        self.search_genre = QPushButton("Genre")
        self.search_year = QPushButton("Year")
        self.search_pages_less = QPushButton("Pages <")
        self.search_pages_more = QPushButton("Pages >")
        self.search_tags = QPushButton("Tags")

        self.search_author.clicked.connect(lambda: self.on_search_features_click("author"))
        self.search_genre.clicked.connect(lambda: self.on_search_features_click("genre"))
        self.search_year.clicked.connect(lambda: self.on_search_features_click("year"))
        self.search_pages_less.clicked.connect(lambda: self.on_search_features_click("pages <"))
        self.search_pages_more.clicked.connect(lambda: self.on_search_features_click("pages >"))
        self.search_tags.clicked.connect(lambda: self.on_search_features_click("tags"))

        self.search_features.addWidget(self.search_author)
        self.search_features.addWidget(self.search_genre)
        self.search_features.addWidget(self.search_year)
        self.search_features.addWidget(self.search_pages_less)
        self.search_features.addWidget(self.search_pages_more)
        self.search_features.addWidget(self.search_tags)

        self.main_layout.addLayout(self.search_features)
        
        # Applied filter from search bucket
        self.applied_filter_layout = QGridLayout()
        self.applied_filter_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.main_layout.addLayout(self.applied_filter_layout)

        # Add a button to add boxes
        self.button = QPushButton("Add Boxes")
        self.button.clicked.connect(self.add_boxes)
        self.main_layout.addWidget(self.button)
        
        # Create a scroll area
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_content = QWidget()
        self.grid_layout = QGridLayout(self.scroll_content)
        self.scroll_area.setWidget(self.scroll_content)
        
        self.main_layout.addWidget(self.scroll_area)

        self.setLayout(self.main_layout)

        # Store added boxes to update on resize
        self.books = []

    def on_search_features_click(self, feature):
        text = self.search_bar.text() 
        if feature in ["pages <", "pages >", "year"] and not text.isdigit():
            self.search_bar.clear()
            return
        if text:
            self.search_bucket[feature] = text
            self.search_bar.clear()
            print(self.search_bucket)
            self.load_search_bucket()
    
    def load_search_bucket(self):
        for i in reversed(range(self.applied_filter_layout.count())): 
            self.applied_filter_layout.itemAt(i).widget().setParent(None)
        # add button for each key in search bucket in applied filter layout
        for i, key in enumerate(self.search_bucket.keys()):
            button = QPushButton(f"{key}: {self.search_bucket[key]}")
            # button size policy
            button.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
            button.clicked.connect(lambda: self.on_remove_filter_click(key))
            self.applied_filter_layout.addWidget(button, 0, i)

    def on_remove_filter_click(self, key):
        self.search_bucket.pop(key)
        print(self.search_bucket)
        self.load_search_bucket()

    def add_boxes(self):
        # Clear existing boxes
        for i in range(10):
            box = CardWidget("default.png","Title of the Book","Author",self)
            self.books.append(box)
        self.update_boxes()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.update_boxes()

    def update_boxes(self):
        width = self.scroll_area.viewport().width()
        self.columns = max(1, width // (250+10))  # 150 for box width + 10 for spacing
        for i, box in enumerate(self.books):
            self.grid_layout.addWidget(box, i // self.columns, i % self.columns, Qt.AlignmentFlag.AlignTop)
