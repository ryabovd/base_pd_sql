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
    sql_path = "persons.sqlite"
    connection = create_connection(sql_path)
    table = [
        'name',
        'date_of_birth_human',
        'date_of_birth',
        'place_of_birth',
        'passport',
        'snils',
        'inn',
        'address',
        'phone',
        'email',
        'actual_date'
    ]
    create_persons_table = """
        CREATE TABLE IF NOT EXISTS persons (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        date_of_birth_human TEXT (10),
        date_of_birth TEXT (10),
        place_of_birth TEXT (50),
        passport TEXT (80),
        snils TEXT (11),
        inn TEXT (12),
        address TEXT (80),
        phone TEXT (12),
        email TEXT (256),
        actual_date TEXT (10)
        );
        """
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
    
    #cursor = connection.cursor()
    execute_query(connection, create_persons_table)
    menu_choise = menu()
    menu_handling(menu_choise, base_structure, connection)



def menu():
    '''
    Menu function
    '''
    menu_choise = 'выбор не сделан'
    print("\033[4m{}\033[0m".format("\nМЕНЮ"))
    print(numbers + " " + "1" + " " + end_text + " - Найти запись")
    print(numbers + " " + "2" + " " + end_text + " - Внести записи")
    print(numbers + " " + "3" + " " + end_text + " - Изменить запись")
    print(numbers + " " + "4" + " " + end_text + " - Напечатать все записи")
    print(numbers + " " + "0" + " " + end_text + " - Выход \n")
    menu_choise = input("Выберите " + numbers + "пункт" + end_text + " меню - " + blue_text).strip()
    print(end_text, end='')
    while menu_choise not in ['0', '1', '2', '3', '4']:
        menu_choise = input(red_text + "Неправильный выбор\n" + end_text + "Выберите " + numbers + "пункт" + end_text + " меню - " + blue_text).strip()
    return menu_choise

def menu_handling(menu_choise, base_structure, connection):
    if menu_choise == '1':
        print("Under construction")
        pass
        # rec_find(base_file)
    elif menu_choise == '2':
        print("Under construction")
        pass
        rec_new(base_structure, connection)
        #rec_new(base_file, base_structure)
    elif menu_choise == '3':
        print("Under construction")
        pass
        #change_data(base_file, base_structure)
    elif menu_choise == '4':
        print("Under construction")
        pass
        #print_all_data(base_file)
    elif menu_choise == '0':
        print(green_text + "ВЫХОД из программы" + end_text)
        sys.exit()
    else:
        print("Выберите значение из меню!")
        pass

"""def rec_find(base_file):
    '''Func that recieved basefile name and printed list of finded records'''
    record = input("Введите ФИО для поиска: (с учетом РЕГИСТРА) ").strip()
    base_list = base_file_read(base_file)
    find_list = get_find_list(base_list, record)
    print_find_list(find_list, record)
    return find_list"""

def test_list_of_data():
    list_of_data = get_list_of_data()
    for rec in list_of_data:
        if len(rec) < 11:
            print(rec)
    base_file = "base_pd.csv"
    base = base_file_read(base_file)
    i = 1
    for rec in base:
        rec = [i] + rec
        list_of_data.append(tuple(rec))
        i += 1
    return list_of_data


def create_connection(path):
    connection = None
    try:
        connection = sqlite3.connect(path)
        print("Connection to SQLite DB successful")
        # Add green text
    except Error as e:
        print(f"The error '{e}' occurred")
    return connection


def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query executed successfully")
        # Add green text
    except Error as e:
        print(f"The error '{e}' occurred")


def rec_new(base_structure, connection):
    data = []
    for y in range(len(base_structure) - 1):
        data_input = input("Введите данные: " + base_structure[y] + " - ").strip()
        data.append(data_input)
        if y == 1:
            date_iso = date_convert_to_ISO(data_input)
            data.append(date_iso)
    if len(data) > 1:
        date = date_today()
        data.append(date)
    data = tuple(data)
    print("Данные для внесения в таблицу", data)
    insert = 'INSERT INTO persons({}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}) VALUES{};'.format('name', 
                                                                                                'date_of_birth_human', 
                                                                                                'date_of_birth', 
                                                                                                'place_of_birth', 
                                                                                                'passport', 
                                                                                                'snils', 
                                                                                                'inn', 
                                                                                                'address', 
                                                                                                'phone', 
                                                                                                'email', 
                                                                                                'actual_date', 
                                                                                                data)
    execute_query(connection, insert)
    

    def check_name(data_input, base_file):
        record = False
        data = base_file_read(base_file)
        for rec in data:
            if rec[0] == data_input:
                record = True
                return record
            else:
                continue
        return record


def date_today():
    '''Func that returned today date'''
    today = date.today()
    return str(today)


def date_convert_to_ISO(date_human):
    date_iso = date_human[6:] + '-' + date_human[3:5] + '-' + date_human[0:2]
    return date_iso


def get_list_of_data():
    list_of_data = []
    base_file = "base_pd.csv"
    base = base_file_read(base_file)
    i = 1
    for rec in base:
        rec = [i] + rec
        list_of_data.append(tuple(rec))
        i += 1
    return list_of_data


def base_file_read(base_file):
    '''Func that reads csv file (delimiter is ';') and returns a list of lists of strings'''
    with open(file=base_file, mode='r', encoding='utf-8') as base:
        lines = csv.reader(base, delimiter=';')
        base_list = list(lines)
    return base_list


def executemany_query(connection, query, list_of_data):
    cursor = connection.cursor()
    try:
        cursor.executemany(query, list_of_data)
        connection.commit()
        print("Query executed successfully")
        # Add green text
    except Error as e:
        print(f"The error '{e}' occurred")


if __name__ == "__main__":
    main()
    print(green_text + 'Работа программы ЗАВЕРШЕНА' + end_text)