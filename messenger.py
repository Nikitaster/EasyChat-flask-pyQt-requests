from datetime import datetime

import requests
from PyQt5 import QtWidgets, QtCore

from clientui import Ui_MainWindow


class Messenger(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, url):
        super().__init__()
        self.setupUi(self)

        self.url = url
        self.after_timestamp = -1

        self.sendButton.pressed.connect(self.button_pressed)

        self.load_messages()

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_messages)
        self.timer.start(1000)

    def pretty_print(self, message):
        """
        2020/09/08 10:00:23  Nick
        Text

        """
        dt = datetime.fromtimestamp(message['timestamp'])
        dt = dt.strftime('%Y/%m/%d %H:%M:%S')
        first_line = dt + '  ' + message['name']
        self.messagesBrowser.append(first_line)
        self.messagesBrowser.append(message['text'])
        self.messagesBrowser.append('')
        self.messagesBrowser.repaint()

    def update_messages(self):
        response = None

        try:
            response = requests.get(
                self.url + '/messages',
                params={'after_timestamp': self.after_timestamp}
            )
        except:
            pass

        if response and response.status_code == 200:
            messages = response.json()['messages']
            for message in messages:
                self.pretty_print(message)
                self.after_timestamp = message['timestamp']

            return messages

    def load_messages(self):
        while self.update_messages():
            pass

    def button_pressed(self):
        name = self.nameInput.text()
        text = self.textInput.toPlainText()
        data = {'name': name, 'text': text}

        response = None
        try:
            response = requests.post(self.url + '/send', json=data)
        except:
            pass

        if response and response.status_code:
            self.textInput.clear()
            self.textInput.repaint()
        else:
            self.messagesBrowser.append('При отправке произошла ошибка')
            self.messagesBrowser.append('')
            self.messagesBrowser.repaint()


app = QtWidgets.QApplication([])
window = Messenger('http://127.0.0.1:5000/')
window.show()
app.exec_()
