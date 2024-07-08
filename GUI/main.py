import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QPushButton, QLabel, QVBoxLayout,
    QHBoxLayout, QSplitter, QFrame, QSizePolicy, QScrollArea, QGridLayout
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon

class MainWindow(QWidget):
    panel_flag = False
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Ebook Manger')
        # TODO : Change the window size based on previus session
        self.setGeometry(100, 100, 800, 600)

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
        self.main_content = QFrame(self)
        self.main_content.setFrameShape(QFrame.Shape.StyledPanel)
        self.main_layout = QVBoxLayout()
        self.main_content.setLayout(self.main_layout)

        # Add label and button to main content area
        self.button = QPushButton('Click to Add Buttons', self)
        self.button.clicked.connect(self.test_on_button_click)
        self.main_layout.addWidget(self.button)

        # Create scrollable area for dynamic boxes
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_content)
        self.grid_layout = QGridLayout()
        self.scroll_layout.addLayout(self.grid_layout)
        self.scroll_content.setLayout(self.scroll_layout)
        self.scroll_area.setWidget(self.scroll_content)

        # Add scrollable area to main layout
        self.main_layout.addWidget(self.scroll_area)

        # Create splitter to make the layout responsive
        self.splitter = QSplitter(Qt.Orientation.Horizontal)
        self.splitter.addWidget(self.side_panel)
        self.splitter.addWidget(self.main_content)
        self.splitter.setSizes([200, 600])

        ###########################################
        #      Finalizing Layout                  #
        ###########################################

        # Create main layout and add splitter
        self.main_layout_container = QHBoxLayout(self)
        self.main_layout_container.addWidget(self.splitter)
        self.setLayout(self.main_layout_container)

        # Initialize widget tracking
        self.widgets = []

        self.show()
        self.toggle_side_panel()

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
        self.update_columns()

    def add_boxes_to_grid(self):
        # Clear the grid layout and reset widget tracking
        for widget in self.widgets:
            widget.setParent(None)
        self.widgets = []

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
        
        self.update_columns()

    def update_columns(self):
        # Calculate the number of columns based on the current width
        width = self.scroll_content.width()
        self.columns = max(1, width // 120)  # Adjust the column width as needed

        # Update positions of existing widgets in the grid layout
        for i, widget in enumerate(self.widgets):
            # TODO: Add custom cards or widgets here
            self.grid_layout.addWidget(widget, i // self.columns, i % self.columns, Qt.AlignmentFlag.AlignTop)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())
