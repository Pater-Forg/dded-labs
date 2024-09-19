from dataclasses import dataclass
from tabulate import tabulate

# Определение класса Compound
@dataclass
class Compound:
    Name: str
    Formula: str
    MolecularWeight: float
    Density: float
    State: str

# Определение класса Paper
@dataclass
class Paper:
    Author: str
    Journal: str
    Number: int
    Year: int
    Pages: str

# Создаем три экземпляра соединений
compounds = [
    Compound(Name="Вода", Formula="H2O", MolecularWeight=18.015, Density=1000, State="Жидкость"),
    Compound(Name="Метан", Formula="CH4", MolecularWeight=16.04, Density=0.7168, State="Газ"),
    Compound(Name="Натрий хлорид", Formula="NaCl", MolecularWeight=58.44, Density=2165, State="Твердое тело")
]

# Создаем три экземпляра публикаций
papers = [
    Paper(Author="Иванов И.И.", Journal="Химия сегодня", Number=45, Year=2020, Pages="12-25"),
    Paper(Author="Петров П.П.", Journal="Физика для чайников", Number=12, Year=2018, Pages="100-112"),
    Paper(Author="Сидоров С.С.", Journal="Юный химик", Number=3, Year=2019, Pages="50-60")
]

# Вывод информации о хим. соединениях в формате таблицы
compoundsTableHeaders = [
    "Название", "Формула", "Молярная масса, г/моль", "Плотность, кг/м3", "Состояние"
]
print("\nИнформация о хим. соединениях в формате таблицы:")
print(tabulate(compounds, headers=compoundsTableHeaders, tablefmt="grid"))

# Вывод информации о статьях в формате таблицы
papersTableHeaders = [
    "Автор", "Журнал", "Номер журнала", "Год журнала", "Страницы журнала"
]
print("\nИнформация о статьях в виде таблицы:")
print(tabulate(papers, headers=papersTableHeaders, tablefmt="grid"))
