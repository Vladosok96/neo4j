# -*- coding: cp1251 -*-

from neo4j import GraphDatabase
import PySimpleGUI as sg


def bool_to_YN(value):
    if value:
        return "����"
    else:
        return "���"


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

    # ���������� ��������� ����������
    layout = [[sg.Text('��� ��������'), sg.Input()],
              [sg.Text('��� ������'), sg.Combo(["������ �������", "������ �����", "����� � �������"], default_value="������ �������")],
              [sg.Text('��������� �� �/�'), sg.Checkbox("")],
              [sg.Text('��� ��������'), sg.Combo(["������������", "��������������", "����������"], default_value="������������")],
              [sg.Text('���������� �� ���������'), sg.Checkbox("")],
              [sg.Text('���. �������:')],
              [sg.Combo(["���������� ����� ���������", "����� ������� ������",
                         "���������������� ������ �� ������� � ���� ������", "������",
                         "������ ��� �������� ������������", "������ ��� �����������",
                         "����������� ������� ������", "������������ ���������"], default_value="���������� ����� ���������")],
              [sg.Combo(["���������� ����� ���������", "����� ������� ������",
                         "���������������� ������ �� ������� � ���� ������", "������",
                         "������ ��� �������� ������������", "������ ��� �����������",
                         "����������� ������� ������", "������������ ���������"], default_value="����� ������� ������")],
              [sg.Button('���������'), sg.Button('�����')]]

    # �������� ����
    window = sg.Window('���������� ������ ��������', layout)

    # ���� �������
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == '�����':  # �������� ���� ��� ������� �� ������ ������
            app.query("""MATCH (ee) DETACH DELETE ee""")
            app.close()
            break

        if event == '���������':  # ������� �� ������ ��������
            if values[0] != '':
                query = 'Create (cleaner:Cleaner {name: "' + values[0] + '", cleaning_type: "' + values[1] + '", remote_control: "' + bool_to_YN(values[4]) + '"}), '
                if values[2]:
                    query += '(charger:Charger {name: "' + values[0] + 'Charger"}), '
                query += '(sensor:Sensor {name: "' + values[3] + '"}), (main_function:MainFunction {name: "������"}), (addition_function1:AdditionFunction1 {name:"' + values[5] + '"}), (addition_function2:AdditionFunction2 {name:"' + values[6] + '"})'
                if values[2]:
                    query += ', (charger)-[:��������_������]->(cleaner)'
                query += ', (sensor)-[:��������_������]->(cleaner), (main_function)-[:��������_�������_��������]->(cleaner), (addition_function1)-[:��������_��������������_��������]->(cleaner), (addition_function2)-[:��������_��������������_��������]->(cleaner)'

                app.query(query)
                print(values)

    window.close()
