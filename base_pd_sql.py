from concurrent.futures.process import _ExecutorManagerThread
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

    table = ('id', 'name', 'date_of_birth_human', 'date_of_birth', 'place_of_birth', 'passport', 'snils', 'inn', 'address', 'phone', 'email', 'actual_date')

    create_persons_table = """
        CREATE TABLE IF NOT EXISTS persons (
            id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,  
            name TEXT (64) NOT NULL,
            date_of_birth_human TEXT (10),
            date_of_birth TEXT (10),
            place_of_birth TEXT (64),
            passport TEXT (256),
            snils TEXT (11),
            inn TEXT (12),
            address TEXT (256),
            phone TEXT (256),
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
    
    print("SQL")
    sql_path = "persons.sqlite"
    connection = create_connection(sql_path)
    cursor = connection.cursor()
    #cursor.execute(create_persons_table)
    execute_query(connection, create_persons_table)
    menu_choise = menu()
    menu_handling(menu_choise, base_structure, table, connection)
    print("Закрываем соединение с базой. Выход.")
    connection.close()


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


def menu_handling(menu_choise, base_structure, table, connection):
    if menu_choise == '1':
        print("Under construction. В работе")
        rec_find(connection)
        pass
        # rec_find(base_file)
    elif menu_choise == '2':
        print("Under construction. Почти закончено")
        pass
        rec_new(base_structure, connection)
        #rec_new(base_file, base_structure)
    elif menu_choise == '3':
        print("Under construction")
        print("Функция изменения записи")
        update_data(base_structure, table, connection)
        pass
        #change_data(base_file, base_structure)
    elif menu_choise == '4':
        select_all(connection)
        print("Under construction. Почти закончено")
        pass
        #print_all_data(base_file)
    elif menu_choise == '0':
        print(green_text + "ВЫХОД из программы" + end_text)
        sys.exit()
    else:
        print("Выберите значение из меню!")
        pass


def rec_find(connection):
    '''Func that recieved basefile name and printed list of finded records'''
    record = input("Введите ФИО для поиска: (с учетом РЕГИСТРА) ").strip()
    query = """SELECT id, name, date_of_birth_human, place_of_birth, passport, snils, inn, address, phone, email, actual_date
                FROM persons 
                WHERE name LIKE '%{}%';""".format(record)
    #print('Запрос на поиск \n', query)
    finded_records = execute_find_query(connection, query)
    #print('rec_find', finded_records)
    print_find_list(finded_records, record)
    return finded_records


def create_connection(path):
    connection = None
    try:
        connection = sqlite3.connect(path)
        print("Connection to SQLite DB successful")
# Add green text
    except Error as e:
        print(f"The error '{e}' occurred")
    return connection


def execute_query(connection, query, data=()):
    cursor = connection.cursor()
    try:
        cursor.execute(query, data)
        connection.commit()
        print("Query executed successfully")
# Add green text
    except Error as e:
        print(f"The error '{e}' occurred")


def rec_new(base_structure, connection):
    data = []
    for y in range(len(base_structure) - 1):
        data_input = input("Введите данные: " + yellow_text + base_structure[y] + end_text + " - ").strip()
        data.append(data_input)
        if y == 0:
            if check_name(data_input, connection):
                print(green_text + 'Имя уникально' + end_text)
            else:
                print(red_text + 'Такое имя уже есть в базе' + end_text)
                print(green_text + "ВЫХОД из программы" + end_text)
                sys.exit()
        if y == 1:
            date_iso = date_convert_to_ISO(data_input)
            data.append(date_iso)
    if len(data) > 1:
        date = date_today()
        data.append(date)
    data = tuple(data)
    print("Данные для внесения в таблицу", yellow_text + '\n'.join(data) + end_text)
    insert = """INSERT INTO persons (
        name, 
        date_of_birth_human,
        date_of_birth,
        place_of_birth,
        passport,
        snils,
        inn,
        address,
        phone,
        email,
        actual_date ) 
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);"""
    execute_query(connection, insert, data)
    

def check_name(data_input, connection):
    query = """SELECT id, 
                    name, 
                    date_of_birth_human, 
                    place_of_birth, passport, 
                    snils, 
                    inn, 
                    address, 
                    phone, 
                    email, 
                    actual_date
                FROM persons 
                WHERE name LIKE '%{}%';""".format(data_input)
    find_result = execute_find_query(connection, query)
    #print(find_result)
    #print(type(find_result))
    if len(find_result) == 0:
        return True
    else:
        return False
    pass


def date_today():
    '''Func that returned today date'''
    today = date.today()
    return str(today)


def date_convert_to_ISO(date_human):
    date_iso = date_human[6:] + '-' + date_human[3:5] + '-' + date_human[0:2]
    return date_iso


def executemany_query(connection, query, list_of_data):
    cursor = connection.cursor()
    try:
        cursor.executemany(query, list_of_data)
        connection.commit()
        print("Query executed successfully")
        # Add green text
    except Error as e:
        print(f"The error '{e}' occurred")


def select_all(connection):
    query = "SELECT * FROM persons"
    all_records = execute_read_query(connection, query)
    for person in all_records:
        print(person)


def execute_read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f"The error '{e}' occurred")


def execute_find_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f"The error '{e}' occurred")
    pass


def update_data(base_structure, table, connection):
    '''Func finds records for update.
    '''
    find_list = rec_find(connection)
    print("update_data", )


    rec_for_change = input('Введите ' + numbers + ' № ' + end_text + ' записи для изменения - ' + blue_text).strip()
    print(end_text, end='')
    print()
    print('find_list', find_list)
    for rec in find_list:
        if rec_for_change == str(rec[0]):
            print(end_text, end='')
            print(red_text + 'Изменить запись???' + end_text, yellow_text + str(rec) + end_text)
            choise = input('Напишите ' + red_text + 'ДА' + end_text + ' или ' + green_text + 'НЕТ' + end_text + ' - ' + yellow_text).strip()
            print(end_text, end='')
            print()
            if choise.lower() == 'да':
                change_record(rec, base_structure, table, connection)
            else:
                print('Не меняем записи')
        else:
            continue


def change_record(record_for_change, base_structure, table, connection):
    '''Func '''
    print('record_for_change', record_for_change)
    new_record = list(record_for_change)
    print('new_record', new_record)
    for y in range(1, len(base_structure)):
        print("ПРОВЕРЬТЕ данные: " + base_structure[y-1])
        print(yellow_text + new_record[y] + end_text)
        print()
        choise = input("Изменить данные? Введите " + red_text + "ДА" + end_text + " или " + green_text + "НЕТ" + end_text + " - " + yellow_text).strip()
        print(end_text, end='')
        print()
        if choise.lower() == 'да':
            new_data = (input('Введите данные: '+ base_structure[y-1] + ' - ').strip(),)
            query = """UPDATE persons SET {} = ? WHERE id = {};""".format(table[y], record_for_change[0])
            execute_query(connection, query, new_data)
        else:
            continue


def print_find_list(find_list, record):
    '''Func recieved list of finded records and record that need to find.
    Printed heads.
    For rec in base printed index of finded record and finded record.
    if record not in base, print notice.
    '''
    if len(find_list) > 0:
        print()
        print(numbers + ' № ' + end_text + '     Запись' + '\n')
        for rec in range(len(find_list)):
            print(numbers + ' ' + str(find_list[rec][0]) + ' ' + end_text, ' ', end='')
            pprint.pprint(find_list[rec][1:], indent=4, width=100)
            print()
    else:
        print('\nЗапись', marked_text + record + end_text, red_text + 'НЕ НАЙДЕНА' + end_text)
        print(green_text + 'Работа программы ЗАВЕРШЕНА' + end_text)
        sys.exit()


if __name__ == "__main__":
    main()
    print(green_text + 'Работа программы ЗАВЕРШЕНА' + end_text)