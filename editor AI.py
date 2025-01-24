import sys
import sqlite3
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QPushButton
from PyQt6.QtCore import Qt
from openai import OpenAI

# Define the GPTModule class using your provided reference
class GPTModule:
    def __init__(self, api_key, base_url="https://openrouter.ai/api/v1", model="openai/gpt-3.5-turbo"):
        self.client = OpenAI(
            base_url=base_url,
            api_key=api_key
        )
        self.model = model

    def get_gpt_response(self, user_input, referer=None, title=None, system_prompt=None, max_tokens=None):
        try:
            extra_headers = {}
            if referer:
                extra_headers["HTTP-Referer"] = referer
            if title:
                extra_headers["X-Title"] = title

            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": user_input})

            completion = self.client.chat.completions.create(
                extra_headers=extra_headers,
                model=self.model,
                messages=messages,
                max_tokens=max_tokens
            )

            return completion.choices[0].message.content
        except Exception as e:
            return f"Error: {str(e)}"

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

    def update_book_details(self, book_id, new_title, new_subtitle, new_genre, new_publisher, new_pub_date, new_pages, new_notes):
        self.connect()
        try:
            self.cursor.execute('''
                UPDATE books 
                SET title = ?, subtitle = ?, genre = ?, publisher = ?, pub_date = ?, pages = ?, notes = ? 
                WHERE id = ?
            ''', (new_title, new_subtitle, new_genre, new_publisher, new_pub_date, new_pages, new_notes, book_id))
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"SQLite error: {e}")
            self.conn.rollback()
        finally:
            self.disconnect()


class BookEditor(QMainWindow):
    def __init__(self, gpt_api_key):
        super().__init__()
        self.db = BookDatabase()
        self.gpt_module = GPTModule(api_key=gpt_api_key)
        self.setWindowTitle("AI Book Database Editor")

        # UI setup
        self.layout = QVBoxLayout()

        # Create table widget
        self.table = QTableWidget()
        self.layout.addWidget(self.table)

        # Load button
        self.load_button = QPushButton("Load Data")
        self.load_button.clicked.connect(self.load_data)
        self.layout.addWidget(self.load_button)

        # Rename button
        self.rename_button = QPushButton("Update Book Details Using AI")
        self.rename_button.clicked.connect(self.update_books_with_ai)
        self.layout.addWidget(self.rename_button)

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

    def update_books_with_ai(self):
        row_count = self.table.rowCount()

        # For each book, use AI to generate new details
        for row in range(row_count):
            # Extract relevant fields (title, author)
            title_item = self.table.item(row, 1)  # Assuming 'title' is in the second column
            author_item = self.table.item(row, 10)  # Assuming 'author' is in the 11th column
            
            if title_item and author_item:
                title = title_item.text()
                author = author_item.text()

                # Create a prompt for the AI to get all details (title, subtitle, genre, etc.)
                prompt = f"""
                Provide full details for the book titled '{title}' by {author}. Include the correct title, subtitle, genre, publisher, publication date, number of pages, and any additional notes.
                AI returns data in the format:
                Title: New Title
                Subtitle: New Subtitle
                Genre: Genre
                Publisher: Publisher
                Publication Date: Date
                Pages: Number
                Notes: Some Notes
                """

                # Get the new details from the AI
                new_details = self.get_ai_details(prompt)

                # print(f"New details for book {title}: {new_details}")

                # Parse the returned details (assuming it's a structured response)
                if new_details:
                    new_title, new_subtitle, new_genre, new_publisher, new_pub_date, new_pages, new_notes = new_details
                    print(f"Updating book {title} \n")
                    print(f"New Title: {new_title}")
                    print(f"New Subtitle: {new_subtitle}")
                    print(f"New Genre: {new_genre}")
                    print(f"New Publisher: {new_publisher}")
                    print(f"New Publication Date: {new_pub_date}")
                    print(f"New Pages: {new_pages}")
                    print(f"New Notes: {new_notes}")

                    self.table.setItem(row, 1, QTableWidgetItem(new_title))  # Update the title column
                    self.table.setItem(row, 2, QTableWidgetItem(new_subtitle))  # Update the subtitle column
                    self.table.setItem(row, 6, QTableWidgetItem(new_genre))  # Update the genre column
                    self.table.setItem(row, 3, QTableWidgetItem(new_publisher))  # Update publisher column
                    self.table.setItem(row, 4, QTableWidgetItem(new_pub_date))  # Update publication date column
                    self.table.setItem(row, 5, QTableWidgetItem(str(new_pages)))  # Update pages column
                    self.table.setItem(row, 9, QTableWidgetItem(new_notes))  # Update notes column

                    # Update the database with the new details
                    book_id = self.table.item(row, 0).text()
                    # Do you Want to update the database with the new details
                    response = input("Do you want to update the database with the new details? (y/n): ")
                    if response.lower() == "y":
                        self.db.update_book_details(book_id, new_title, new_subtitle, new_genre, new_publisher, new_pub_date, new_pages, new_notes)

    def get_ai_details(self, prompt):
        response = self.gpt_module.get_gpt_response(user_input=prompt)
        # Parse the AI response (assuming it's returned in a structured format, like comma-separated)
        if response:
            details = response.split("\n")
            # Assuming AI returns data in the format:
            # Title: New Title
            # Subtitle: New Subtitle
            # Genre: Genre
            # Publisher: Publisher
            # Publication Date: Date
            # Pages: Number
            # Notes: Some Notes

            try:
                new_title = details[0].split(":")[1].strip()
                new_subtitle = details[1].split(":")[1].strip()
                new_genre = details[2].split(":")[1].strip()
                new_publisher = details[3].split(":")[1].strip()
                new_pub_date = details[4].split(":")[1].strip()
                new_pages = int(details[5].split(":")[1].strip())
                new_notes = details[6].split(":")[1].strip()
                return new_title, new_subtitle, new_genre, new_publisher, new_pub_date, new_pages, new_notes
            except Exception as e:
                print(f"Error parsing AI response: {e}")
                return None
        return None


def main():
    app = QApplication(sys.argv)
    gpt_api_key = "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"  # Replace with your actual API key
    window = BookEditor(gpt_api_key=gpt_api_key)
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
