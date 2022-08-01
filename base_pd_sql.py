import sqlite3
from sqlite3 import Error
import csv
from datetime import date
import sys
import ctypes
import pprint


kernel32 = ctypes.windll.kernel32
kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)

'''
Colors!
Write a module and import in future.
'''
red_text = '\033[31m'
green_text = '\033[32m'
yellow_text = '\033[33m'
blue_text = '\033[34m'
white_text_on_blue = '\033[37m\033[44m'
marked_text = '\033[43m'
end_text = '\033[0m'
numbers = white_text_on_blue


def main():
    print("SQL")
    connection = create_connection("persons.sqlite")

    create_persons_table = """
        CREATE TABLE IF NOT EXISTS persons (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        date_of_birth DATE,
        place_of_birth TEXT (50),
        passport TEXT (80),
        snils TEXT (11),
        inn TEXT (12),
        address TEXT (80),
        phone TEXT (12),
        email TEXT (256)
        );
        """

    execute_query(connection, create_persons_table)

    
    
    base_structure = [
        'Фамилия Имя Отчество (с учетом РЕГИСТРА)', 
        'Дата рождения dd.mm.yyyy', 
        'Место рождения', 
        'Паспорт (Номер, Кем выдан, Дата выдачи, Код подразделения)', 
        'СНИЛС (только цифры)', 
        'ИНН', 
        'Адрес (Индекс, Регион, Город, Улица, Дом, Квартира)', 
        'Телефон (+7********** несколько через запятую)', 
        'e-mail (несколько через запятую)', 
        'Дата актуальности'
        ]


    pass
    

def create_connection(path):
    connection = None
    try:
        connection = sqlite3.connect(path)
        print("Connection to SQLite DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")
    return connection


def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query executed successfully")
    except Error as e:
        print(f"The error '{e}' occurred")


if __name__ == "__main__":
    main()
    print(green_text + 'Работа программы ЗАВЕРШЕНА' + end_text)