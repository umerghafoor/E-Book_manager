import os
import shutil
import sys
from PyQt6.QtCore import QUrl,Qt,QTimer,QSize
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QFileDialog, QVBoxLayout, QPushButton, QWidget, QLabel,QFrame,
    QLineEdit, QDialog, QHBoxLayout, QSpinBox, QComboBox, QGridLayout, QScrollArea, QButtonGroup,
)
from PyQt6.QtGui import QPixmap,QPainter,QPainterPath
from PyQt6.QtGui import QDesktopServices, QIcon
from PyQt6.QtWidgets import QAbstractSpinBox

import configparser
from PIL import Image, ImageOps, ImageDraw


class RoundedImageLabel(QLabel):
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Create a QPainterPath to define the rounded rectangle
        path = QPainterPath()
        rect = self.rect()
        path.addRoundedRect(rect, 50, 50)  # Adjust the radius as needed
        
        # Use the QPainterPath as a clip path to make the label rounded
        painter.setClipPath(path)
        
        super().paintEvent(event)


class RenameFileDialog(QDialog):
    def __init__(self, old_filename, old_title,old_author,old_genre,old_page_count,parent=None):
        super().__init__(parent)

        self.setWindowTitle("Rename E-book")
        self.setModal(True)

        self.layout = QVBoxLayout(self)

        self.new_name_label = QLabel("Name:")
        self.new_name_input = QLineEdit(old_title)

        self.new_author_label = QLabel("Author:")
        self.new_author_input = QLineEdit(old_author)

        self.new_genre_label = QLabel("Genre:")
        self.new_genre_combo = QComboBox()
        self.new_genre_combo.setPlaceholderText(old_genre)

        genres = [
            "Art & Design",
            "Biography",
            "Engineering",
            "History",
            "Novels",
            "Papers",
            "Poetry",
            "Religious",
            "Science",
            "Self Motivation",
            "Other"
        ]

        self.new_genre_combo.addItems(genres)

        self.new_pages_label = QLabel("Pages:")
        self.new_pages_input = QLineEdit(old_page_count)

        self.rename_button = QPushButton("Rename")
        self.rename_button.clicked.connect(self.accept)

        self.image_path_label = QLabel("Image Path:")
        self.image_path_input = QLineEdit()
        self.image_path_button = QPushButton("Browse Image")
        self.image_path_button.clicked.connect(self.select_image)

        self.paste_image_button = QPushButton("Paste from Clipboard")
        self.paste_image_button.clicked.connect(self.paste_image)

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

        self.load_stylesheet("styles.css")

    
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
    def load_stylesheet(self, stylesheet_file):
       with open(stylesheet_file, "r") as file:
            self.setStyleSheet(file.read())


