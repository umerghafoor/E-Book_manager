# book_title = book['title']
# book_subtitle   = book['subtitle']
# book_author = book['author_id']
# book_publisher = book['publisher']
# book_pub_date = book['pub_date']
# book_pages = book['pages']
# book_genre = book['genre']
# book_thumbnail = book['thumbnail']
# book_notes = book['notes']


class Book:
    def __init__(self,book_id, title, subtitle, author, publisher, pub_date, pages, genre, thumbnail, notes, path, tags=None):
        self.book_id = book_id
        self.title = title
        self.subtitle = subtitle
        self.author = author
        self.publisher = publisher
        self.pub_date = pub_date
        self.pages = pages
        self.genre = genre
        self.thumbnail = thumbnail
        self.notes = notes
        self.path = path
        self.tags = tags

    def __str__(self):
        return f"Title: {self.title}, Subtitle: {self.subtitle}, Author: {self.author}, Publisher: {self.publisher}, Publication Date: {self.pub_date}, Pages: {self.pages}, Genre: {self.genre}, Thumbnail: {self.thumbnail}, Notes: {self.notes}, "
    
    def __repr__(self):
        return f"Book({self.title}, {self.subtitle}, {self.author}, {self.publisher}, {self.pub_date}, {self.pages}, {self.genre}, {self.thumbnail}, {self.notes})"
    
    def __eq__(self, other):
        return self.path == other.path
    
    def __hash__(self):
        return hash((self.title, self.author))
    
    def to_dict(self):
        return {
            "title": self.title,
            "subtitle": self.subtitle,
            "author": self.author,
            "publisher": self.publisher,
            "pub_date": self.pub_date,
            "pages": self.pages,
            "genre": self.genre,
            "thumbnail": self.thumbnail,
            "notes": self.notes
        }
    
    def get_title(self):
        return self.title
    
    def get_subtitle(self):
        return self.subtitle
    
    def get_author(self):
        return self.author
    
    def get_publisher(self):
        return self.publisher
    
    def get_pub_date(self):
        return self.pub_date
    
    def get_pages(self):
        return self.pages
    
    def get_genre(self):
        return self.genre
    
    def get_thumbnail(self):
        return self.thumbnail
    
    def get_notes(self):
        return self.notes
    
    def get_path(self):
        return self.path
    
    def get_tags(self):
        return self.tags
    
    def get_id(self):
        return self.book_id