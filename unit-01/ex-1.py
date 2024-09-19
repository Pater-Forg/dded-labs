import sqlite3 as sql
from pprint import pprint

# Подключаемся к БД
dbConnection = sql.Connection("./unit-01/unit-01.db")

# Получаем курсор
dbCursor = dbConnection.cursor()

# Создаем таблицу Paper
dbCursor.execute(
    "CREATE TABLE IF NOT EXISTS Paper(author, journal, volume, year, pages, pub_type, doi)"
)

# Заполняем таблицу
dbCursor.execute(
    """
    INSERT INTO Paper VALUES
    ('Winifred Watsica', 'Xiphias arca canto aliquam crux', 12, 2015, 23, 'Original Research', 'doi:10.1080/02626667.2015.1623456'),
    ('Leonid Gromov', 'Carcharodon carcharias ultra paludem imperiosus', 9, 2018, 19, 'Case Study', 'doi:10.1080/02626667.2018.1854921'),
    ('Mariya Ivanova', 'Delphinus delphis e valle clarus', 11, 2021, 30, 'Technical Note', 'doi:10.1080/02626667.2021.1930487'),
    ('Igor Sokolov', 'Octopus vulgaris per collum invisibilis', 18, 2022, 25, 'Research Letter', 'doi:10.1080/02626667.2022.2043278'),
    ('Veronika Petrovna', 'Sphyrna mokarran inter astrum opulentia', 17, 2024, 21, 'Short Communication', 'doi:10.1080/02626667.2024.2124567')
    """
)

# Выбираем все записи из таблицы
result = dbCursor.execute(
    "SELECT * FROM Paper"
)
print('All rows:')
pprint(result.fetchall())

# Выбираем только те записи, у которых год публикации больше 2020
result = dbCursor.execute(
    "SELECT * FROM Paper WHERE year > 2020"
)
print('\nYear > 2020:')
pprint(result.fetchall())