import os
import sys
from PyQt6.QtCore import QUrl
from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog, QTableWidget, QTableWidgetItem, QVBoxLayout, QPushButton, QWidget, QLabel, QLineEdit
from PyQt6.QtGui import QDesktopServices

class EbookManagerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setGeometry(100, 100, 800, 400)
        self.setWindowTitle("E-book Manager")

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        self.ebook_table = QTableWidget()
        self.ebook_table.setColumnCount(4)
        self.ebook_table.setHorizontalHeaderLabels(['Title', 'Author', 'Genre', 'File Path'])
        self.layout.addWidget(self.ebook_table)

        self.load_button = QPushButton("Load E-books")
        self.load_button.clicked.connect(self.load_ebooks)
        self.layout.addWidget(self.load_button)

        self.rename_label = QLabel("New Title:")
        self.rename_input = QLineEdit()
        self.rename_button = QPushButton("Rename E-book")
        self.rename_button.clicked.connect(self.rename_ebook)
        self.layout.addWidget(self.rename_label)
        self.layout.addWidget(self.rename_input)
        self.layout.addWidget(self.rename_button)

        self.open_button = QPushButton("Open E-book")
        self.open_button.clicked.connect(self.open_ebook)
        self.layout.addWidget(self.open_button)

    def load_ebooks(self):
        folder_path = QFileDialog.getExistingDirectory(self, "Select Folder Containing E-books")
        if folder_path:
            self.ebooks = self.scan_folder_for_ebooks(folder_path)
            self.update_ebook_table()

    def scan_folder_for_ebooks(self, folder_path):
        ebook_list = []
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                if file.endswith(".pdf") or file.endswith(".epub"):
                    title = os.path.splitext(file)[0]
                    author = "Unknown"  # You can modify this to extract author information from the e-book file.
                    file_path = os.path.join(root, file)
                    genre = "Unknown"  # You can specify the genre or leave it as "Unknown."
                    ebook_list.append({"title": title, "author": author, "file_path": file_path, "genre": genre})
        return ebook_list

    def update_ebook_table(self):
        self.ebook_table.setRowCount(len(self.ebooks))
        for row, ebook in enumerate(self.ebooks):
            for col, field in enumerate(['title', 'author', 'genre', 'file_path']):
                item = QTableWidgetItem(ebook[field])
                self.ebook_table.setItem(row, col, item)

    def rename_ebook(self):
        selected_row = self.ebook_table.currentRow()
        if selected_row != -1:
            new_title = self.rename_input.text()
            old_file_path = self.ebooks[selected_row]['file_path']
            file_extension = os.path.splitext(old_file_path)[1]
            new_file_path = os.path.join(os.path.dirname(old_file_path), new_title + file_extension)

            os.rename(old_file_path, new_file_path)
            self.ebooks[selected_row]['title'] = new_title
            self.ebooks[selected_row]['file_path'] = new_file_path
            self.update_ebook_table()


    def open_ebook(self):
        selected_row = self.ebook_table.currentRow()
        if selected_row != -1:
            file_path = self.ebooks[selected_row]['file_path']
            QDesktopServices.openUrl(QUrl.fromLocalFile(file_path))

def main():
    app = QApplication(sys.argv)
    window = EbookManagerApp()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
