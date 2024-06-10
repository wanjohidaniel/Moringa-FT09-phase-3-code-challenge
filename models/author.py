# models/author.py
from database.connection import get_db_connection

class Author:
    def __init__(self, name, id=None):
        self._name = name
        self._id = id
        if id is None:
            self.save_to_db()

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    def save_to_db(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO authors (name) VALUES (?)', (self._name,))
        self._id = cursor.lastrowid
        conn.commit()
        conn.close()

    def articles(self):
      from models.article import Article
      from models.magazine import Magazine
      with self._get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT id, title, content, magazine_id FROM articles WHERE author_id = ?', (self._id,))
        articles = [Article(id=row[0], title=row[1], content=row[2], author=self, magazine=Magazine.get_by_id(row[3])) for row in cursor.fetchall()]
      return articles


    def magazines(self):
        from models.magazine import Magazine
        with self._get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT DISTINCT magazines.id, magazines.name, magazines.category '
                           'FROM articles '
                           'JOIN magazines ON articles.magazine_id = magazines.id '
                           'WHERE articles.author_id = ?', (self._id,))
            magazines = [Magazine(id=row[0], name=row[1], category=row[2]) for row in cursor.fetchall()]
        return magazines

    @staticmethod
    def get_all():
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT id, name FROM authors')
            authors = [Author(id=row[0], name=row[1]) for row in cursor.fetchall()]
        return authors

    @staticmethod
    def get_by_id(author_id):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT id, name FROM authors WHERE id = ?', (author_id,))
            row = cursor.fetchone()
            if row:
                author = Author(id=row[0], name=row[1])
            else:
                author = None
        return author

    def _get_db_connection(self):
        return get_db_connection()
