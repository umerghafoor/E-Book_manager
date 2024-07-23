from PyQt6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QPushButton, QFileDialog
)
from PyQt6.QtCore import Qt
import os


class SettingsView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Create main layout
        main_layout = QVBoxLayout()

        # Create "Load Book" button
        self.load_book_button = QPushButton("Load E-Book")
        self.load_book_folder_button = QPushButton("Load Folder")
        
        self.load_book_button.clicked.connect(self.load_book)
        self.load_book_folder_button.clicked.connect(self.load_folder)


        main_layout.addWidget(self.load_book_button, alignment=Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.load_book_folder_button, alignment=Qt.AlignmentFlag.AlignCenter)


        # Create About section
        about_label = QLabel("<h2>About</h2>"
                             "<p>Welcome to eBook Manager, your ultimate tool for organizing and enjoying your digital library! Our mission is to provide a seamless and intuitive solution for managing your eBook collection, making it easier for you to access and enjoy your favorite reads.</p>"
                             "<p>Version 1.0.0</p>")
        about_label.setWordWrap(True)
        about_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(about_label)

        # Set the layout for the widget
        self.setLayout(main_layout)

    def load_book(self):
        # Open dialog to select a file or folder
        path = QFileDialog.getOpenFileName(self, "Select File or Folder", "", "All Files (*)")[0]

        if path:
            print(f"Selected File: {path}")
        else:
            print("No selection made.")

    def load_folder(self):
        # Open dialog to select a folder
        folder_path = QFileDialog.getExistingDirectory(self, "Select Folder")
        
        if folder_path:
            print(f"Selected Folder: {folder_path}")
        else:
            print("No folder selected.")
