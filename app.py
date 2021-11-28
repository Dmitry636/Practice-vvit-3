import requests

from flask import Flask, render_template, request, redirect

import psycopg2

# создание приложение
app = Flask(__name__)

# подключение к базе данных и добавление курсора для обращения к ней
conn = psycopg2.connect(database="service_db",
                        user="postgres",
                        password="dexus636",
                        host="localhost",
                        port="5432")

cursor = conn.cursor()

# создание декоратора, который сравнивает данные введеные пользователем с базой данных
@app.route('/login/', methods=['POST', 'GET'])
def login():  
    if request.method == 'POST':
        if request.form.get("login"):
            # забираем значения введенные пользователем username и password
            username = request.form.get('username')
            password = request.form.get('password')
            # сравививаем введенные значения с базой данных
            cursor.execute("SELECT * FROM service.users WHERE login=%s AND password=%s", (str(username), str(password)))
            records = list(cursor.fetchall())

            return render_template('account.html', full_name=records[0][1])
        elif request.form.get("registration"):
            return redirect("/registration/")

    return render_template('login.html')

# создание декоратора, который регестрирует пользователя
@app.route('/registration/', methods=['POST', 'GET'])
def registration():
    if request.method == 'POST':
        # забираем значения введенные пользователем имя(name), логин(login), пароль(password)
        name = request.form.get('name')
        login = request.form.get('login')
        password = request.form.get('password')     
        # добавляем в базу данных введенные пользователем значения
        cursor.execute('INSERT INTO service.users (full_name, login, password) VALUES (%s, %s, %s);',
                       (str(name), str(login), str(password)))
        conn.commit()

        return redirect('/login/')

    return render_template('registration.html')
