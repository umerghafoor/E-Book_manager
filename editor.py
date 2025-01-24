import sys
import sqlite3
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QPushButton, QHBoxLayout
from PyQt6.QtCore import Qt
import pandas as pd


class BookDatabase:
    def __init__(self, db_file='books.db'):
        self.db_file = db_file
        self.conn = None
        self.cursor = None

    def connect(self):
        if not self.conn:
            self.conn = sqlite3.connect(self.db_file)
            self.cursor = self.conn.cursor()

    def disconnect(self):
        if self.conn:
            self.conn.close()
            self.conn = None
            self.cursor = None

    def get_all_books(self):
        self.connect()
        try:
            self.cursor.execute('SELECT * FROM books')
            columns = [column[0] for column in self.cursor.description]
            books = self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"SQLite error: {e}")
            books = []
        finally:
            self.disconnect()

        return columns, books


class BookEditor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.db = BookDatabase()
        self.setWindowTitle("Book Database Editor")

        # UI setup
        self.layout = QVBoxLayout()

        # Create table widget
        self.table = QTableWidget()
        self.layout.addWidget(self.table)

        # Load button
        self.load_button = QPushButton("Load Data")
        self.load_button.clicked.connect(self.load_data)
        self.layout.addWidget(self.load_button)

        # Save button
        self.save_button = QPushButton("Save Changes")
        self.save_button.clicked.connect(self.save_changes)
        self.layout.addWidget(self.save_button)

        # Set layout for main window
        container = QWidget()
        container.setLayout(self.layout)
        self.setCentralWidget(container)

    def load_data(self):
        # Get book data from the database
        columns, books = self.db.get_all_books()

        # Set the number of rows and columns in the table
        self.table.setRowCount(len(books))
        self.table.setColumnCount(len(columns))
        self.table.setHorizontalHeaderLabels(columns)

        # Populate table with data
        for row, book in enumerate(books):
            for col, value in enumerate(book):
                self.table.setItem(row, col, QTableWidgetItem(str(value)))

    def save_changes(self):
        row_count = self.table.rowCount()
        col_count = self.table.columnCount()

        # Retrieve modified data from the table
        updated_data = []
        for row in range(row_count):
            row_data = []
            for col in range(col_count):
                item = self.table.item(row, col)
                if item is None:
                    row_data.append(None)
                else:
                    row_data.append(item.text())
            updated_data.append(row_data)

        # Update the database with new values
        self.db.connect()
        try:
            for row_data in updated_data:
                book_id = row_data[0]  # Assuming the first column is the book ID
                updated_values = tuple(row_data[1:])  # Exclude the ID from the update
                self.db.cursor.execute('''
                    UPDATE books SET title = ?, subtitle = ?, author_id = ?, publisher = ?, pub_date = ?, pages = ?, genre = ?, path = ?, thumbnail = ?, notes = ?
                    WHERE id = ?
                ''', (*updated_values, book_id))
            self.db.conn.commit()
        except sqlite3.Error as e:
            print(f"SQLite error: {e}")
            self.db.conn.rollback()
        finally:
            self.db.disconnect()


def main():
    app = QApplication(sys.argv)
    window = BookEditor()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
