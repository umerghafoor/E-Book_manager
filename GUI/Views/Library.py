from GUI.Views.book_info import BookDetailsDialog
from Model.book import Book
from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QScrollArea, QGridLayout, QGroupBox, QPushButton, QLineEdit, QHBoxLayout, QSizePolicy, QDialog
from PyQt6.QtCore import Qt

from GUI.Views.card_book import CardWidget
from database.database_setup import BookDatabase

class LibraryView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.search_bucket = {}
        self.book_db = BookDatabase()
        self.initUI()
        self.add_boxes()

    def initUI(self):
        self.main_layout = QVBoxLayout()
        
        # Add Search bar
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search for books")
        self.search_bar.textChanged.connect(self.on_search_text_changed)
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

        # # Add a button to add boxes
        # self.button = QPushButton("Add Boxes")
        # self.button.clicked.connect(self.add_boxes)
        # self.main_layout.addWidget(self.button)
        
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
        # for i in range(10):
        #     box = CardWidget("default.png","Title of the Book","Author",self)
        #     self.books.append(box)

        # Load books from database
        new_books = self.book_db.get_all_books()
        print(new_books)

        self.books = []

        for book in new_books:
            book_id = book['id']
            book_title = book['title']
            book_subtitle   = book['subtitle']
            book_author = self.book_db.get_auther_by_id(book['author_id'])
            book_publisher = book['publisher']
            book_pub_date = book['pub_date']
            book_pages = book['pages']
            book_genre = book['genre']
            book_thumbnail = book['thumbnail']
            book_notes = book['notes']
            book_path = book['path']
            book_tags = self.book_db.get_tags_by_book_id(book['id'])

            book = Book(book_id, book_title, book_subtitle, book_author, book_publisher, book_pub_date, book_pages, book_genre, book_thumbnail, book_notes, book_path, book_tags)

            box = CardWidget(book, self)
            box.clicked.connect(lambda book=book: self.on_card_clicked(book))
            self.books.append(box)


        print("new boxes added")
        self.update_boxes()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if self.search_bar.text():
            self.on_search_text_changed(self.search_bar.text())
        else:
            self.update_boxes()

    def update_boxes(self):
        for i in reversed(range(self.grid_layout.count())): 
            self.grid_layout.itemAt(i).widget().setParent(None)
            
        width = self.scroll_area.viewport().width()
        print(f"Scroll Area Width: {width}")
        self.columns = max(1, width // (350+10))  # 150 for box width + 10 for spacing
        for i, box in enumerate(self.books):
            self.grid_layout.addWidget(box, i // self.columns, i % self.columns, Qt.AlignmentFlag.AlignTop)

    def on_search_text_changed(self, text):
        for i in reversed(range(self.grid_layout.count())): 
            self.grid_layout.itemAt(i).widget().setParent(None)
        print(f"Search text changed: {text}")
        width = self.scroll_area.viewport().width()
        self.columns = max(1, width // (350+10))  # 150 for box width + 10 for spacing
        i = 0
        for box in self.books:
            if text.lower() in box.book.get_title().lower() or text.lower() in box.book.get_author()[0].lower():
                self.grid_layout.addWidget(box, i // self.columns, i % self.columns, Qt.AlignmentFlag.AlignTop)
                i += 1
        for box in self.books:
            if text.lower() in box.book.get_subtitle().lower():
                self.grid_layout.addWidget(box, i // self.columns, i % self.columns, Qt.AlignmentFlag.AlignTop)
                i += 1

    def on_card_clicked(self, book):
        print(f"Clicked on book: {book.get_title()}")
        # Open book details dialog

        book_details_dialog = BookDetailsDialog(book = book, show_path=False)
        if book_details_dialog.exec() == QDialog.DialogCode.Accepted:
            book_details = book_details_dialog.get_details()
            get_tags_string = ", ".join(book_details['tags'])
            print(get_tags_string)

            self.book_db.connect()
            self.book_db.edit_book(
                book_id=book.get_id(),
                title=book_details['title'],
                subtitle=book_details['subtitle'],
                author=book_details['author_name'],
                publisher=book_details['publisher'],
                pub_date=book_details['pub_date'],
                pages=book_details['pages'],
                genre=book_details['genre'],
                path=book.get_path(),
                thumbnail=book_details['thumbnail'],
                notes=book_details['notes'],
                tags=get_tags_string
            )

            print(book_details)
            self.add_boxes()
