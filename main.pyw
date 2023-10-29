import os
import sys
from PyQt6.QtCore import QUrl,Qt
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QFileDialog, QVBoxLayout, QPushButton, QWidget, QLabel,QFrame,
    QLineEdit, QDialog, QHBoxLayout, QSpinBox, QComboBox, QGridLayout, QScrollArea, QSizePolicy, QButtonGroup,
)
from PyQt6.QtGui import QPixmap
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
        self.old_page_count_label = QLabel(f"Old Page Count: {old_page_count}")
        self.new_page_count_label = QLabel("New Page Count:")
        self.new_page_count_input = QSpinBox()
        self.new_page_count_input.setMinimum(1)
        self.new_page_count_input.setMaximum(10000)
        self.new_page_count_input.setValue(int(old_page_count))

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
        self.layout.addWidget(self.new_genre_combo)
        self.layout.addWidget(self.old_page_count_label)
        self.layout.addWidget(self.new_page_count_label)
        self.layout.addWidget(self.new_page_count_input)
        self.layout.addWidget(self.rename_button)

class EbookCard(QFrame):  # Use QFrame as the outer container
    def __init__(self, title, author, genre, page_count, file_path, image_path, parent=None, app=None, ebook=None, grid_layout=None):
        super().__init__(parent)
        self.app = app  # Store a reference to the main application
        self.file_path = file_path
        self.image_path = image_path
        self.title = title
        self.author = author
        self.genre = genre
        self.page_count = page_count
        self.ebook = ebook
        self.grid_layout = grid_layout  # Store a reference to the grid layout

        self.layout = QVBoxLayout(self)

        title_label = QLabel(f"{title}")
        title_label.setWordWrap(True)

        self.image_label = QLabel()  # Create a QLabel for displaying the image
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Center align the image
        self.layout.addWidget(self.image_label)
        self.layout.addWidget(title_label)
        self.layout.addWidget(QLabel(f"Author : {author}"))
        self.layout.addWidget(QLabel(f"Genre: {genre}"))
        self.layout.addWidget(QLabel(f"Pages: {page_count}"))

        # Initialize pixmap to None
        self.pixmap = None
        self.magnified = None

        self.load_image(image_path)  # Load the image during initialization

        
        self.setFixedSize(150, 400)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        
        # "Rename" button
        self.rename_button = QPushButton("Rename")
        self.rename_button.clicked.connect(self.show_rename_dialog)
        self.layout.addWidget(self.rename_button)

        self.setStyleSheet("QFrame { border: 0px solid #000; border-radius: 20px;}")

    def enterEvent(self, event):
        if not self.magnified:
            self.magnified = True
            self.image_label.setPixmap(self.magnified_pixmap)
            self.setFixedSize(155, 400)
            self.setStyleSheet("QFrame { border: 0px solid #000; border-radius: 20px; background-color: blue;  }")

    def leaveEvent(self, event):
        if self.magnified:
            self.magnified = False
            self.image_label.setPixmap(self.pixmap)
            self.setFixedSize(150, 400)
            self.setStyleSheet("")

    def mouseDoubleClickEvent(self, event):
        self.open_ebook()
    
    def mousePressEvent(self, event):
        self.app.update_preview_card(self.title, self.image_path,self.ebook)
        print("mousePressEvent")
        #self.open_ebook()

    def load_image(self, image_path):
        if os.path.exists(image_path):
            self.pixmap = QPixmap(image_path)
        else:
            # Load a default image if the image path is not valid
            self.pixmap = QPixmap("default.png")
        fixed_width = 150
        fixed_height = 250
        if not self.pixmap.isNull():
            self.pixmap = self.pixmap.scaled(fixed_width, fixed_height, aspectRatioMode=Qt.AspectRatioMode.KeepAspectRatio)
            self.image_label.setPixmap(self.pixmap)
            self.magnified_pixmap = self.pixmap.scaled(155, 200, aspectRatioMode=Qt.AspectRatioMode.KeepAspectRatio)

    def open_ebook(self):
        print(self.file_path)
        QDesktopServices.openUrl(QUrl.fromLocalFile(self.file_path))

    def show_rename_dialog(self):
        old_title = self.title
        old_author = self.author
        old_genre = self.genre
        old_page_count = self.page_count

        dialog = RenameDialog(old_title, old_author, old_genre, old_page_count)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            new_title = dialog.new_title_input.text()
            new_author = dialog.new_author_input.text()
            new_genre = dialog.new_genre_combo.currentText()
            new_page_count = dialog.new_page_count_input.value()

            old_file_path = self.file_path
            old_image_path = os.path.splitext(old_file_path)[0] + ".png"  # Use .png as the extension for image files
            file_extension = os.path.splitext(old_file_path)[1]
            new_file_name = f"{new_title}+{new_author}+{new_genre}+{new_page_count}{file_extension}"
            new_file_path = os.path.join(os.path.dirname(old_file_path), new_file_name)
            new_image_name = f"{new_title}+{new_author}+{new_genre}+{new_page_count}.png"  # Use .png extension for images
            new_image_path = os.path.join(os.path.dirname(old_image_path), new_image_name)

            print(new_image_path)
            print(new_file_path)

            os.rename(old_file_path, new_file_path)

            if os.path.exists(old_image_path):
                os.rename(old_image_path, new_image_path)

