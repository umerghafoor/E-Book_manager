import sqlite3

def create_database():
    
    conn = sqlite3.connect('books.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            subtitle TEXT,
            author TEXT NOT NULL,
            publisher TEXT,
            pub_date TEXT,
            pages INTEGER,
            genre TEXT,
            path TEXT,
            thumbnail TEXT,
            notes TEXT,
            tags TEXT
        )
    ''')
    
    conn.commit()
    conn.close()

def add_book(title, subtitle, author, publisher, pub_date, pages, genre, path, thumbnail, notes, tags):
    
    conn = sqlite3.connect('books.db')
    
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO books (title, subtitle, author, publisher, pub_date, pages, genre, path, thumbnail, notes, tags)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (title, subtitle, author, publisher, pub_date, pages, genre, path, thumbnail, notes, tags))
    
    conn.commit()
    conn.close()

def get_book_by_title(title):
    conn = sqlite3.connect('books.db')
    
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM books WHERE title = ?', (title,))
    book = cursor.fetchone()
    
    conn.close()
    
    return book

def get_all_books():
    conn = sqlite3.connect('books.db')
    
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM books')
    books = cursor.fetchall()
    
    conn.close()
    
    return books