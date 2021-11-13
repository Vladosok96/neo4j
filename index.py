# -*- coding: cp1251 -*-

from neo4j import GraphDatabase
import PySimpleGUI as sg


def bool_to_YN(value):
    if value:
        return "Есть"
    else:
        return "Нет"


class App:

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        # Don't forget to close the driver connection when you are finished with it
        self.driver.close()

    def query(self, query):
        with self.driver.session() as session:
            session.read_transaction(self._query, query)

    @staticmethod
    def _query(tx, query):
        tx.run(query)


if __name__ == "__main__":
    # Aura queries use an encrypted connection using the "neo4j+s" URI scheme
    uri = "neo4j+s://3ab69a9f.databases.neo4j.io:7687"
    user = "neo4j"
    password = "pHgWsI59E-gLjENUMh1ujWOlsznwJMc4CzWCzQYQXyQ"
    app = App(uri, user, password)

    # Добавление элементов интерфейса
    layout = [[sg.Text('Имя пылесоса'), sg.Input()],
              [sg.Text('Тип уборки'), sg.Combo(["Только влажная", "Только сухая", "Сухая и влажная"], default_value="Только влажная")],
              [sg.Text('Установка на З/У'), sg.Checkbox("")],
              [sg.Text('Тип датчиков'), sg.Combo(["Инфракрасные", "Ультразвуковые", "Оптические"], default_value="Инфракрасные")],
              [sg.Text('Управление со смартфона'), sg.Checkbox("")],
              [sg.Text('Доп. функции:')],
              [sg.Combo(["Построение карты помещения", "Режим быстрой уборки",
                         "Программирование уборки по времени и дням недели", "Таймер",
                         "Сигнал при разрядке аккумулятора", "Сигнал при застревании",
                         "Ограничение времени уборки", "Ароматизация помещения"], default_value="Построение карты помещения")],
              [sg.Combo(["Построение карты помещения", "Режим быстрой уборки",
                         "Программирование уборки по времени и дням недели", "Таймер",
                         "Сигнал при разрядке аккумулятора", "Сигнал при застревании",
                         "Ограничение времени уборки", "Ароматизация помещения"], default_value="Режим быстрой уборки")],
              [sg.Button('Отправить'), sg.Button('Выйти')]]

    # Создание окна
    window = sg.Window('Добавление робота пылесоса', layout)

    # Цикл событий
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Выйти':  # Закрытие окна или нажатие на кнопку выхода
            app.query("""MATCH (ee) DETACH DELETE ee""")
            app.close()
            break

        if event == 'Отправить':  # Нажатие на кнопку отправки
            if values[0] != '':
                query = 'Create (cleaner:Cleaner {name: "' + values[0] + '", cleaning_type: "' + values[1] + '", remote_control: "' + bool_to_YN(values[4]) + '"}), '
                if values[2]:
                    query += '(charger:Charger {name: "' + values[0] + 'Charger"}), '
                query += '(sensor:Sensor {name: "' + values[3] + '"}), (main_function:MainFunction {name: "Уборка"}), (addition_function1:AdditionFunction1 {name:"' + values[5] + '"}), (addition_function2:AdditionFunction2 {name:"' + values[6] + '"})'
                if values[2]:
                    query += ', (charger)-[:Является_частью]->(cleaner)'
                query += ', (sensor)-[:Является_частью]->(cleaner), (main_function)-[:Является_главной_функцией]->(cleaner), (addition_function1)-[:Является_дополнительной_функцией]->(cleaner), (addition_function2)-[:Является_дополнительной_функцией]->(cleaner)'

                app.query(query)
                print(values)

    window.close()
