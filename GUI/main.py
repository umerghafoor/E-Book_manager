import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QPushButton, QLabel, QVBoxLayout,
    QHBoxLayout, QSplitter, QFrame, QSizePolicy, QScrollArea, QGridLayout
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon

from GUI.Views.Home import HomeView
from GUI.Views.Library import LibraryView
from GUI.Views.Settings import SettingsView

class MainWindow(QWidget):
    panel_flag = False
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Ebook Manger')
        # TODO : Change the window size based on previus session
        self.setGeometry(100, 100, 800, 600)
        self.load_stylesheet('style.css')

        ###########################################
        #      Creating Side panel                #
        ###########################################

        # Create side panel with Text Buttons
        self.side_panel = QFrame(self)
        self.side_panel.setFrameShape(QFrame.Shape.StyledPanel)
        self.side_panel.setMinimumWidth(50)
        self.side_panel.setMaximumWidth(240)
        self.side_panel.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)

        # Create buttons for side panel
        self.expand_button_fp = QPushButton('Expand', self)
        self.home_button_fp = QPushButton('Home', self)
        self.library_button_fp = QPushButton('Library', self)
        self.settings_button_fp = QPushButton('Setting', self)
        self.expand_button_fp.setFixedHeight(48)
        self.home_button_fp.setFixedHeight(48)
        self.library_button_fp.setFixedHeight(48)
        self.settings_button_fp.setFixedHeight(48)

        # Add icons to buttons
        # TODO : Change the icon path to your local path
        self.expand_button_fp.setIcon(QIcon('icon.png'))
        self.home_button_fp.setIcon(QIcon('icon.png'))
        self.library_button_fp.setIcon(QIcon('icon.png'))
        self.settings_button_fp.setIcon(QIcon('icon.png'))

        # Add functions of the buttons
        self.expand_button_fp.clicked.connect(self.toggle_side_panel)
        self.home_button_fp.clicked.connect(self.show_home_view)
        self.library_button_fp.clicked.connect(self.show_library_view)
        self.settings_button_fp.clicked.connect(self.show_settings_view)

        # Add Items to side panel
        self.side_layout = QVBoxLayout()
        self.side_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.side_layout.setContentsMargins(0, 0, 0, 0)
        self.side_layout.addWidget(self.expand_button_fp)
        self.side_layout.addWidget(self.home_button_fp)
        self.side_layout.addWidget(self.library_button_fp)
        self.side_layout.addStretch()
        self.side_layout.addWidget(self.settings_button_fp)

        self.side_panel.setLayout(self.side_layout)

        ###########################################
        #      Creating Main content area         #
        ###########################################

        # Create main content area
        self.main_layout = QVBoxLayout()
    
    
        # Create splitter to make the layout responsive
        self.splitter = QSplitter(Qt.Orientation.Horizontal)
        self.splitter.setContentsMargins(0, 0, 0, 0)
        self.splitter.addWidget(self.side_panel)
        self.main_content_frame = QFrame(self)
        self.splitter.addWidget(self.main_content_frame)
        self.main_content_frame.setLayout(self.main_layout)
        self.splitter.setSizes([200, 600])

        # TODO : Change the view to the view you want to show first
        self.show_home_view()
        # self.show_library_view()

        ###########################################
        #      Finalizing Layout                  #
        ###########################################

        # Create main layout and add splitter
        self.main_layout_container = QHBoxLayout(self)
        self.main_layout_container.setContentsMargins(0, 0, 0, 0)
        self.main_layout_container.addWidget(self.splitter)
        self.setLayout(self.main_layout_container)

        # Initialize widget tracking
        self.widgets = []

        self.show()
        self.toggle_side_panel()
    
    def load_stylesheet(self, stylesheet_file):
        # Load and apply the style sheet from the file
        with open(stylesheet_file, "r") as file:
            self.setStyleSheet(file.read())

    def test_on_button_click(self):
        self.add_boxes_to_grid()

    def toggle_side_panel(self):
        def toggle_state(show_panel):
            if show_panel:
                self.splitter.setSizes([50, sizes[1] + sizes[0]])
                self.expand_button_fp.setText('')
                self.home_button_fp.setText('')
                self.library_button_fp.setText('')
                self.settings_button_fp.setText('')
                self.panel_flag = False
            else:
                self.splitter.setSizes([200, sizes[1] - 200])
                self.expand_button_fp.setText('Expand')
                self.home_button_fp.setText('Home')
                self.library_button_fp.setText('Library')
                self.settings_button_fp.setText('Settings')
                self.panel_flag = True

        sizes = self.splitter.sizes()
        
        if  self.panel_flag:
            toggle_state(True)
        else:
            toggle_state(False)

    def add_boxes_to_grid(self):
        # Clear the grid layout and reset widget tracking
        for widget in self.widgets:
            widget.setParent(None)
        self.widgets = []

        # books = book_db.get_all_books()
        #load all books from the database
        books = []
        print("This is the books", books)



        # Add new fixed-size boxes
        num_boxes = 1000  # Adjust this to add more boxes
        for i in range(num_boxes):
            box = QLabel(f'Box {i+1}', self)
            box.setFixedSize(100, 100)
            box.setStyleSheet("background-color: lightblue; border: 1px solid black; margin: 5px;")
            self.grid_layout.addWidget(box, i // self.columns, i % self.columns, Qt.AlignmentFlag.AlignTop)
            self.widgets.append(box)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if self.width() > 1200:
            if not self.panel_flag:
                self.toggle_side_panel()
        if self.width() < 800:
            if self.panel_flag:
                self.toggle_side_panel()
    
    def update_main_view(self, view_class):
        for i in reversed(range(self.main_layout.count())):
            widget = self.main_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)
        view = view_class(self)
        self.main_layout.addWidget(view)

    def show_home_view(self):
        self.update_main_view(HomeView)

    def show_library_view(self):
        self.update_main_view(LibraryView)

    def show_settings_view(self):
        self.update_main_view(SettingsView)

