from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout, QLabel, QLineEdit, QPushButton, QDateEdit, 
    QSpinBox, QDialogButtonBox, QFileDialog, QHBoxLayout
)
from PyQt6.QtCore import QDate
import os
import subprocess
import platform

class BookDetailsDialog(QDialog):

    def __init__(self, file_path=None, book=None, show_path=True):
        super().__init__()

        self.show_path = show_path
        self.init_UI_()

        if file_path:
            # Separate book name from the path
            file_name = file_path.split("\\")[-1]
            self.title_input.setText(file_name.split("+")[0])
            if len(file_name.split("+")) > 1:
                self.author_input.setText(file_name.split("+")[1])
                self.publisher_input.setText(file_name.split("+")[2])
                self.page_count_input.setValue(int(file_name.split("+")[3].split(".")[0]))
            else:
                self.author_input.setText("Unknown")
                self.publisher_input.setText("Unknown")
                self.page_count_input.setValue(0)
            self.book_path = file_path

        elif book:
            self.title_input.setText(book.get_title())
            self.subtitle_input.setText(book.get_subtitle())
            # if isinstance(book.get_author(), tuple):
            #     for author in book.get_author():
            #         self.author_input_1.setText(author)
            print(book.get_author())
            self.author_input.setText(book.get_author()[0])
            self.publisher_input.setText(book.get_publisher())
            self.pub_date_input.setDate(QDate.fromString(book.get_pub_date(), "yyyy-MM-dd"))
            self.page_count_input.setValue(book.get_pages())
            self.genre_input.setText(book.get_genre())
            self.thumbnail_input.setText(book.get_thumbnail())
            self.notes_input.setText(book.get_notes())
            if isinstance(book.get_tags(), list):
                tags = book.get_tags()[0]
                self.tags_input.setText(", ".join(tags))
            self.book_path = book.get_path()

    def init_UI_(self):
        self.setWindowTitle("Enter Book Details")
        
        layout = QVBoxLayout()
        form_layout = QFormLayout()
        
        self.title_input = QLineEdit()
        form_layout.addRow(QLabel("Title:"), self.title_input)
        
        self.subtitle_input = QLineEdit()
        form_layout.addRow(QLabel("Subtitle:"), self.subtitle_input)
        
        # self.author_input = QHBoxLayout()
        # self.add_author_button = QPushButton("+")
        # self.add_author_button.clicked.connect(self.add_author)
        self.author_input = QLineEdit()
        # self.author_input.addWidget(self.author_input_1)
        form_layout.addRow(QLabel("Author:"), self.author_input)
        
        self.publisher_input = QLineEdit()
        form_layout.addRow(QLabel("Publisher:"), self.publisher_input)
        
        self.pub_date_input = QDateEdit()
        self.pub_date_input.setCalendarPopup(True)
        self.pub_date_input.setDate(QDate.currentDate())
        form_layout.addRow(QLabel("Publication Date:"), self.pub_date_input)
        
        self.page_count_input = QSpinBox()
        self.page_count_input.setRange(1, 10000)
        form_layout.addRow(QLabel("Pages:"), self.page_count_input)
        
        self.genre_input = QLineEdit()
        form_layout.addRow(QLabel("Genre:"), self.genre_input)
        
        if self.show_path:
            self.path_input = QLineEdit()
            self.path_button = QPushButton("Select File")
            self.path_button.clicked.connect(self.select_file)
            form_layout.addRow(QLabel("File Path:"), self.path_input)
            form_layout.addWidget(self.path_button)
            
        self.thumbnail_input = QLineEdit()
        self.thumbnail_button = QPushButton("Select Thumbnail")
        self.thumbnail_button.clicked.connect(self.select_thumbnail)
        form_layout.addRow(QLabel("Thumbnail:"), self.thumbnail_input)
        form_layout.addWidget(self.thumbnail_button)
        
        self.notes_input = QLineEdit()
        form_layout.addRow(QLabel("Notes:"), self.notes_input)
        
        self.tags_input = QLineEdit()
        form_layout.addRow(QLabel("Tags:"), self.tags_input)
        
        # Open button to open the PDF
        self.open_button = QPushButton("Open")
        self.open_button.clicked.connect(self.open_pdf)
        form_layout.addWidget(self.open_button)

        self.dialog_buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Save | QDialogButtonBox.StandardButton.Cancel)
        self.dialog_buttons.accepted.connect(self.accept)
        self.dialog_buttons.rejected.connect(self.reject)
        
        layout.addLayout(form_layout)
        layout.addWidget(self.dialog_buttons)
        self.setLayout(layout)

    def select_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Book File", "", "PDF Files (*.pdf);;All Files (*)")
        if file_path:
            self.path_input.setText(file_path)

    def select_thumbnail(self):
        thumbnail_path, _ = QFileDialog.getOpenFileName(self, "Select Thumbnail", "", "Image Files (*.jpg *.png);;All Files (*)")
        if thumbnail_path:
            self.thumbnail_input.setText(thumbnail_path)

    def get_details(self):
        """Return all entered details as a dictionary."""
        # authors = []
        # for i in range(self.author_input.count() - 1):
        #     authors.append(self.author_input.itemAt(i).widget().text())

        # tags = self.tags_input.text().split(", ")
        
        return {
            "title": self.title_input.text(),
            "subtitle": self.subtitle_input.text(),
            "author_name": self.author_input.text(),
            "publisher": self.publisher_input.text(),
            "pub_date": self.pub_date_input.date().toString("yyyy-MM-dd"),
            "pages": self.page_count_input.value(),
            "genre": self.genre_input.text(),
            "path": self.book_path,
            "thumbnail": self.thumbnail_input.text(),
            "notes": self.notes_input.text(),
            "tags": self.tags_input.text()
        }

    def add_author(self):
        new_author_input = QLineEdit()
        self.author_input.insertWidget(self.author_input.count() - 1, new_author_input)

    def open_pdf(self):
        if self.book_path and os.path.exists(self.book_path):
            if platform.system() == "Windows":
                os.startfile(self.book_path)  # Windows
            elif platform.system() == "Darwin":
                subprocess.run(["open", self.book_path])  # macOS
            else:
                subprocess.run(["xdg-open", self.book_path])  # Linux
        else:
            print("No valid file path provided.")

        # cancel the dialog
        self.reject()