import os
from PyQt6.QtCore import QUrl
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QWidget, QLabel, QLineEdit, QDialog, QFileDialog, QComboBox, QListWidget, QListWidgetItem
from PyQt6.QtGui import QColor


class RenameFileDialog(QDialog):
    def __init__(self, old_filename, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Rename E-book")
        self.setModal(True)

        self.layout = QVBoxLayout(self)

        self.old_filename_label = QLabel("Old Name:")
        self.old_filename_input = QLineEdit(old_filename)

        self.new_name_label = QLabel("New Name:")
        self.new_name_input = QLineEdit(old_filename)

        self.new_author_label = QLabel("New Author:")
        self.new_author_input = QLineEdit()

        self.new_genre_label = QLabel("New Genre:")
        self.new_genre_combo = QComboBox()

        self.new_genre_combo.addItem("Art & Design")
        self.new_genre_combo.addItem("Biography")
        self.new_genre_combo.addItem("Engineering")
        self.new_genre_combo.addItem("History")
        self.new_genre_combo.addItem("Novels")
        self.new_genre_combo.addItem("Papers")
        self.new_genre_combo.addItem("Biography")
        self.new_genre_combo.addItem("Poetry")
        self.new_genre_combo.addItem("Religious")
        self.new_genre_combo.addItem("Science")
        self.new_genre_combo.addItem("Self Motivation")
        self.new_genre_combo.addItem("Other")


        self.new_pages_label = QLabel("New Pages:")
        self.new_pages_input = QLineEdit()

        self.rename_button = QPushButton("Rename")
        self.rename_button.clicked.connect(self.accept)

        self.layout.addWidget(self.old_filename_label)
        self.layout.addWidget(self.old_filename_input)
        self.layout.addWidget(self.new_name_label)
        self.layout.addWidget(self.new_name_input)
        self.layout.addWidget(self.new_author_label)
        self.layout.addWidget(self.new_author_input)
        self.layout.addWidget(self.new_genre_label)
        self.layout.addWidget(self.new_genre_combo)
        self.layout.addWidget(self.new_pages_label)
        self.layout.addWidget(self.new_pages_input)
        self.layout.addWidget(self.rename_button)



class FileRenamerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.ebook_list = []

    def init_ui(self):
        self.setGeometry(100, 100, 400, 300)
        self.setWindowTitle("File Renamer")

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        self.rename_button = QPushButton("Add E-books")
        self.rename_button.clicked.connect(self.add_ebooks)
        self.layout.addWidget(self.rename_button)

        self.ebook_list_widget = QListWidget()
        self.layout.addWidget(self.ebook_list_widget)

        self.rename_selected_button = QPushButton("Rename Selected E-book")
        self.rename_selected_button.clicked.connect(self.rename_selected_ebook)
        self.layout.addWidget(self.rename_selected_button)

    def add_ebooks(self):
        folder_path = QFileDialog.getExistingDirectory(self, "Select Folder Containing E-books", options=QFileDialog.Option.ShowDirsOnly)
        if folder_path:
            for root, dirs, files in os.walk(folder_path):
                for file in files:
                    if file.endswith(".pdf") or file.endswith(".epub"):
                        self.ebook_list.append(os.path.join(root, file))
                        item = QListWidgetItem(file)
                        if not self.is_valid_naming_convention(file):
                            item.setForeground(QColor("red"))
                        self.ebook_list_widget.addItem(item)

    def rename_selected_ebook(self):
        selected_item = self.ebook_list_widget.currentItem()
        if selected_item:
            selected_index = self.ebook_list_widget.currentRow()
            old_file_path = self.ebook_list[selected_index]

            if self.is_valid_naming_convention(selected_item.text()):
                # If the naming convention is correct, extract name, author, genre, and pages from the filename
                parts = selected_item.text().split('+')
                new_name, new_author, new_genre, new_pages_ext = parts
                new_pages, _ = os.path.splitext(new_pages_ext)
            else:
                new_name = ""
                new_author = ""
                new_genre = "Other"
                new_pages = ""

            dialog = RenameFileDialog(os.path.basename(old_file_path))
            dialog.new_name_input.setText(new_name)
            dialog.new_author_input.setText(new_author)
            dialog.new_genre_combo.setCurrentText(new_genre)
            dialog.new_pages_input.setText(new_pages)

            if dialog.exec() == QDialog.DialogCode.Accepted:
                new_name = dialog.new_name_input.text()
                new_author = dialog.new_author_input.text()
                new_genre = dialog.new_genre_combo.currentText()
                new_pages = dialog.new_pages_input.text()

                new_filename = f"{new_name}+{new_author}+{new_genre}+{new_pages}.pdf"  
                new_file_path = os.path.join(os.path.dirname(old_file_path), new_filename)

                os.rename(old_file_path, new_file_path)
                self.ebook_list[selected_index] = new_file_path
                selected_item.setText(new_filename)
                if not self.is_valid_naming_convention(new_filename):
                    selected_item.setForeground(QColor("red"))
                else:
                    selected_item.setForeground(QColor("black"))

    def is_valid_naming_convention(self, filename):
        # Check if the filename follows the format: bookname+author+genre+pages.pdf
        parts = filename.split('+')
        if len(parts) == 4:
            bookname, author, genre, pages_ext = parts
            pages, extension = os.path.splitext(pages_ext)
            if extension == '.pdf':
                return True
        return False

def main():
    app = QApplication([])
    window = FileRenamerApp()
    window.show()
    app.exec()

if __name__ == '__main__':
    main()