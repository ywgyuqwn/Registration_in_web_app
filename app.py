from flask import Flask, render_template, request, redirect
import psycopg2

app = Flask(__name__)
conn = psycopg2.connect(database="service__db",
                        user="postgres",
                        password="coconimo00F",
                        host="localhost",
                        port="5432")

cursor = conn.cursor()

@app.route('/login/', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        if request.form.get("login"):
            username = request.form.get('username')
            password = request.form.get('password')
            cursor.execute("SELECT * FROM service__db.users WHERE login=%s AND password=%s", (str(username), str(password)))
            records = list(cursor.fetchall())
            return render_template('account.html', full_name=records[0][1])
        elif request.form.get("registration"):
            return redirect("/registration/")
    return render_template('login.html')

@app.route('/registration/', methods=['POST', 'GET'])
def registration():
    if request.method == 'POST':
        name = request.form.get('name')
        login = request.form.get('login')
        password = request.form.get('password')
        # проверка есть ли логин в базе данных
        cursor.execute("SELECT login FROM service__db.users;")
        logins = list(i[0] for i in cursor.fetchall())
        print(login, logins)
        print(login in logins)
        if login in logins:
            return render_template('registration.html', error='Такой логин уже существует в базе данных')
        # проверка есть ли в имени цифры
        is_digit_in_name = False
        for i in range(10):
            if str(i) in name:
                is_digit_in_name = True
        if is_digit_in_name:
            return render_template('registration.html', error='У вас есть цифры в имени')
        if name == '' or password == '' or login == '':
            return render_template('registration.html', error='Заполните пустые поля')

        cursor.execute('INSERT INTO service__db.users (full_name, login, password) VALUES (%s, %s, %s);',
                       (str(name), str(login), str(password)))
        conn.commit()
        return redirect('/login/')
    return render_template('registration.html')

if __name__ == '__main__':
    app.run()