import time
from datetime import datetime
from flask import Flask, request, jsonify, abort
import requests
from random import choice

app = Flask(__name__)


class Bot:
    def __init__(self, data_model):
        self.model = data_model
        self.commands = {
            'fact': self.fact,
            'popwords': self.popular_words,
            'info': self.info,
            'users': self.users,
            'help': self.help,
            'cat': self.cat,
        }

    def execute(self, cmd):
        args = cmd.split(' ')
        if args[0] in self.commands:
            self.commands[args[0]]()
            return {'ok': True}
        else:
            self.help()
            return {'ok': False, 'msg': 'Command not found!'}

    def fact(self):
        """
        Генерирует случайный факт про кошек
        """
        facts = requests.get('https://cat-fact.herokuapp.com/facts')
        if facts.status_code == 200:
            facts = facts.json()['all']
            self.model.add_msg('Bot', '{}'.format(choice(facts)['text']))

    def popular_words(self):
        """
        Выводит сообщение от бота с популярными словами в чате
        """
        words = {}
        words_list = []
        for item in self.model.data:
            words_line = item['text'].lower().split(' ')
            for word in words_line:
                if not word[len(word) - 1].isalpha():
                    word = word[:len(word) - 1]
                words_list.append(word)

        for word in words_list:
            words[word] = 0
        for word in words_list:
            words[word] += 1

        max_value = 0
        popular_words = ''
        for item in words:
            if words[item] > max_value:
                max_value = words[item]

        for item in words:
            if words[item] == max_value:
                popular_words += "{}, ".format(item)
        self.model.add_msg('Bot', 'Популярные слова в чате: {}. Они были использованы {} раз(а)'.format(
            popular_words[:len(popular_words) - 2], max_value))

    def users(self):
        users = ''
        for user in model.get_all_users():
            users += '{}, '.format(user)
        self.model.add_msg('Bot', 'Пользователи в чате:\n{}'.format(users[:len(users) - 2]))

    def info(self):
        self.model.add_msg('Bot', 'Информация о чате:\n- сообщений: {}\n- пользователей: {}'.format(
            len(model.data), len(model.get_all_users())
        ))

    def help(self):
        commands = ''
        for cmd in self.commands.keys():
            commands += '{}, '.format(cmd)
        self.model.add_msg('Bot', 'Список команд бота:\n{}'.format(commands[:len(commands) - 2]))

    def cat(self):
        # это можно было вынести в отдельный файл, но я оставил тут для удобства отправки
        self.model.add_msg('Bot', """▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄
▐▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▌
▐▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▌
▐▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▌
▐▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓░░░░▓▓░░░░▓▓▓▓▓▓▓▓▓▌
▐▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓░░░░░░░░░░░░░▓▓▓▓▓▓▓▓▌
▐▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓░░░░░░░░░░░░░▓▓▓▓▓▓▓▓▌
▐▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓░░░░░░░░░░░░░▓░░░░▓▓▓▌
▐▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓░░░█▄░░░░▄█░░░░░░░░▓▓▌
▐▓▓▓▓▓▓▓▓▓▓░░░░▓▓▓▓▓▓▓░░░████████░░░░▄▄░░▓▓▌
▐░░░░▓▓▓▓▓▓░░░░▓▓▓▓▓▓▓░░░███▀██▀█░░▄███░░▓▓▌
▐░░░░▓▓▓▓▓▓░░░░▓▓▓▓▓▓▓░░░▐████▀██▄███▀░░░▓▓▌
▐░░░░░▓▓▓░░░░░░▓▓▓░░░▓░░░░▀████████▀░░▄▄░░░▌
▐░░░░░▓▓▓░░░░░░░░░░░░░░░░▄███████▀░░▄███░░░▌
▐░░░░░▓▓▓░░░░░░░░░░░░░░░▄█████████▄███▀░░░░▌
▐░░░░░░░░░░░░░░░░░░░░▄██████████████▀░░░░░░▌
▐░░░░░░░░░░░░░░░░░░▄██████████████▀░░░░░░░░▌
▐░░░░░░░░░░░░░░░░░▐████████████▀░░░░░░░░░░░▌
▐░░░░░░░░░░░░░░░░░█████████████░░░░░░░░░░░░▌
▐░░░░░░░░░░░░░░░░█████████████▌░░░░░░░░░░░░▌
▐░░░░░░░░░░░░░░░██████████████░░░░░░░░░░░░░▌
▐░██▄░░░░░░░▄▄██████████████▀░░░░░░░░░░░░░░▌
▐░▀███▄░░▄███████████████▀▀░░░░░░░░░░░░░░░░▌
▐░░░▀▀█████▀▀░░▒▀███▌███▄░░░░░░░░░░░░░░░░░░▌
▐░░░░░░░░░░░░░░░░░▀██▌████░░░░░░░░░░░░░░░░░▌
▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀""")


class Model:
    def __init__(self):
        self.data = []

    def get_all_users(self):
        unique_users = set()
        for item in self.data:
            unique_users.add(item['name'])
        return unique_users

    def add_msg(self, name, text):
        self.data.append({
            'id': len(model.data),
            'name': name,
            'text': text,
            'timestamp': time.time()
        })


model = Model()
bot = Bot(model)


@app.route("/")
def hello():
    return """
    <h1>Добро пожаловать на сервер нашего Мессенджера!</h1> 
    <a href='/status'>Статус</a> <br>
    <a href='/messages'>Сообщения</a> <br>
    """


@app.route("/status")
def status():
    return jsonify(
        status=True,
        name='Messenger',
        time=datetime.now().strftime('%d.%m.%Y %H:%M:%S'),
        users=len(model.get_all_users()),
        messages_amount=len(model.data),
    )


@app.route("/send", methods=['POST'])
def send():
    data = request.json

    if data['text'][0] == '/':
        return bot.execute(data['text'][1:])
    else:
        model.add_msg(data['name'], data['text'])

    return {'ok': True}


@app.route("/messages")
def messages():
    if 'after_timestamp' in request.args:
        after_timestamp = float(request.args['after_timestamp'])
    else:
        after_timestamp = 0

    # limit = 100
    max_limit = 100
    if 'limit' in request.args:
        limit = int(request.args['limit'])
        if limit > max_limit:
            abort(400, 'too big limit')
    else:
        limit = max_limit

    after_id = 0
    for message in model.data:
        if message['timestamp'] > after_timestamp:
            break
        after_id += 1

    return {'messages': model.data[after_id:after_id+limit]}


if __name__ == '__main__':
    app.run()