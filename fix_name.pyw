import os
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QPushButton, QWidget, QLabel, QLineEdit,
    QDialog, QFileDialog, QComboBox, QListWidget, QListWidgetItem
)
from PyQt6.QtGui import QColor
from PIL import Image, ImageOps, ImageDraw
import shutil


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
        self.new_genre_combo.addItem("Poetry")
        self.new_genre_combo.addItem("Religious")
        self.new_genre_combo.addItem("Science")
        self.new_genre_combo.addItem("Self Motivation")
        self.new_genre_combo.addItem("Other")


        self.new_pages_label = QLabel("New Pages:")
        self.new_pages_input = QLineEdit()

        self.rename_button = QPushButton("Rename")
        self.rename_button.clicked.connect(self.accept)

        self.image_path_label = QLabel("Image Path:")
        self.image_path_input = QLineEdit()
        self.image_path_button = QPushButton("Browse Image")
        self.image_path_button.clicked.connect(self.select_image)

        self.paste_image_button = QPushButton("Paste from Clipboard")
        self.paste_image_button.clicked.connect(self.paste_image)

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
        self.layout.addWidget(self.image_path_label)
        self.layout.addWidget(self.image_path_input)
        self.layout.addWidget(self.image_path_button)
        self.layout.addWidget(self.paste_image_button)
        self.layout.addWidget(self.rename_button)

    
    def select_image(self):
        image_path, _ = QFileDialog.getOpenFileName(self, "Select Image File", filter="Image Files (*.png)")
        if image_path:
            self.image_path_input.setText(image_path)

    def paste_image(self):
        clipboard = QApplication.clipboard()
        image = clipboard.image()
        if not image.isNull():
            # Save the image to a temporary file and set the file path
            temp_image_path = "temp_image.png"
            image.save(temp_image_path, "PNG")

            # Crop the image to rounded edges
            self.crop_to_a4_ratio(temp_image_path)
            self.image_path_input.setText(temp_image_path)
        else:
            self.image_path_input.setText("default.png")

    def crop_to_a4_ratio(self, image_path):
        with Image.open(image_path) as img:
            img_width, img_height = img.size
            img_aspect_ratio = img_width / img_height
            if img_aspect_ratio < 1.41:
                new_width = img_height / 1.41
                crop_width = new_width
                crop_height = img_height
            else:
                new_height = img_width * 1.41
                crop_width = img_width
                crop_height = new_height


            mask = Image.new("L", (int(crop_width), int(crop_height)), 0)
            draw = ImageDraw.Draw(mask)
            draw.rounded_rectangle((0, 0, crop_width, crop_height), radius=80, fill=255)

            result = ImageOps.fit(img, (int(crop_width), int(crop_height)), centering=(0.5, 0.5))
            result.putalpha(mask)

            result.save(image_path)



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

        self.ebook_list_widget.itemDoubleClicked.connect(self.rename_selected_ebook)
        # self.ebook_list_widget.itemClicked.connect(self.open_ebook)
        self.load_stylesheet("fix_name.css")

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
                image_path = dialog.image_path_input.text()

                new_filename = f"{new_name}+{new_author}+{new_genre}+{new_pages}.pdf"
                new_file_path = os.path.join(os.path.dirname(old_file_path), new_filename)

                os.rename(old_file_path, new_file_path)
                self.ebook_list[selected_index] = new_file_path
                selected_item.setText(new_filename)
                if not self.is_valid_naming_convention(new_filename):
                    selected_item.setForeground(QColor("red"))
                else:
                    selected_item.setForeground(QColor("black"))

                # Handle image file
                if image_path:
                    image_filename = f"{new_name}+{new_author}+{new_genre}+{new_pages}.png" 
                    image_file_path = os.path.join(os.path.dirname(old_file_path), image_filename)

                    # Copy the selected image file to the e-book directory
                    shutil.copy(image_path, image_file_path)

    def is_valid_naming_convention(self, filename):
        # Check if the filename follows the format: bookname+author+genre+pages.pdf
        parts = filename.split('+')
        if len(parts) == 4:
            bookname, author, genre, pages_ext = parts
            pages, extension = os.path.splitext(pages_ext)
            if extension == '.pdf':
                return True
        return False
    
    def open_ebook(self, item):
        selected_index = self.ebook_list_widget.row(item)
        if selected_index >= 0 and selected_index < len(self.ebook_list):
            selected_ebook = self.ebook_list[selected_index]
            os.system(f'"{selected_ebook}"')
    
    def load_stylesheet(self, stylesheet_file):
        # Load and apply the style sheet from the file
        with open(stylesheet_file, "r") as file:
            self.setStyleSheet(file.read())

def main():
    app = QApplication([])
    window = FileRenamerApp()
    window.show()
    app.exec()

if __name__ == '__main__':
    main()