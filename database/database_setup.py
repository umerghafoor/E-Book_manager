import sqlite3

class BookDatabase:
    def __init__(self, db_file='books.db'):
        self.db_file = db_file
        self.conn = None
        self.cursor = None
    
    def connect(self):
        # if not conected, connect to the database
        if not self.conn:
            self.conn = sqlite3.connect(self.db_file)
            self.cursor = self.conn.cursor()
    
    def disconnect(self):
        if self.conn:
            self.conn.close()
            self.conn = None
            self.cursor = None
    
    def create_database(self):
        self.connect()
        
        # Create authors table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS authors (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL
            )
        ''')
        
        # Create books table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY,
                title TEXT NOT NULL,
                subtitle TEXT,
                publisher TEXT,
                pub_date TEXT,
                pages INTEGER,
                genre TEXT,
                path TEXT,
                thumbnail TEXT,
                notes TEXT,
                author_id INTEGER,
                FOREIGN KEY (author_id) REFERENCES authors(id)
            )
        ''')
        
        # Create tags table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS tags (
                id INTEGER PRIMARY KEY,
                tag TEXT UNIQUE
            )
        ''')
        
        # Create book_tags table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS book_tags (
                book_id INTEGER,
                tag_id INTEGER,
                PRIMARY KEY (book_id, tag_id),
                FOREIGN KEY (book_id) REFERENCES books(id),
                FOREIGN KEY (tag_id) REFERENCES tags(id)
            )
        ''')
        
        self.conn.commit()
        self.disconnect()
    
    def add_author(self, name,close_conection=True):
        self.connect()
        try:
            # Check if author already exists
            
            self.cursor.execute('SELECT id FROM authors WHERE name = ?', (name,))
            author = self.cursor.fetchone()
            if author:
                author_id = author[0]
            else:
                self.cursor.execute('INSERT OR IGNORE INTO authors (name) VALUES (?)', (name,))
                author_id = self.cursor.lastrowid
            
            self.conn.commit()
            
        except sqlite3.Error as e:
            print(f"SQLite error (add_author): {e}")
            self.conn.rollback()
        
        finally:
            if close_conection:
                self.disconnect()
        
        return author_id
    
    def add_tag(self, tag,close_conection=True):
        self.connect()
        
        try:
            # Insert tag if not already present 
            self.cursor.execute('INSERT OR IGNORE INTO tags (tag) VALUES (?)', (tag,))
            self.conn.commit()
            # Retrieve tag_id
            self.cursor.execute('SELECT id FROM tags WHERE tag = ?', (tag,))
            tag_id = self.cursor.fetchone()[0]
            
        except sqlite3.Error as e:
            print(f"SQLite error (add_tag): {e}")
            self.conn.rollback()
            tag_id = None
        
        finally:
            if close_conection:
                self.disconnect()
        
        return tag_id
    
    def add_book(self, title, subtitle, author_name, publisher, pub_date, pages, genre, path, thumbnail, notes, tags):
        self.connect()
        try:
            author_id = self.add_author(author_name,close_conection=False)
            
            # Insert book details
            self.cursor.execute('''
                INSERT INTO books (title, subtitle, author_id, publisher, pub_date, pages, genre, path, thumbnail, notes)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (title, subtitle, author_id, publisher, pub_date, pages, genre, path, thumbnail, notes))
                
            book_id = self.cursor.lastrowid
            
            # Insert tags for the book
            for tag in tags.split(', '):
                tag_id = self.add_tag(tag,close_conection=False)
                
                self.cursor.execute('INSERT INTO book_tags (book_id, tag_id) VALUES (?, ?)', (book_id, tag_id))
            
            self.conn.commit()
        
        except sqlite3.Error as e:
            print(f"SQLite error: {e}")
            self.conn.rollback()
        
        finally:
            self.disconnect()
    
    def book_exists(self, book_id):
        self.connect()
        
        try:
            self.cursor.execute('SELECT id FROM books WHERE id = ?', (book_id,))
            book = self.cursor.fetchone()
            
        except sqlite3.Error as e:
            print(f"SQLite error: {e}")
        
        finally:
            self.disconnect()
        
        return bool(book)

    def get_book_by_title(self, title):
        self.connect()
        
        try:
            self.cursor.execute('SELECT * FROM books WHERE title = ?', (title,))
            book = self.cursor.fetchone()
            
        except sqlite3.Error as e:
            print(f"SQLite error: {e}")
        
        finally:
            self.disconnect()
        
        return book
    
    def get_all_books(self):
        self.connect()
        
        try:
            self.cursor.execute('SELECT * FROM books')
            books = self.cursor.fetchall()
            
        except sqlite3.Error as e:
            print(f"SQLite error: {e}")
        
        finally:
            self.disconnect()
        
        return books
    
    def get_tags_by_book_id(self, book_id):
        self.connect()
        
        try:
            self.cursor.execute('''
                SELECT tag
                FROM tags
                JOIN book_tags ON tags.id = book_tags.tag_id
                WHERE book_tags.book_id = ?
            ''', (book_id,))
            tags = self.cursor.fetchall()
            
        except sqlite3.Error as e:
            print(f"SQLite error: {e}")
        
        finally:
            self.disconnect()
        
        return tags

    def get_author_by_book_id(self, book_id):
        self.connect()
        
        try:
            self.cursor.execute('''
                SELECT name
                FROM authors
                JOIN books ON authors.id = books.author_id
                WHERE books.id = ?
            ''', (book_id,))
            author = self.cursor.fetchone()
            
        except sqlite3.Error as e:
            print(f"SQLite error: {e}")
        
        finally:
            self.disconnect()
        
        return author

    def edit_book(self, book_id, title=None, subtitle=None, author_id=None, author=None, publisher=None, pub_date=None, pages=None, genre=None, path=None, thumbnail=None, notes=None, tags=None):
        self.connect()
        
        try:
            if author:
                author_id = self.add_author(author,close_conection=False)
            
            updates = {
                'title': title,
                'subtitle': subtitle,
                'author_id': author_id,
                'publisher': publisher,
                'pub_date': pub_date,
                'pages': pages,
                'genre': genre,
                'path': path,
                'thumbnail': thumbnail,
                'notes': notes
            }
            
            updates = {k: v for k, v in updates.items() if v is not None}
            
            query = 'UPDATE books SET ' + ', '.join([f"{k} = ?" for k in updates.keys()]) + ' WHERE id = ?'
            
            self.cursor.execute(query, list(updates.values()) + [book_id])
            
            if tags:
                self.cursor.execute('DELETE FROM book_tags WHERE book_id = ?', (book_id,))
                
                for tag in tags.split(', '):
                    tag_id = self.add_tag(tag)
                    self.cursor.execute('INSERT INTO book_tags (book_id, tag_id) VALUES (?, ?)', (book_id, tag_id))
            
            self.conn.commit()
        
        except sqlite3.Error as e:
            print(f"SQLite error: {e}")
            self.conn.rollback()
        
        finally:
            self.disconnect()

    def add_tag_to_book(self, book_id, tag):
        self.connect()
        
        try:
            tag_id = self.add_tag(tag,close_conection=False)
            self.cursor.execute('INSERT INTO book_tags (book_id, tag_id) VALUES (?, ?)', (book_id, tag_id))
            self.conn.commit()
        
        except sqlite3.Error as e:
            print(f"SQLite error: {e}")
            self.conn.rollback()
        
        finally:
            self.disconnect()


class UserDatabase:
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
    
    def create_tables(self):
        self.connect()
        try:
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY,
                    username TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL,
                    email TEXT UNIQUE NOT NULL
                )
            ''')

            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS user_books (
                    user_id INTEGER,
                    book_id INTEGER,
                    progress INTEGER,
                    PRIMARY KEY (user_id, book_id),
                    FOREIGN KEY (user_id) REFERENCES users(id),
                    FOREIGN KEY (book_id) REFERENCES books(id)
                )
            ''')

            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS user_notes (
                    id INTEGER PRIMARY KEY,
                    user_id INTEGER,
                    book_id INTEGER,
                    note TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id),
                    FOREIGN KEY (book_id) REFERENCES books(id)
                )
            ''')

            self.conn.commit()
        
        except sqlite3.Error as e:
            print(f"SQLite error (create_tables): {e}")
            self.conn.rollback()
        
        finally:
            self.disconnect()
    
    def create_user(self, username, password, email):
        self.connect()
        try:
            self.cursor.execute('INSERT INTO users (username, password, email) VALUES (?, ?, ?)', (username, password, email))
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"SQLite error (create_user): {e}")
            self.conn.rollback()
        finally:
            self.disconnect()
    
    def user_exists(self, username):
        self.connect()
        try:
            self.cursor.execute('SELECT id FROM users WHERE username = ?', (username,))
            user_id = self.cursor.fetchone()
            return user_id is not None
        except sqlite3.Error as e:
            print(f"SQLite error (user_exists): {e}")
            return False
        finally:
            self.disconnect()
    
    def book_exists(self, book_id):
        self.connect()
        try:
            self.cursor.execute('SELECT id FROM books WHERE id = ?', (book_id,))
            book_id = self.cursor.fetchone()
            return book_id is not None
        except sqlite3.Error as e:
            print(f"SQLite error (book_exists): {e}")
            return False
        finally:
            self.disconnect()
    
    def add_user_book_progress(self, user_id, book_id, progress):
        if not self.user_exists(user_id):
            print(f"Error: User with id {user_id} does not exist.")
            return
        
        if not self.book_exists(book_id):
            print(f"Error: Book with id {book_id} does not exist.")
            return
        
        self.connect()
        try:
            self.cursor.execute('INSERT OR REPLACE INTO user_books (user_id, book_id, progress) VALUES (?, ?, ?)', (user_id, book_id, progress))
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"SQLite error (add_user_book_progress): {e}")
            self.conn.rollback()
        finally:
            self.disconnect()
    
    def get_user_book_progress(self, user_id, book_id):
        if not self.user_exists(user_id):
            print(f"Error: User with id {user_id} does not exist.")
            return None
        
        if not self.book_exists(book_id):
            print(f"Error: Book with id {book_id} does not exist.")
            return None
        
        self.connect()
        try:
            self.cursor.execute('SELECT progress FROM user_books WHERE user_id = ? AND book_id = ?', (user_id, book_id))
            progress = self.cursor.fetchone()
            if progress:
                progress = progress[0]
        except sqlite3.Error as e:
            print(f"SQLite error (get_user_book_progress): {e}")
            progress = None
        finally:
            self.disconnect()
        return progress

    def add_user_note(self, user_id, book_id, note):
        if not self.user_exists(user_id):
            print(f"Error: User with id {user_id} does not exist.")
            return
        
        if not self.book_exists(book_id):
            print(f"Error: Book with id {book_id} does not exist.")
            return
        
        self.connect()
        try:
            self.cursor.execute('INSERT INTO user_notes (user_id, book_id, note) VALUES (?, ?, ?)', (user_id, book_id, note))
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"SQLite error (add_user_note): {e}")
            self.conn.rollback()
        finally:
            self.disconnect()
    
    def get_user_notes(self, user_id, book_id):
        if not self.user_exists(user_id):
            print(f"Error: User with id {user_id} does not exist.")
            return []
        
        if not self.book_exists(book_id):
            print(f"Error: Book with id {book_id} does not exist.")
            return []
        
        self.connect()
        try:
            self.cursor.execute('SELECT note, timestamp FROM user_notes WHERE user_id = ? AND book_id = ?', (user_id, book_id))
            notes = self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"SQLite error (get_user_notes): {e}")
            notes = []
        finally:
            self.disconnect()
        return notes
