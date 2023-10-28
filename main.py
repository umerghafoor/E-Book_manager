import os
import sys
from PyQt6.QtCore import QUrl
from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog, QTableWidget, QTableWidgetItem, QVBoxLayout, QPushButton, QWidget, QLabel, QLineEdit, QDialog, QVBoxLayout, QHBoxLayout, QSpinBox
from PyQt6.QtGui import QDesktopServices
import configparser

class RenameDialog(QDialog):
    def __init__(self, old_title, old_author, old_genre, old_page_count, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Rename E-book")
        self.setModal(True)

        self.layout = QVBoxLayout(self)

        self.old_title_label = QLabel(f"Old Title: {old_title}")
        self.new_title_label = QLabel("New Title:")
        self.new_title_input = QLineEdit(old_title)
        self.old_author_label = QLabel(f"Old Author: {old_author}")
        self.new_author_label = QLabel("New Author:")
        self.new_author_input = QLineEdit(old_author)
        self.old_genre_label = QLabel(f"Old Genre: {old_genre}")
        self.new_genre_label = QLabel("New Genre:")
        self.new_genre_input = QLineEdit(old_genre)
        self.old_page_count_label = QLabel(f"Old Page Count: {old_page_count}")
        self.new_page_count_label = QLabel("New Page Count:")
        self.new_page_count_input = QSpinBox()
        self.new_page_count_input.setMinimum(1)
        self.new_page_count_input.setMaximum(10000)
        self.new_page_count_input.setValue(int(old_page_count))  # Convert old_page_count to an integer

        self.rename_button = QPushButton("Rename")
        self.rename_button.clicked.connect(self.accept)

        self.layout.addWidget(self.old_title_label)
        self.layout.addWidget(self.new_title_label)
        self.layout.addWidget(self.new_title_input)
        self.layout.addWidget(self.old_author_label)
        self.layout.addWidget(self.new_author_label)
        self.layout.addWidget(self.new_author_input)
        self.layout.addWidget(self.old_genre_label)
        self.layout.addWidget(self.new_genre_label)
        self.layout.addWidget(self.new_genre_input)
        self.layout.addWidget(self.old_page_count_label)
        self.layout.addWidget(self.new_page_count_label)
        self.layout.addWidget(self.new_page_count_input)
        self.layout.addWidget(self.rename_button)

class EbookManagerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.load_last_path()

    def init_ui(self):
        self.setGeometry(100, 100, 800, 400)
        self.setWindowTitle("E-book Manager")

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        

        self.layout = QVBoxLayout(self.central_widget)

        self.ebook_table = QTableWidget()
        self.ebook_table.cellDoubleClicked.connect(self.open_ebook)
        self.ebook_table.setColumnCount(5)
        self.ebook_table.setHorizontalHeaderLabels(['Title', 'Author', 'Genre', 'Page Count', 'File Path'])
        self.layout.addWidget(self.ebook_table)

        self.load_button = QPushButton("Load E-books")
        self.load_button.clicked.connect(self.load_ebooks)
        self.layout.addWidget(self.load_button)

        self.rename_button = QPushButton("Rename E-book")
        self.rename_button.clicked.connect(self.show_rename_dialog)
        self.layout.addWidget(self.rename_button)

        self.open_button = QPushButton("Open E-book")
        self.open_button.clicked.connect(self.open_ebook)
        self.layout.addWidget(self.open_button)

    def load_last_path(self):
        config = configparser.ConfigParser()
        config.read('config.ini')
        if 'Paths' in config and 'last_path' in config['Paths']:
            last_path = config['Paths']['last_path']
            if os.path.isdir(last_path):
                self.ebooks = self.scan_folder_for_ebooks(last_path)
                self.update_ebook_table()

    def save_last_path(self, path):
        config = configparser.ConfigParser()
        config['Paths'] = {'last_path': path}
        with open('config.ini', 'w') as configfile:
            config.write(configfile)

    def load_ebooks(self):
        folder_path = QFileDialog.getExistingDirectory(self, "Select Folder Containing E-books", options=QFileDialog.Option.ShowDirsOnly)
        if folder_path:
            self.save_last_path(folder_path)
            self.ebooks = self.scan_folder_for_ebooks(folder_path)
            self.update_ebook_table()

    def scan_folder_for_ebooks(self, folder_path):
        ebook_list = []
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                if file.endswith(".pdf") or file.endswith(".epub"):
                    title, author, genre, page_count = self.extract_metadata_from_filename(file)
                    file_path = os.path.join(root, file)
                    ebook_list.append({"title": title, "author": author, "genre": genre, "page_count": page_count, "file_path": file_path})
        return ebook_list

    def update_ebook_table(self):
        self.ebook_table.setRowCount(len(self.ebooks))
        for row, ebook in enumerate(self.ebooks):
            for col, field in enumerate(['title', 'author', 'genre', 'page_count', 'file_path']):
                item = QTableWidgetItem(ebook[field])
                self.ebook_table.setItem(row, col, item)

    def show_rename_dialog(self):
        selected_row = self.ebook_table.currentRow()
        if selected_row != -1:
            ebook = self.ebooks[selected_row]
            old_title = ebook['title']
            old_author = ebook['author']
            old_genre = ebook['genre']
            old_page_count = ebook['page_count']

            dialog = RenameDialog(old_title, old_author, old_genre, old_page_count)
            if dialog.exec() == QDialog.DialogCode.Accepted:
                new_title = dialog.new_title_input.text()
                new_author = dialog.new_author_input.text()
                new_genre = dialog.new_genre_input.text()
                new_page_count = dialog.new_page_count_input.value()

                old_file_path = ebook['file_path']
                file_extension = os.path.splitext(old_file_path)[1]
                new_file_name = f"{new_title}+{new_author}+{new_genre}+{new_page_count}{file_extension}"
                new_file_path = os.path.join(os.path.dirname(old_file_path), new_file_name)

                os.rename(old_file_path, new_file_path)
                self.ebooks[selected_row]['title'] = new_title
                self.ebooks[selected_row]['author'] = new_author
                self.ebooks[selected_row]['genre'] = new_genre
                self.ebooks[selected_row]['page_count'] = new_page_count
                self.ebooks[selected_row]['file_path'] = new_file_path
                self.load_last_path()

    def open_ebook(self):
        selected_row = self.ebook_table.currentRow()
        if selected_row != -1:
            file_path = self.ebooks[selected_row]['file_path']
            QDesktopServices.openUrl(QUrl.fromLocalFile(file_path))

    def extract_metadata_from_filename(self, filename):
        filename_without_extension = os.path.splitext(filename)[0]
        parts = filename_without_extension.split('+')
        if len(parts) == 4:
            title, author, genre, page_count = parts
        else:
            title = author = genre = "Unknown"
            page_count = "1"  # Default page count
        return title, author, genre, page_count

def main():
    app = QApplication(sys.argv)
    window = EbookManagerApp()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