class PreviewCard(QFrame):
    def __init__(self, title=None, author=None, genre=None, page_count=None, file_path=None, image_path=None, parent=None, app=None, ebooks=None, grid_layout=None):
        super().__init__()
        self.init_ui(title, author, genre, page_count, file_path, image_path, parent, app, ebooks, grid_layout)

    def init_ui(self, title, author, genre, page_count, file_path, image_path, parent=None, app=None, ebooks=None, grid_layout=None):
        self.setFixedWidth(300)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.setStyleSheet("QFrame { border: 2px solid #000; border-radius: 20px; background-color: #f0f0f0; }")

        self.playout = QVBoxLayout(self)

        self.title_label = QLabel(title)  # Set the title_label text to the provided title
        self.title_label.setWordWrap(True)

        self.image_label = QLabel()  # Create a QLabel for displaying the image
        self.image_label.setFixedWidth(280)
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.playout.addWidget(self.image_label)
        self.playout.addWidget(self.title_label)
        self.playout.addWidget(QLabel(f"Author: {author}"))  # Update author label
        self.playout.addWidget(QLabel(f"Genre: {genre}"))    # Update genre label
        self.playout.addWidget(QLabel(f"Pages: {page_count}"))  # Update page count label

        self.setLayout(self.playout)

    def update_preview(self, title, image_path):
        self.title_label.setText(title)
        pixmap = QPixmap(image_path)
        pixmap = pixmap.scaled(150, 250, aspectRatioMode=Qt.AspectRatioMode.KeepAspectRatio)
        self.image_label.setPixmap(pixmap)

class EbookManagerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.load_last_path()
        self.preview_card = PreviewCard()


    def init_ui(self):
        self.setGeometry(100, 100, 1000, 600)
        self.setWindowTitle("E-book Manager")

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        self.filter_layout = QVBoxLayout()
        self.filter_line_layout = QHBoxLayout()
        self.filter_label = QLabel("Filter by:")
        self.filter_name_input = QLineEdit()
        self.filter_author_input = QLineEdit()
        self.filter_genre_combobox = QComboBox()
        self.filter_genre_combobox.addItem("All Genres")
        self.filter_genre_combobox.addItems([
            "Art & Design", "Biography", "Engineering", "History", "Novels", "Papers",
            "Poetry", "Religious", "Science", "Self Motivation", "Other"
        ])
        self.filter_page_count_greater_label = QLabel("Page Count >=")
        self.filter_page_count_greater_input = QSpinBox()
        self.filter_page_count_greater_input.setMinimum(1)
        self.filter_page_count_greater_input.setMaximum(10000)
        self.filter_page_count_smaller_label = QLabel("Page Count <=")
        self.filter_page_count_smaller_input = QSpinBox()
        self.filter_page_count_smaller_input.setMinimum(1)
        self.filter_page_count_smaller_input.setMaximum(10000)
        self.filter_page_count_smaller_input.setValue(10000)
        self.filter_button = QPushButton("Filter")
        self.filter_button.clicked.connect(self.apply_filter)

        self.clear_filters_button = QPushButton("Clear Filters")
        self.clear_filters_button.clicked.connect(self.clear_filters)

        self.load_button = QPushButton("Load E-books")
        self.load_button.clicked.connect(self.load_ebooks)

        self.filter_line_layout.addWidget(self.filter_label)
        self.filter_line_layout.addWidget(self.filter_name_input)
        self.filter_line_layout.addWidget(self.filter_author_input)
        self.filter_line_layout.addWidget(self.filter_genre_combobox)
        self.filter_line_layout.addWidget(self.filter_page_count_greater_label)
        self.filter_line_layout.addWidget(self.filter_page_count_greater_input)
        self.filter_line_layout.addWidget(self.filter_page_count_smaller_label)
        self.filter_line_layout.addWidget(self.filter_page_count_smaller_input)
        self.filter_line_layout.addWidget(self.filter_button)
        self.filter_line_layout.addWidget(self.clear_filters_button)
        self.filter_line_layout.addWidget(self.load_button)

        self.filter_layout.addLayout(self.filter_line_layout)
        self.filter_tags_layout = QHBoxLayout()
        self.filter_tags = QLabel("")
        self.filter_tags_layout.addWidget(self.filter_tags)
        self.filter_layout.addLayout(self.filter_tags_layout)

        self.layout.addLayout(self.filter_layout)

        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)

        self.scroll_widget = QWidget(self)
        self.grid_layout = QGridLayout(self.scroll_widget)
        #self.grid_layout.setSpacing(10)
        #self.grid_layout.setHorizontalSpacing(50)
        self.available_width = 0 

        self.scroll_area.setWidget(self.scroll_widget)
        # self.layout.addWidget(self.scroll_area)


        # Create a frame to hold the QScrollArea and the preview card
        self.scroll_and_preview_frame = QFrame()
        self.scroll_and_preview_layout = QHBoxLayout(self.scroll_and_preview_frame)
        self.layout.addWidget(self.scroll_and_preview_frame)

        # Add the QScrollArea to the left side
        self.scroll_and_preview_layout.addWidget(self.scroll_area)

        # Create a layout for the preview card and add it to the right side
        
        self.playout = QVBoxLayout()

        self.title_label = QLabel("title")  # Set the title_label text to the provided title
        self.title_label.setWordWrap(True)

        self.auther_label = QLabel("Author")  # Set the title_label text to the provided title
        self.title_label.setWordWrap(True)

        self.genre_label = QLabel("Genre")  # Set the title_label text to the provided title
        self.title_label.setWordWrap(True)

        self.title_label = QLabel("Pages")  # Set the title_label text to the provided title
        self.title_label.setWordWrap(True)

        self.image_label = QLabel()  # Create a QLabel for displaying the image
        self.image_label.setFixedWidth(280)
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.playout.addWidget(self.image_label)
        self.playout.addWidget(self.title_label)
        self.playout.addWidget(QLabel("Author"))  # Update author label
        self.playout.addWidget(QLabel("Genre"))    # Update genre label
        self.playout.addWidget(QLabel("Pages"))  # Update page count label

        self.preview_layout = QVBoxLayout()
        self.preview_layout.addLayout(self.playout)
        self.scroll_and_preview_layout.addLayout(self.preview_layout)

        self.applied_filters = []
        self.ebook_group = QButtonGroup()

    def update_ebook_grid(self, ebooks=None):
        if ebooks is None:
            ebooks = self.ebooks

        if self.available_width == 0:
            return

        card_width = 250  # Desired card width
        num_columns = max(1, self.available_width // card_width)

        # Clear the existing layout
        for i in reversed(range(self.grid_layout.count())):
            widget = self.grid_layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()

        col = 0
        row = 0

        # Add vertical spacing between rows
        #self.grid_layout.setVerticalSpacing(10)  # Adjust the spacing as needed

        for ebook in ebooks:
            card = EbookCard(ebook['title'], ebook['author'], ebook['genre'], ebook['page_count'], ebook['file_path'], ebook['image_path'],app=self,ebook=ebook)
            self.grid_layout.addWidget(card, row, col,1,0)
            col += 1
            if col >= num_columns:
                col = 0
                row += 1

        for i in range(num_columns):
            self.grid_layout.setColumnStretch(i, 1)

    def resizeEvent(self, event):
        self.available_width = event.size().width()
        print(self.available_width)
        self.update_ebook_grid()
        super().resizeEvent(event)
        #self.grid_layout.setSpacing(10)


    def update_preview_card(self, title, image_path,ebook):
        self.title_label.setText(title)
        

    def update_applied_filters(self):
        tags = [f"#{tag}" for tag in self.applied_filters]
        self.filter_tags.setText(" ".join(tags))

    def load_last_path(self):
        config = configparser.ConfigParser()
        config.read('config.ini')
        if 'Paths' in config and 'last_path' in config['Paths']:
            last_path = config['Paths']['last_path']
            if os.path.isdir(last_path):
                self.ebooks = self.scan_folder_for_ebooks(last_path)
                self.update_ebook_grid()

    def save_last_path(self, path):
        config = configparser.ConfigParser()
        config['Paths'] = {'last_path': path}
        with open('config.ini', 'w') as configfile:
            config.write(configfile)

    def load_ebooks(self):
        folder_path = QFileDialog.getExistingDirectory(
            self, "Select Folder Containing E-books", options=QFileDialog.Option.ShowDirsOnly
        )
        if folder_path:
            self.save_last_path(folder_path)
            self.ebooks = self.scan_folder_for_ebooks(folder_path)
            self.update_ebook_grid()

    def scan_folder_for_ebooks(self, folder_path):
        ebook_list = []
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                if file.endswith(".pdf") or file.endswith(".epub"):
                    title, author, genre, page_count = self.extract_metadata_from_filename(file)
                    file_path = os.path.join(root, file)
                    image_path = os.path.join(root, os.path.splitext(file)[0] + ".png")
                    ebook_list.append({"title": title, "author": author, "genre": genre, "page_count": page_count, "file_path": file_path,"image_path": image_path})
        return ebook_list

    def show_rename_dialog(self):
        selected_row = self.grid_layout.indexOf(self.sender())
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
        selected_row = self.grid_layout.indexOf(self.sender())
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
            page_count = "1"
        return title, author, genre, page_count

    def apply_filter(self):
        self.applied_filters = []
        name_filter = self.filter_name_input.text().strip().lower()
        author_filter = self.filter_author_input.text().strip().lower()
        genre_filter = self.filter_genre_combobox.currentText()
        page_count_greater_filter = self.filter_page_count_greater_input.value()
        page_count_smaller_filter = self.filter_page_count_smaller_input.value()

        if name_filter:
            self.applied_filters.append(f"Name:{name_filter}")
        if author_filter:
            self.applied_filters.append(f"Author:{author_filter}")
        if genre_filter != "All Genres":
            self.applied_filters.append(f"Genre:{genre_filter}")
        if page_count_greater_filter > 1:
            self.applied_filters.append(f"Page>={page_count_greater_filter}")
        if page_count_smaller_filter < 10000:
            self.applied_filters.append(f"Page<={page_count_smaller_filter}")

        self.update_applied_filters()

        filtered_ebooks = [ebook for ebook in self.ebooks if
                           (not name_filter or name_filter in ebook['title'].lower()) and
                           (not author_filter or author_filter in ebook['author'].lower()) and
                           (genre_filter == "All Genres" or genre_filter in ebook['genre']) and
                           (page_count_greater_filter <= int(ebook['page_count']) <= page_count_smaller_filter)]

        self.update_ebook_grid(filtered_ebooks)

    def clear_filters(self):
        self.filter_name_input.clear()
        self.filter_author_input.clear()
        self.filter_genre_combobox.setCurrentIndex(0)
        self.filter_page_count_greater_input.setValue(1)
        self.filter_page_count_smaller_input.setValue(10000)

        self.applied_filters = []
        self.update_applied_filters()

        self.update_ebook_grid(self.ebooks)

def main():
    app = QApplication(sys.argv)
    window = EbookManagerApp()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
