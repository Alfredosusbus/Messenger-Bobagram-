import window
from PyQt5 import QtWidgets, QtCore, QtGui
import requests
from datetime import datetime
import log_window
import os

USER = ""

class Registration(QtWidgets.QMainWindow, log_window.Ui_MainWindow):
    def __init__(self):
        super(Registration, self).__init__()
        self.setupUi(self)

        self.label.setText("")
        self.label_2.setText("Registration")
        self.lineEdit.setPlaceholderText("Enter your Login")
        self.lineEdit_2.setPlaceholderText("Enter your Password")
        self.pushButton.setText("Register")
        self.pushButton_2.setText("Start")
        self.setWindowTitle("Register")

        self.pushButton.clicked.connect(self.reg)
        self.pushButton_2.clicked.connect(self.open_login)

    def open_login(self):
        self.login = Login()
        self.login.show()
        self.hide()

    def reg(self):
        user_nickname = self.lineEdit.text()
        user_password = self.lineEdit_2.text()

        if user_nickname == "":
            self.label.setText("Enter correct login!")
            return

        if user_password == "":
            self.label.setText("Enter correct Password!")
            return

        if len(user_nickname) > 3:
            try:
                response = requests.post(
                    url='http://127.0.0.1:5000/registration',
                    json={
                        'nickname': user_nickname,
                        'password': user_password
                    }
                )
            except Exception as e:
                print("Server not available", e)
                return

            if response.status_code != 200:
                self.label.setText("Registration error!")
                return

            self.label.setText(f"Account {user_nickname} successfully registered!")

            global USER
            USER = user_nickname
        else:
            self.label.setText("Login must have more than 4 symbols!")
            return

        self.open_messenger()
        return

    def open_messenger(self):
        self.messenger = Messenger()
        self.messenger.show()
        self.hide()


class Login(QtWidgets.QMainWindow, log_window.Ui_MainWindow):
    def __init__(self):
        super(Login, self).__init__()
        self.setupUi(self)

        self.label.setText("")
        self.label_2.setText("Log in")
        self.lineEdit.setPlaceholderText("Enter login")
        self.lineEdit_2.setPlaceholderText("Enter password")
        self.pushButton.setText("Log in")
        self.pushButton_2.setText("Register")
        self.setWindowTitle("Log in")

        self.pushButton.clicked.connect(self.login)
        self.pushButton_2.clicked.connect(self.open_reg)

    def open_reg(self):
        self.reg = Registration()
        self.reg.show()
        self.hide()

    def login(self):
        user_nickname = self.lineEdit.text()
        user_password = self.lineEdit_2.text()

        if user_nickname == '':
            self.label.setText("Enter correct login!")
            return

        if user_password == '':
            self.label.setText("Enter correct password!")
            return

        if len(user_nickname) > 0:
            try:
                response = requests.post(
                    url='http://127.0.0.1:5000/login',
                    json={
                        'nickname': user_nickname,
                        'password': user_password
                    }
                )
            except Exception:
                print("Server not available")
                return

            if response.status_code != 200:
                self.label.setText('Authorization error!')
                return

            global USER
            USER = user_nickname
            self.open_messenger()
            return

    def open_messenger(self):
        self.messenger = Messenger()
        self.messenger.show()
        self.hide()


class Messenger(QtWidgets.QMainWindow, window.Ui_MainWindow):
    def __init__(self):
        super(Messenger, self).__init__()
        self.setupUi(self)
        self.after = 0
        self.pushButton.clicked.connect(self.send_message)
        self.textEdit.installEventFilter(self)
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.get_messages)
        self.timer.start(1000)
        self.pushButton_2.clicked.connect(self.exit)
        self.message_history_file = "message_history.txt"
        self.load_message_history()

    def eventFilter(self, obj, event):
        if obj == self.textEdit and event.type() == QtCore.QEvent.KeyPress:
            if event.key() == QtCore.Qt.Key_Return and self.textEdit.hasFocus():
                self.send_message()
                return True
        return super(Messenger, self).eventFilter(obj, event)

    def exit(self):
        self.login = Login()
        self.login.show()
        self.hide()

    def show_messages(self, message):
        item = QtWidgets.QListWidgetItem()
        dt = datetime.fromtimestamp(message['time'])
        if message['name'] == USER:
            item.setTextAlignment(QtCore.Qt.AlignRight)
        item.setText(f"{message['name']} {dt.strftime('%H:%M')}\n{message['text']}")
        self.listWidget.addItem(item)
        
        with open(self.message_history_file, "a") as file:
            file.write(f"{message['name']} {dt.strftime('%H:%M')}\n{message['text']}\n")

    def load_message_history(self):
        if os.path.exists(self.message_history_file):
            with open(self.message_history_file, "r") as file:
                for line in file:
                    if line.strip():
                        self.listWidget.addItem(line.strip())

    def get_messages(self):
        try:
            response = requests.get(url='http://127.0.0.1:5000/messages', params={'after': self.after})
        except Exception as e:
            print(e)
            return
        messages = response.json()['messages']
        for i in range(len(messages)):
            self.show_messages(messages[i])
            self.after = messages[i]['time']
            self.listWidget.scrollToBottom()

    def send_message(self):
        global USER
        name = USER
        text = self.textEdit.toPlainText()
        if len(name) > 0 and len(text) > 0:
            try:
                response = requests.post(url='http://127.0.0.1:5000/send', json={'name': name, 'text': text})
            except Exception as e:
                item = QtWidgets.QListWidgetItem()
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                item.setText('Server not available!\n')
                self.listWidget.addItem(item)
                print(e)
                return

            if response.status_code != 200:
                item = QtWidgets.QListWidgetItem()
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                item.setText('Wrong name or text!\n')
                self.listWidget.addItem(item)
                return

            self.textEdit.clear()


if __name__ == '__main__':
    App = QtWidgets.QApplication([])
    window = Login()
    window.show()
    App.exec()









            
    

