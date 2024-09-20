from sqlalchemy import create_engine, Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker, declarative_base
import requests
import bibtexparser

# Инициализация базы данных
Base = declarative_base()

# Определение таблицы категорий статей
class ArticleCategory(Base):
    __tablename__ = 'article_categories'
    
    id = Column(Integer, primary_key=True)
    code = Column(String, nullable=False, unique=True)
    title = Column(String, nullable=False)

    articles = relationship('Article', back_populates='category')

# Определение таблицы статей
class Article(Base):
    __tablename__ = 'articles'
    
    id = Column(Integer, primary_key=True)
    author = Column(String, nullable=False)
    title = Column(String, nullable=False)
    journal = Column(String, nullable=False)
    journalNumber = Column(Integer, nullable=False)
    year = Column(Integer, nullable=False)
    pages = Column(String, nullable=False)
    doi = Column(String, nullable=False)
    
    categoryId = Column(Integer, ForeignKey('article_categories.id'), nullable=False)
    category = relationship('ArticleCategory', back_populates='articles')

# Метод для создания и инициализации базы данных
def CreateDatabase():
    engine = create_engine('sqlite:///unit-02/ex-2/articles.db')
    Base.metadata.create_all(engine)
    return engine

# Парсинг данных по DOI и создание объектов статей
def ParseDOI(doi):
    url = f'http://dx.doi.org/{doi}'
    response = requests.get(url, allow_redirects=True, headers={'Accept': 'application/x-bibtex'})
    if response.ok:
        return bibtexparser.loads(response.content).entries[0]
    return None

def PopulateCategories(engine):
    Session = sessionmaker(bind=engine)
    session = Session()

    # Добавление категорий
    if session.query(ArticleCategory).count() > 0:
        print('Таблица категорий уже заполнена')
        return
    
    categories = {
        'ML': 'Machine Learning',
        'EC': 'Electrochemistry',
        'PC': 'Physical Chemistry'
    }

    for code, title in categories.items():
        category = ArticleCategory(code=code, title=title)
        session.add(category)

    session.commit()

# Заполнение базы данных
def PopulateArticles(engine):
    Session = sessionmaker(bind=engine)
    session = Session()

    if session.query(Article).count() > 0:
        print('Таблица статей уже заполнена')
        return

    # Статьи для парсинга
    articlesByCategory = {
        'ML': [
            '10.1016/j.jechem.2024.02.035',
            '10.1016/j.commatsci.2023.112350',
            '10.1016/j.ijhydene.2021.03.132',
            '10.1016/j.electacta.2023.142741'
        ],
        'EC': [
            '10.1149/2754-2734/acff0b',
            '10.1149/2.104203jes',
            '10.1016/j.ijhydene.2006.10.062',
            '10.1016/j.jpowsour.2004.12.067'
        ],
        'PC': [
            '10.3390/pr11102897',
            '10.1016/j.jqsrt.2023.108617',
            '10.1351/PAC-CON-10-09-36',
            '10.1016/j.fluid.2009.01.007',
            '10.1021/ci00003a006'
        ]
    }

    # Парсинг статей и добавление в базу данных
    for categoryCode, dois in articlesByCategory.items():
        for doi in dois:
            parsedArticle = ParseDOI(doi)
            if parsedArticle:
                article = Article(
                    author=parsedArticle['author'],
                    title=parsedArticle['title'],
                    journal=parsedArticle['journal'],
                    journalNumber=parsedArticle['volume'],
                    year=parsedArticle['year'],
                    pages=parsedArticle['pages'],
                    doi=doi,
                    category=session.query(ArticleCategory).filter_by(code=categoryCode).first()
                )
                session.add(article)

    session.commit()

# Вывод всех данных из базы
def PrintAllData(engine):
    Session = sessionmaker(bind=engine)
    session = Session()

    articles = session.query(Article).all()
    for article in articles:
        print(f"{article.author}, {article.journal} {article.journalNumber}({article.year}) {article.pages}, DOI: {article.doi}, Category: {article.category.title}\n")

# Вывод данных по категориям
def PrintDataByCategory(engine, categoryCode):
    Session = sessionmaker(bind=engine)
    session = Session()

    category = session.query(ArticleCategory).filter_by(code=categoryCode).first()
    if category:
        for article in category.articles:
            print(f"{article.author}, {article.journal} {article.journalNumber}({article.year}) {article.pages}, DOI: {article.doi}\n")

# Вывод всех статей за 2023 год
def PrintArticlesByYear(engine, year):
    Session = sessionmaker(bind=engine)
    session = Session()

    articles = session.query(Article).filter_by(year=year).all()
    for article in articles:
        print(f"{article.author}, {article.journal} {article.journalNumber}({article.year}) {article.pages}, DOI: {article.doi}\n")

# Основная функция
if __name__ == '__main__':
    engine = CreateDatabase()
    PopulateCategories(engine)
    PopulateArticles(engine)
    
    print("Все данные в базе данных:")
    PrintAllData(engine)
    
    print("\nСтатьи из категории ML:")
    PrintDataByCategory(engine, 'ML')
    
    print("\nВсе статьи за 2023 год:")
    PrintArticlesByYear(engine, 2023)
