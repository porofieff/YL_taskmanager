import sys
import sqlite3

from PyQt5 import uic, QtCore
from PyQt5.QtWidgets import QWidget, QApplication, QLineEdit, QPushButton, QCheckBox, QTableWidgetItem, QListWidget, QListWidgetItem


class Window(QWidget):
    def __init__(self):
        super().__init__()

        self.db_connect = sqlite3.connect("task_db.db")
        self.cursor = self.db_connect.cursor()

        uic.loadUi('taskmanager.ui', self)

        self.add_button.clicked.connect(self.add_task)
        self.save_button.clicked.connect(self.save_data_changes)
        self.del_button.clicked.connect(self.del_complete_task)

        self.update_db()
        
    def add_task(self):
        #print('add_task is work')

        new_task = self.add_line.text()
        ready = '0'
        query = """INSERT INTO tasks (task_title, ready) VALUES (?,?)"""
        data = (new_task, ready)
        self.cursor.execute(query, data)
        self.db_connect.commit()

        self.add_line.setText('')
        self.update_db()

    def del_complete_task(self):
        #print('del_task is work')

        self.cursor.execute("""DELETE FROM tasks WHERE ready = '1'""")
        self.db_connect.commit()

        self.update_db()

    def save_data_changes(self):
        #print('data save is work')

        for i in range(self.task_list.count()):
            item = self.task_list.item(i)
            task = item.text()
            if item.checkState() == QtCore.Qt.Checked:
                query = ("""UPDATE tasks SET ready = '1' WHERE task_title = ?""")
                print('1')
            elif item.checkState() == QtCore.Qt.Unchecked:
                query = ("""UPDATE tasks SET ready = '0' WHERE task_title = ?""")
                print('0')

            self.cursor.execute(query, (task,))

        self.db_connect.commit()

    def update_db(self):
        #print('update is work')

        self.task_list.clear()
        data = self.cursor.execute("""SELECT task_title, ready FROM tasks""").fetchall()
        for task in data:
            task_item = QListWidgetItem(str(task[0]))
            task_item.setFlags(task_item.flags() | QtCore.Qt.ItemIsUserCheckable)
            if str(task[1] )== '1':
                task_item.setCheckState(QtCore.Qt.Checked)
            elif str(task[1]) == '0':
                task_item.setCheckState(QtCore.Qt.Unchecked)
            self.task_list.addItem(task_item)


    def closeEvent(self, event):
        #print('close connection is work')
        self.db_connect.close()
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    wnd = Window()
    wnd.show()
    sys.exit(app.exec())