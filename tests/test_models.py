import unittest
from models.author import Author
from models.article import Article
from models.magazine import Magazine
from database.setup import create_tables
from database.connection import get_db_connection

class TestModels(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        create_tables()

    def setUp(self):
        self.conn = get_db_connection()
        self.cursor = self.conn.cursor()
        self.cursor.execute('DELETE FROM articles')
        self.cursor.execute('DELETE FROM authors')
        self.cursor.execute('DELETE FROM magazines')
        self.conn.commit()

    def tearDown(self):
        self.conn.close()

    def test_author_creation(self):
        author = Author(name="John Doe")
        self.assertEqual(author.name, "John Doe")

    def test_article_creation(self):
        author = Author(name="John Doe")
        magazine = Magazine(name="Tech Weekly", category="Technology")
        article = Article(title="Test Title", content="Test Content", author=author, magazine=magazine)
        self.assertEqual(article.title, "Test Title")
        self.assertEqual(article.content, "Test Content")
        self.assertEqual(article.author.name, "John Doe")
        self.assertEqual(article.magazine.name, "Tech Weekly")

    def test_magazine_creation(self):
        magazine = Magazine(name="Tech Weekly", category="Technology")
        self.assertEqual(magazine.name, "Tech Weekly")
        self.assertEqual(magazine.category, "Technology")

    def test_author_articles(self):
        author = Author(name="John Doe")
        magazine = Magazine(name="Tech Weekly", category="Technology")
        article1 = Article(title="Test Title 1", content="Test Content 1", author=author, magazine=magazine)
        article2 = Article(title="Test Title 2", content="Test Content 2", author=author, magazine=magazine)
        articles = author.articles()
        self.assertEqual(len(articles), 2)
        self.assertEqual(articles[0].title, "Test Title 1")
        self.assertEqual(articles[1].title, "Test Title 2")

    def test_author_magazines(self):
        author = Author(name="John Doe")
        magazine1 = Magazine(name="Tech Weekly", category="Technology")
        magazine2 = Magazine(name="Health Monthly", category="Health")
        Article(title="Tech Article", content="Tech Content", author=author, magazine=magazine1)
        Article(title="Health Article", content="Health Content", author=author, magazine=magazine2)
        magazines = author.magazines()
        self.assertEqual(len(magazines), 2)
        self.assertTrue(any(mag.name == "Tech Weekly" for mag in magazines))
        self.assertTrue(any(mag.name == "Health Monthly" for mag in magazines))

    def test_magazine_articles(self):
        author = Author(name="John Doe")
        magazine = Magazine(name="Tech Weekly", category="Technology")
        article1 = Article(title="Test Title 1", content="Test Content 1", author=author, magazine=magazine)
        article2 = Article(title="Test Title 2", content="Test Content 2", author=author, magazine=magazine)
        articles = magazine.articles()
        self.assertEqual(len(articles), 2)
        self.assertEqual(articles[0].title, "Test Title 1")
        self.assertEqual(articles[1].title, "Test Title 2")

    def test_magazine_contributors(self):
        author1 = Author(name="John Doe")
        author2 = Author(name="Jane Smith")
        magazine = Magazine(name="Tech Weekly", category="Technology")
        Article(title="Test Title 1", content="Test Content 1", author=author1, magazine=magazine)
        Article(title="Test Title 2", content="Test Content 2", author=author2, magazine=magazine)
        contributors = magazine.contributors()
        self.assertEqual(len(contributors), 2)
        self.assertTrue(any(author.name == "John Doe" for author in contributors))
        self.assertTrue(any(author.name == "Jane Smith" for author in contributors))

    def test_magazine_article_titles(self):
        author = Author(name="John Doe")
        magazine = Magazine(name="Tech Weekly", category="Technology")
        Article(title="Test Title 1", content="Test Content 1", author=author, magazine=magazine)
        Article(title="Test Title 2", content="Test Content 2", author=author, magazine=magazine)
        titles = magazine.article_titles()
        self.assertEqual(len(titles), 2)
        self.assertIn("Test Title 1", titles)
        self.assertIn("Test Title 2", titles)

    def test_magazine_contributing_authors(self):
        author = Author(name="John Doe")
        magazine = Magazine(name="Tech Weekly", category="Technology")
        Article(title="Test Title 1", content="Test Content 1", author=author, magazine=magazine)
        Article(title="Test Title 2", content="Test Content 2", author=author, magazine=magazine)
        Article(title="Test Title 3", content="Test Content 3", author=author, magazine=magazine)
        contributing_authors = magazine.contributing_authors()
        self.assertEqual(len(contributing_authors), 1)
        self.assertEqual(contributing_authors[0].name, "John Doe")

if __name__ == "__main__":
    unittest.main()
