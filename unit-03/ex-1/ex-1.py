import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from scipy.optimize import curve_fit
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
import re
from tabulate import tabulate
import numpy as np

def r2_score(y_true, y_pred):
    # Сумма квадратов остатка (SSR)
    ss_res = np.sum((y_true - y_pred) ** 2)
    
    # Сумма квадратов отклонений от среднего (SST)
    ss_tot = np.sum((y_true - np.mean(y_true)) ** 2)
    
    # Коэффициент детерминации R^2
    r2 = 1 - (ss_res / ss_tot)
    
    return r2


# Заданная функция теплоемкости
def heat_capacity_function(T: float, a, b, c, d) -> float:
    return a + b * 1e-3 * T + c * 1e5 * T ** (-2.) + d * 1e-6 * T ** 2

# Функция для аппроксимации конкретной функцией
def fit_custom_function(x, y):
    # Начальные приближения для параметров
    initial_guess = [1, 1, 0, 0]
    
    # Подбор параметров с помощью curve_fit
    params, covariance = curve_fit(heat_capacity_function, x, y, p0=initial_guess)

    return params

# Функция для построения графиков
def plot_data_with_fit(temperatures, heat_capacities, fit_func, params, substance_name, r2):
    # Параметры графика
    plt.scatter(temperatures, heat_capacities, label=f'{substance_name} data', marker='o')
    plt.plot(temperatures, fit_func(temperatures, *params), label=f'{substance_name} fit, R²={r2:.4f}')
    plt.xlabel('T (K)')
    plt.ylabel('Cp (J/(mol*K))')
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')


# Базовый класс для декларативных классов
Base = declarative_base()

# Определение таблицы Compound
class Compound(Base):
    __tablename__ = 'compound'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    formula = Column(String, nullable=False)

    # Один к одному: связь с таблицей Thermodynamic
    thermodynamic = relationship("Thermodynamic", uselist=False, back_populates="compound")

# Определение таблицы Thermodynamic
class Thermodynamic(Base):
    __tablename__ = 'thermodynamic'

    id = Column(Integer, primary_key=True, autoincrement=True)
    formula = Column(String, nullable=False)
    delta_ho_298 = Column(Float, nullable=False)
    so_298 = Column(Float, nullable=False)
    t_min = Column(Float, nullable=False)
    t_max = Column(Float, nullable=False)
    a = Column(Float, nullable=False)
    b = Column(Float, nullable=False)
    c = Column(Float, nullable=False)
    d = Column(Float, nullable=False)

    # Связь с таблицей Compound
    compound_id = Column(Integer, ForeignKey('compound.id'))
    compound = relationship("Compound", back_populates="thermodynamic")

# Функция для извлечения названия и формулы из имени файла
def extract_name_and_formula(filename):
    # Используем регулярное выражение для извлечения названия и формулы
    match = re.match(r"(.+?) \((.+?)\)", filename)
    if match:
        name = match.group(1).strip()
        formula = match.group(2).strip()
        return name, formula
    else:
        raise ValueError(f"Неверный формат названия файла: {filename}")
    
# Функция для извлечения и вывода данных из таблиц
def print_data_from_tables(engine):
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        # Извлекаем все данные из таблицы Compound
        compounds = session.query(Compound).all()

        # Если есть данные, выводим их
        if compounds:
            print("\nТаблица Compound:")
            # Преобразуем в удобный для вывода формат
            compound_data = [[c.id, c.name, c.formula] for c in compounds]
            print(tabulate(compound_data, headers=["ID", "Name", "Formula"], tablefmt="grid"))

        # Извлекаем все данные из таблицы Thermodynamic
        thermodynamics = session.query(Thermodynamic).all()

        if thermodynamics:
            print("\nТаблица Thermodynamic:")
            # Преобразуем в удобный для вывода формат
            thermo_data = [[
                t.id, t.formula, t.delta_ho_298, t.so_298, t.t_min, t.t_max, t.a, t.b, t.c, t.d, t.compound_id
            ] for t in thermodynamics]
            print(tabulate(thermo_data, headers=["ID", "Formula", "Delta Ho(298)", "S(298)", "T(min)", "T(max)", "a", "b", "c", "d", "Compound ID"], tablefmt="grid"))

    finally:
        session.close()

# Главная функция для обработки и визуализации
def main():
    root_folder = 'unit-03\\ex-1\\data'
    # Список файлов с данными
    files = [x for x in os.listdir(root_folder) if x.endswith('.csv')]
    plt.figure(figsize=(15, 6))

    # Создаем подключение к базе данных SQLite (можно заменить на другую БД, например, PostgreSQL)
    engine = create_engine('sqlite:///unit-03/ex-1/unit-03.db')

    # Пересоздание всех таблиц
    Base.metadata.drop_all(engine)  # Удаление существующих таблиц
    Base.metadata.create_all(engine)  # Создание новых таблиц

    # Создаем сессию для взаимодействия с базой данных
    Session = sessionmaker(bind=engine)
    session = Session()

    # Обработка каждого файла
    for file in files:
        # Чтение данных
        data = pd.read_csv(f'{root_folder}\\{file}')
        # Перевод в Дж/Мол/К
        data['Cp(cal/mol/K)'] *= 4.1868
        
        # Фильтрация данных в диапазоне 298-2000K
        mask = (data['T (K)'] >= 298) & (data['T (K)'] <= 2000)
        temperatures_filtered = data['T (K)'][mask]
        heat_capacities_filtered = data['Cp(cal/mol/K)'][mask]

        # Аппроксимация конкретной функцией
        params = fit_custom_function(temperatures_filtered, heat_capacities_filtered)
        
        # Предсказание значений теплоемкости по аппроксимированной функции
        heat_capacity_pred = heat_capacity_function(temperatures_filtered, *params)

        # Оценка R^2
        r2 = r2_score(heat_capacities_filtered, heat_capacity_pred)

        # Название вещества (берем из имени файла)
        name, formula = extract_name_and_formula(file)

        # Построение графика
        plot_data_with_fit(temperatures_filtered, heat_capacities_filtered, heat_capacity_function, params, formula, r2)

        # Добавляем данные в таблицу Compound
        compound = Compound(name=name, formula=formula)
        session.add(compound)
        session.commit()

        # Ищем строку, где T(K) == 298 для получения delta_ho_298 и so_298
        row_298 = data.loc[data['T (K)'] == 298]

        # Извлекаем нужные значения при T = 298
        delta_ho_298 = row_298['dH (kcal/mol)'].values[0]
        so_298 = row_298['S(cal/mol/K)'].values[0]
        # Получаем максимальную и минимальную температуры
        t_min = temperatures_filtered.min()
        t_max = temperatures_filtered.max()

        # Параметры функции аппроксимации
        a, b, c, d = params

        # Добавляем данные в таблицу Thermodynamic
        thermodynamic = Thermodynamic(
            formula=formula,
            delta_ho_298=delta_ho_298,
            so_298=so_298,
            t_min=t_min,
            t_max=t_max,
            a=a,
            b=b,
            c=c,
            d=d,
            compound_id=compound.id  # Связываем с compound через ForeignKey
        )
        session.add(thermodynamic)
        session.commit()

    # Отображение графика
    plt.title('Теплоемкость от температуры')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('unit-03\\ex-1\\plot.png')

    # Выводим данные
    print_data_from_tables(engine)

# Запуск программы
if __name__ == "__main__":
    main()
