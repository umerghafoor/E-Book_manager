from PyQt5.QtWidgets import QLabel, QVBoxLayout, QWidget, QApplication
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QPainterPath
import sys

class RoundedImageLabel(QLabel):
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Create a QPainterPath to define the rounded rectangle
        path = QPainterPath()
        rect = self.rect()
        path.addRoundedRect(rect, 50, 50)  # Adjust the radius as needed
        
        # Set the brush to transparent to make the corners transparent
        painter.setBrush(Qt.GlobalColor.transparent)
        
        # Use the QPainterPath as a clip path to make the label rounded
        painter.setClipPath(path)
        
        super().paintEvent(event)

app = QApplication(sys.argv)
window = QWidget()

# Create a layout for the image (on the left)
image_layout = QVBoxLayout()
image_label = RoundedImageLabel()
image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
image_label.setFixedWidth(100)
image_layout.addWidget(image_label)

window.setLayout(image_layout)
window.show()
sys.exit(app.exec_())
