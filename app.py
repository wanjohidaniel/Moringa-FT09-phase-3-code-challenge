from database.setup import create_tables
from models.article import Article
from models.author import Author
from models.magazine import Magazine

def main():
    # Initialize the database and create tables
    create_tables()

    # Collect user input
    author_name = input("Enter author's name: ")
    magazine_name = input("Enter magazine name: ")
    magazine_category = input("Enter magazine category: ")
    article_title = input("Enter article title: ")
    article_content = input("Enter article content: ")

    # Create an author
    author = Author(name=author_name)

    # Create a magazine
    magazine = Magazine(name=magazine_name, category=magazine_category)

    # Create an article
    article = Article(title=article_title, content=article_content, author=author, magazine=magazine)

    # Retrieve and print all authors
    authors = Author.get_all()
    print("\nAuthors:")
    for a in authors:
        print(f"ID: {a.id}, Name: {a.name}")

    # Retrieve and print all magazines
    magazines = Magazine.get_all()
    print("\nMagazines:")
    for m in magazines:
        print(f"ID: {m.id}, Name: {m.name}, Category: {m.category}")

    # Retrieve and print all articles
    articles = Article.get_all()
    print("\nArticles:")
    for art in articles:
        print(f"ID: {art.id}, Title: {art.title}, Content: {art.content}, Author: {art.author.name}, Magazine: {art.magazine.name}")

if __name__ == "__main__":
    main()
