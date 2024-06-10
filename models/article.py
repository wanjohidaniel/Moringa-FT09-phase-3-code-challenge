import sqlite3
from database.connection import get_db_connection
from models.author import Author
from models.magazine import Magazine

class Article:
    def __init__(self, title, content, author, magazine, author_id=None, id=None):
        self._title = title
        self._content = content
        self._author = author
        self._magazine = magazine
        self._author_id = author_id
        self._id = id
        if id is None:
            self.save_to_db()

    @property
    def id(self):
        return self._id

    @property
    def title(self):
        return self._title

    @property
    def content(self):
        return self._content

    @property
    def author(self):
        return self._author

    @property
    def magazine(self):
        return self._magazine

    @property
    def author_id(self):
        return self._author_id

    def save_to_db(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO articles (title, content, author_id, magazine_id) VALUES (?, ?, ?, ?)',
            (self._title, self._content, self._author.id, self._magazine.id)
        )
        self._id = cursor.lastrowid
        conn.commit()
        conn.close()

    @staticmethod
    def get_all():
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT id, title, content, author_id, magazine_id FROM articles')
        articles = []
        for row in cursor.fetchall():
            author = Author.get_by_id(row[3])
            magazine = Magazine.get_by_id(row[4])
            articles.append(Article(id=row[0], title=row[1], content=row[2], author=author, magazine=magazine))
        conn.close()
        return articles

    @staticmethod
    def get_by_id(article_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT id, title, content, author_id, magazine_id FROM articles WHERE id = ?', (article_id,))
        row = cursor.fetchone()
        if row:
            author = Author.get_by_id(row[3])
            magazine = Magazine.get_by_id(row[4])
            article = Article(id=row[0], title=row[1], content=row[2], author=author, magazine=magazine)
        else:
            article = None
        conn.close()
        return article
