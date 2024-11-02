from PyQt6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QPushButton, QFileDialog, QDialog
)
from PyQt6.QtCore import Qt
from database.database_setup import BookDatabase
from GUI.Views.book_info import BookDetailsDialog
import os

class SettingsView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        main_layout = QVBoxLayout()

        self.load_book_button = QPushButton("Load E-Book")
        self.load_book_folder_button = QPushButton("Load Folder")
        
        self.load_book_button.clicked.connect(self.load_book)
        self.load_book_folder_button.clicked.connect(self.load_folder)

        main_layout.addWidget(self.load_book_button, alignment=Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.load_book_folder_button, alignment=Qt.AlignmentFlag.AlignCenter)

        about_label = QLabel("<h2>About</h2>"
                             "<p>Welcome to eBook Manager, your ultimate tool for organizing and enjoying your digital library! Our mission is to provide a seamless and intuitive solution for managing your eBook collection, making it easier for you to access and enjoy your favorite reads.</p>"
                             "<p>Version 1.0.0</p>")
        about_label.setWordWrap(True)
        about_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(about_label)

        self.setLayout(main_layout)

    def load_book(self):
        path = QFileDialog.getOpenFileName(self, "Select E-Book", "", "PDF Files (*.pdf);;All Files (*)")[0]

        if path:
            print(f"Selected File: {path}")
            details_dialog = BookDetailsDialog()
            if details_dialog.exec() == QDialog.DialogCode.Accepted:
                book_details = details_dialog.get_details()
                BookDatabase().create_database()
                BookDatabase().add_book(
                title=book_details['title'],
                subtitle=book_details['subtitle'],
                author_name=book_details['author_name'],
                publisher=book_details['publisher'],
                pub_date=book_details['pub_date'],
                pages=book_details['pages'],
                genre=book_details['genre'],
                path=path,
                thumbnail=book_details['thumbnail'],
                notes=book_details['notes'],
                tags=book_details['tags']
                )
                print(book_details)
        else:
            print("No selection made.")


    def load_folder(self):
        # Open dialog to select a folder
        folder_path = QFileDialog.getExistingDirectory(self, "Select Folder")
        
        if folder_path:
            print(f"Selected Folder: {folder_path}")
            
            for filename in os.listdir(folder_path):
                if filename.lower().endswith('.pdf'):
                    file_path = os.path.join(folder_path, filename)
                    print(f"Found PDF: {file_path}")
                    
                    details_dialog = BookDetailsDialog()
                    if details_dialog.exec() == QDialog.DialogCode.Accepted:
                        book_details = details_dialog.get_details()
                        BookDatabase().create_database()
                        BookDatabase().add_book(
                            title=book_details['title'],
                            subtitle=book_details['subtitle'],
                            author_name=book_details['author_name'],
                            publisher=book_details['publisher'],
                            pub_date=book_details['pub_date'],
                            pages=book_details['pages'],
                            genre=book_details['genre'],
                            path=file_path,
                            thumbnail=book_details['thumbnail'],
                            notes=book_details['notes'],
                            tags=book_details['tags']
                        )
                        print(f"Added book: {book_details['title']} by {book_details['author_name']}")
                else:
                    print(f"Skipping non-PDF file: {filename}")
        else:
            print("No folder selected.")
            folder_path = QFileDialog.getExistingDirectory(self, "Select Folder")
            
            if folder_path:
                print(f"Selected Folder: {folder_path}")
                
                for filename in os.listdir(folder_path):
                    if filename.endswith('.pdf'):
                        file_path = os.path.join(folder_path, filename)
                        print(f"Found PDF: {file_path}")
                        
                        details_dialog = BookDetailsDialog()
                        if details_dialog.exec() == QDialog.DialogCode.Accepted:
                            book_details = details_dialog.get_details()
                            BookDatabase().create_database()
                            BookDatabase().add_book(
                                title=book_details['title'],
                                subtitle=book_details['subtitle'],
                                author_name=book_details['author_name'],
                                publisher=book_details['publisher'],
                                pub_date=book_details['pub_date'],
                                pages=book_details['pages'],
                                genre=book_details['genre'],
                                path=file_path,
                                thumbnail=book_details['thumbnail'],
                                notes=book_details['notes'],
                                tags=book_details['tags']
                            )
                            print(book_details)
                    else:
                        print(f"Skipping non-PDF file: {filename}")
            else:
                print("No folder selected.")