class EbookCard(QFrame):
    def __init__(self, title, author, genre, page_count, file_path, image_path, parent=None, app=None, ebook=None, grid_layout=None):
        super().__init__(parent)
        self.app = app
        self.file_path = file_path
        self.image_path = image_path
        self.title = title
        self.author = author
        self.genre = genre
        self.page_count = page_count
        self.ebook = ebook
        self.grid_layout = grid_layout
        self.selected = False

        # Create the main layout for the card
        main_layout = QHBoxLayout(self)

        # Create a layout for the image (on the left)
        image_layout = QVBoxLayout()
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setFixedWidth(80)
        self.image_label.setStyleSheet("border-radius: 20px;") 
        image_layout.addWidget(self.image_label)

        # Create a layout for the text and button (on the right)
        text_button_layout = QVBoxLayout()
        title_label = QLabel(f"{title}")
        title_label.setWordWrap(True)
        title_label.setStyleSheet("QLabel { font-weight: bold; }")
        title_label.setFixedWidth(180)
        title_label.setFixedHeight(50)
        auther_label = QLabel(f"Author: {author}")
        auther_label.setStyleSheet("QLabel { color: #2a3c4a; }")

        text_button_layout.addWidget(title_label)
        text_button_layout.addWidget(auther_label)
        text_button_layout.addWidget(QLabel(f"Genre: {genre}"))
        text_button_layout.addWidget(QLabel(f"Pages: {page_count}"))
        text_button_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        text_button_layout.setSpacing(0)

        # "Rename" button
        self.rename_button = QPushButton("Rename")
        self.rename_button.setFixedWidth(80)
        self.rename_button.clicked.connect(self.show_rename_dialog)
        text_button_layout.addWidget(self.rename_button)

        # Add the image layout to the main layout
        main_layout.addLayout(image_layout)

        # Add the text and button layout to the main layout
        main_layout.addLayout(text_button_layout)

        main_layout.setSpacing(10)

        # Initialize pixmap to None
        self.pixmap = None
        self.magnified = None

        self.load_image(image_path)

        self.setFixedSize(290, 160)
        self.load_stylesheet("cardstyles.css")
        #self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    def enterEvent(self, event):
        self.setProperty("hoverState", True)
        self.style().unpolish(self)
        self.style().polish(self)

    def leaveEvent(self, event):
        self.setProperty("hoverState", False)
        self.style().unpolish(self)
        self.style().polish(self)

    def mouseDoubleClickEvent(self, event):
        self.setProperty("OpenState", False)
        self.style().unpolish(self)
        self.style().polish(self)

        self.open_ebook()
    
    def set_selected(self, selected):
        self.selected = selected
        # if selected:
        #     self.setStyleSheet("QFrame { border: 0px solid #000; border-radius: 20px; background-color: #44a8fe; }")
        # else:
        #     self.setStyleSheet("QFrame { border: 0px solid #000; border-radius: 20px; }")

    def mousePressEvent(self, event):
        if not self.selected:
            self.set_selected(True)  # Select the card
            self.app.update_preview_card(self.title, self.image_path,self.ebook)
        else:
            self.set_selected(False)  # Deselect the card

    def load_image(self, image_path):
        if os.path.exists(image_path):
            self.pixmap = QPixmap(image_path)
        else:
            # Load a default image if the image path is not valid
            self.pixmap = QPixmap("default.png")
        fixed_width = 80
        fixed_height = 250
        if not self.pixmap.isNull():
            self.pixmap = self.pixmap.scaled(fixed_width, fixed_height, aspectRatioMode=Qt.AspectRatioMode.KeepAspectRatio)
            self.image_label.setPixmap(self.pixmap)
            self.magnified_pixmap = self.pixmap.scaled(95, 200, aspectRatioMode=Qt.AspectRatioMode.KeepAspectRatio)

    def open_ebook(self):
        print(self.file_path)
        QDesktopServices.openUrl(QUrl.fromLocalFile(self.file_path))

    def show_rename_dialog(self):
        old_title = self.title
        old_author = self.author
        old_genre = self.genre
        old_page_count = self.page_count

        dialog = RenameFileDialog(self.file_path,old_title,old_author,old_genre,old_page_count)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            new_title = dialog.new_name_input.text()
            new_author = dialog.new_author_input.text()
            new_genre = dialog.new_genre_combo.currentText()
            new_page_count = dialog.new_pages_input.text()
            image_path = dialog.image_path_input.text()

            old_file_path = self.file_path
            old_image_path = os.path.splitext(old_file_path)[0] + ".png"
            file_extension = os.path.splitext(old_file_path)[1]
            new_file_name = f"{new_title}+{new_author}+{new_genre}+{new_page_count}{file_extension}"
            new_file_path = os.path.join(os.path.dirname(old_file_path), new_file_name)
            new_image_name = f"{new_title}+{new_author}+{new_genre}+{new_page_count}.png" 
            new_image_path = os.path.join(os.path.dirname(old_image_path), new_image_name)

            print(new_file_path)
            print(new_image_path)

            if os.path.exists(old_file_path):
                os.rename(old_file_path, new_file_path)

            if os.path.exists(image_path):
                shutil.copy(image_path, new_image_path)
            elif os.path.exists(old_image_path):
                os.rename(old_image_path, new_image_path)

    def load_stylesheet(self, stylesheet_file):
        # Load and apply the style sheet from the file
        with open(stylesheet_file, "r") as file:
            self.setStyleSheet(file.read())

class EbookManagerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon("icon.png"))
        self.init_ui()
        self.load_last_path()

    def init_ui(self):
        self.setGeometry(100, 100, 1000, 600)
        self.setWindowTitle("E-book Manager")

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        self.filter_layout = QVBoxLayout()
        self.filter_line_layout = QVBoxLayout()
        self.filter_name_input = QLineEdit()
        self.filter_name_input.setFixedWidth(280)
        self.filter_name_input.setPlaceholderText("Filter by Name")
        self.filter_author_input = QLineEdit()
        self.filter_author_input.setFixedWidth(280)
        self.filter_author_input.setPlaceholderText("Filter by Author")
        self.filter_genre_combobox = QComboBox()
        self.filter_genre_combobox.setFixedWidth(280)
        self.filter_genre_combobox.addItem("All Genres")
        self.filter_genre_combobox.addItems([
            "Art & Design", "Biography", "Engineering", "History", "Novels", "Papers",
            "Poetry", "Religious", "Science", "Self Motivation", "Other"
        ])
        # self.filter_page_count_greater_label = QLabel("Page Count >=")
        self.filter_page_count_greater_input = QSpinBox()
        self.filter_page_count_greater_input.setMinimum(1)
        self.filter_page_count_greater_input.setMaximum(10000)
        self.filter_page_count_greater_input.setFixedWidth(100)
        self.filter_page_count_greater_input.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.filter_page_count_greater_input.setStepType(QAbstractSpinBox.StepType.AdaptiveDecimalStepType)

        self.filter_page_count_smaller_label = QLabel("Page")
        self.filter_page_count_smaller_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.filter_page_count_smaller_input = QSpinBox()
        self.filter_page_count_smaller_input.setMinimum(1)
        self.filter_page_count_smaller_input.setMaximum(10000)
        self.filter_page_count_smaller_input.setValue(1000)
        self.filter_page_count_smaller_input.setFixedWidth(100)
        self.filter_page_count_smaller_input.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.filter_page_count_smaller_input.setStepType(QAbstractSpinBox.StepType.AdaptiveDecimalStepType)
        
        self.filter_button = QPushButton("Filter")
        self.filter_button.setIcon(QIcon("filter.png"))
        self.filter_button.setIconSize(QSize(22, 22))
        self.filter_button.clicked.connect(self.apply_filter)

        self.clear_filters_button = QPushButton("Clear")
        self.clear_filters_button.setIcon(QIcon("clear-filter.png"))
        self.clear_filters_button.clicked.connect(self.clear_filters)

        self.load_button = QPushButton("Load")
        self.load_button.setIcon(QIcon("folder.png"))
        self.load_button.clicked.connect(self.load_ebooks)

        self.filter_line_layout.addWidget(self.filter_name_input)
        self.filter_line_layout.addWidget(self.filter_author_input)
        page_count = QHBoxLayout()
        page_count.addWidget(self.filter_page_count_greater_input)
        page_count.addWidget(self.filter_page_count_smaller_label)
        page_count.addWidget(self.filter_page_count_smaller_input)
        self.filter_line_layout.addLayout(page_count)
        self.filter_line_layout.addWidget(self.filter_genre_combobox)

        combobox_1=QHBoxLayout()
        combobox_1.addWidget(self.filter_button)
        combobox_1.addWidget(self.clear_filters_button)
        combobox_1.addWidget(self.load_button)
        self.filter_line_layout.addLayout(combobox_1)
        
        self.sort_combo = QComboBox()
        self.sort_combo.addItem("Sort by Name (A-Z)")
        self.sort_combo.addItem("Sort by Author (A-Z)")
        self.sort_combo.addItem("Sort by Pages (Low to High)")
        self.sort_combo.addItem("Sort by Genre (A-Z)")
        self.sort_combo.currentIndexChanged.connect(self.sort_ebooks)


        self.filter_line_layout.addWidget(self.sort_combo)
        
        self.filter_layout.addLayout(self.filter_line_layout)
        self.filter_tags_layout = QHBoxLayout()
        self.filter_tags = QLabel("")
        self.filter_tags_layout.addWidget(self.filter_tags)
        self.filter_layout.addLayout(self.filter_tags_layout)

        #self.layout.addLayout(self.filter_layout)

        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)

        self.scroll_widget = QWidget(self)
        self.grid_layout = QGridLayout(self.scroll_widget)
        self.grid_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
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

        self.title_label = QLabel("title")
        self.title_label.setWordWrap(True)

        self.auther_label = QLabel("Author")
        self.title_label.setWordWrap(True)

        self.genre_label = QLabel("Genre")  
        self.genre_label.setWordWrap(True)

        self.Pages_label = QLabel("Pages")
        self.Pages_label.setWordWrap(True)

        self.image_label = QLabel() 
        self.image_label.setFixedWidth(280)
        # self.image_label.setFixedHeight(300)
        self.pixmap = QPixmap("default.png")
        self.pixmap = self.pixmap.scaled(175, 280, aspectRatioMode=Qt.AspectRatioMode.KeepAspectRatio)
        self.image_label.setPixmap(self.pixmap)
        
        self.playout.addWidget(self.image_label)
        self.playout.addWidget(self.title_label)
        self.playout.addWidget(self.auther_label)  # Update author label
        self.playout.addWidget(self.genre_label)    # Update genre label
        self.playout.addWidget(self.Pages_label)  # Update page count label

        self.preview_layout = QVBoxLayout()
        self.preview_layout.addLayout(self.filter_layout)
        self.preview_layout.addLayout(self.playout)
        self.scroll_and_preview_layout.addLayout(self.preview_layout)

        self.applied_filters = []
        self.ebook_group = QButtonGroup()

        self.last_available_width = 0
        self.load_stylesheet("styles.css")
        
    def update_ebook_grid(self, ebooks=None):
        
        if ebooks is None:
            ebooks = self.ebooks

        self.sort_ebooks()
        
        if self.available_width == 0:
            return

        card_width = 290  # Desired card width
        num_columns = max(1, (self.available_width-350) // card_width)

        # Clear the existing layout
        for i in reversed(range(self.grid_layout.count())):
            widget = self.grid_layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()

        col = 0
        row = 0

        # Add vertical spacing between rows
        #self.grid_layout.setVerticalSpacing(10)

        for ebook in ebooks:
            card = EbookCard(ebook['title'], ebook['author'], ebook['genre'], ebook['page_count'], ebook['file_path'], ebook['image_path'],app=self,ebook=ebook)
            self.grid_layout.addWidget(card, row, col,1,1)
            col += 1
            if col >= num_columns:
                col = 0
                row += 1

        for i in range(num_columns):
            self.grid_layout.setColumnStretch(i, 1)

    def sort_ebooks(self):
        selected_sort_option = self.sort_combo.currentText()

        if selected_sort_option == "Sort by Name (A-Z)":
            self.ebooks.sort(key=lambda ebook: ebook["title"])
        elif selected_sort_option == "Sort by Author (A-Z)":
            self.ebooks.sort(key=lambda ebook: ebook["author"])
        elif selected_sort_option == "Sort by Pages (Low to High)":
            self.ebooks.sort(key=lambda ebook: int(ebook["page_count"]))
        elif selected_sort_option == "Sort by Genre (A-Z)":
            self.ebooks.sort(key=lambda ebook: ebook["genre"])

       
    def resizeEvent(self, event):
        self.available_width = event.size().width()
        # print(self.available_width)
        self.delayed_update_ebook_grid()  # Call the delayed update_ebook_grid method
        super().resizeEvent(event)

    def delayed_update_ebook_grid(self):
        if not hasattr(self, "timer"):
            self.timer = QTimer(self)
            self.timer.setSingleShot(True)
            self.timer.timeout.connect(self.update_ebook_grid)
        
        # Only update the grid layout when the available width changes
        if self.available_width != self.last_available_width:
            self.timer.start(500)
            self.last_available_width = self.available_width

    def update_preview_card(self, title, image_path,ebook):
        self.title_label.setText(ebook['title'])
        self.auther_label.setText(ebook["author"])
        self.genre_label.setText(ebook["genre"])
        self.Pages_label.setText(ebook["page_count"])

        if os.path.exists(image_path):
            self.pixmap = QPixmap(image_path)
        else:
            # Load a default image if the image path is not valid
            self.pixmap = QPixmap("default.png")
        self.pixmap = self.pixmap.scaled(240, 480, aspectRatioMode=Qt.AspectRatioMode.KeepAspectRatio)
        self.image_label.setPixmap(self.pixmap)

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
        else:
            self.ebooks = []

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
            title = filename_without_extension 
            author = genre = "Unknown"
            page_count = "0"
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

    def load_stylesheet(self, stylesheet_file):
        # Load and apply the style sheet from the file
        with open(stylesheet_file, "r") as file:
            self.setStyleSheet(file.read())

def main():
    app = QApplication(sys.argv)
    window = EbookManagerApp()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
