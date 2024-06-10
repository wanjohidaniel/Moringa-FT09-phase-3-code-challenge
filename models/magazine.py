import sqlite3
from models.author import Author
from database.connection import get_db_connection

class Magazine:
    def __init__(self, name, category, id=None):
        self._name = name
        self._category = category
        self._id = id
        if id is None:
            self.save_to_db()

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @property
    def category(self):
        return self._category

    def save_to_db(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO magazines (name, category) VALUES (?, ?)', (self._name, self._category))
        self._id = cursor.lastrowid
        conn.commit()
        conn.close()

    def articles(self):
        from models.article import Article
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT a.id, a.title, a.content, a.author_id, a.magazine_id
            FROM articles a
            WHERE a.magazine_id = ?
        ''', (self.id,))
        articles = [Article(id=row[0], title=row[1], content=row[2], author=row[3], magazine=self) for row in cursor.fetchall()]
        conn.close()
        return articles

    def contributors(self):
        from models.author import Author
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT DISTINCT a.id, a.name
            FROM authors a
            JOIN articles ar ON a.id = ar.author_id
            WHERE ar.magazine_id = ?
        ''', (self.id,))
        authors = [Author(id=row[0], name=row[1]) for row in cursor.fetchall()]
        conn.close()
        return authors

    def article_titles(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT title FROM articles WHERE magazine_id = ?', (self.id,))
        titles = [row[0] for row in cursor.fetchall()]
        conn.close()
        return titles

    def contributing_authors(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT a.id, a.name
            FROM authors a
            JOIN articles ar ON a.id = ar.author_id
            WHERE ar.magazine_id = ?
            GROUP BY a.id
            HAVING COUNT(ar.id) > 2
        ''', (self.id,))
        authors = [Author(id=row[0], name=row[1]) for row in cursor.fetchall()]
        conn.close()
        return authors

    @staticmethod
    def get_all():
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT id, name, category FROM magazines')
        magazines = [Magazine(id=row[0], name=row[1], category=row[2]) for row in cursor.fetchall()]
        conn.close()
        return magazines

    @staticmethod
    def get_by_id(magazine_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT id, name, category FROM magazines WHERE id = ?', (magazine_id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return Magazine(id=row[0], name=row[1], category=row[2])
        else:
            return None
