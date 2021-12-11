from neo4j import GraphDatabase
# import logging
# from neo4j.exceptions import ServiceUnavailable
import PySimpleGUI as sg


class App:

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        # Don't forget to close the driver connection when you are finished with it
        self.driver.close()

    def query(self, text):
        with self.driver.session() as session:
            result = session.read_transaction(self._query, text)
            # print(result)
            return result

    @staticmethod
    def _query(tx, text):
        result = tx.run(text)
        return [row["name"] for row in result]
   


if __name__ == "__main__":
    # Aura queries use an encrypted connection using the "neo4j+s" URI scheme
    uri = "neo4j+s://f5772c29.databases.neo4j.io"
    user = "neo4j"
    password = "YGi1DC9ZqFQWFOvKrgiDCqUbmWgfCjuGRjUnKXS2y_g"
    app = App(uri, user, password)
    screens = app.query("MATCH (sc:Screen)-[sem:Semantic]-(scs) WHERE sem.name = 'Является разновидностью' return scs.name AS name;")
    interfaceObj = app.query("MATCH (ob:Object)-[sem:Semantic]-(obs) WHERE sem.name = 'Является разновидностью' return obs.name AS name;")

    layout = [
        # [sg.Button('Обновить')],
        [sg.Text('Сценарий поведения'), sg.Button('С регистрацией'), sg.Button('Без регистрации')],
        [sg.Text('Экраны:')],
        [sg.Combo(screens, default_value=screens[0]), sg.Button('Искать экран')],
        [sg.Text('Элементы интерфейса:')],
        [sg.Combo(interfaceObj, default_value=interfaceObj[0]), sg.Button('Искать элемент')],
        [sg.Output(size=(88, 20))],
        [sg.Button('Выйти')]
    ]
    window = sg.Window('Bruh neo4j', layout)
    while True:                             # The Event Loop
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'Выйти'):
            break
        # elif event == 'Обновить':
        #     window = sg.Window('File Compare', layout)
        elif event == 'Искать экран':
            screen = app.query(f"MATCH (sc)-[sem:Semantic]-(events) WHERE sem.name = 'Относится к' AND sc.name = '{values[0]}' return events.name AS name;")
            ev = app.query(f"MATCH (sc)-[sem:Semantic]-(events) WHERE sem.name = 'Относится к' AND sc.name = '{values[0]}' return events.event AS name;")
            print(f'События экрана {values[0]}:')
            for i in range(len(screen)):
                print('  ' + screen[i] + ' (' + ev[i] + ')')
            print()
        elif event == 'Искать элемент':
            screen = app.query(
                f"MATCH (sc)-[sem:Semantic]-(events) WHERE sem.name = 'Отслеживает' AND sc.name = '{values[1]}' return events.name AS name;")
            ev = app.query(
                f"MATCH (sc)-[sem:Semantic]-(events) WHERE sem.name = 'Отслеживает' AND sc.name = '{values[1]}' return events.event AS name;")
            print(f'События объекта {values[1]}:')
            for i in range(len(screen)):
                print('  ' + screen[i] + ' (' + ev[i] + ')')
            print()
        elif event == 'С регистрацией':
            print('Вывод сценария заказа с регистрацией:\n  ', end='')
            path = ['Категории']
            print(path[-1], end='')
            while len(app.query(f"MATCH (sc)-[sem:Semantic]->(scs) WHERE sc.name = '{path[-1]}' AND '1' in sem.script return scs.name AS name;")) > 0:
                path.append(app.query(f"MATCH (sc)-[sem:Semantic]->(scs) WHERE sc.name = '{path[-1]}' AND '1' in sem.script return scs.name AS name;")[0])
                print(' -> ' + path[-1], end='')
            print('\n')
        elif event == 'Без регистрации':
            print('Вывод сценария заказа без регистрации:\n  ', end='')
            path = ['Категории']
            print(path[-1], end='')
            while len(app.query(f"MATCH (sc)-[sem:Semantic]->(scs) WHERE sc.name = '{path[-1]}' AND '2' in sem.script return scs.name AS name;")) > 0:
                path.append(app.query(f"MATCH (sc)-[sem:Semantic]->(scs) WHERE sc.name = '{path[-1]}' AND '2' in sem.script return scs.name AS name;")[0])
                print(' -> ' + path[-1], end='')
            print('\n')
    
    app.close()