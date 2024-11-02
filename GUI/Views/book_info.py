from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout, QLabel, QLineEdit, QPushButton, QDateEdit, 
    QSpinBox, QDialogButtonBox, QFileDialog
)
from PyQt6.QtCore import QDate

class BookDetailsDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Enter Book Details")
        
        layout = QVBoxLayout()
        form_layout = QFormLayout()
        
        self.title_input = QLineEdit()
        form_layout.addRow(QLabel("Title:"), self.title_input)
        
        self.subtitle_input = QLineEdit()
        form_layout.addRow(QLabel("Subtitle:"), self.subtitle_input)
        
        self.author_input = QLineEdit()
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
        return {
            "title": self.title_input.text(),
            "subtitle": self.subtitle_input.text(),
            "author_name": self.author_input.text(),
            "publisher": self.publisher_input.text(),
            "pub_date": self.pub_date_input.date().toString("yyyy-MM-dd"),
            "pages": self.page_count_input.value(),
            "genre": self.genre_input.text(),
            "path": self.path_input.text(),
            "thumbnail": self.thumbnail_input.text(),
            "notes": self.notes_input.text(),
            "tags": self.tags_input.text()
        }
