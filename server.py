from flask import Flask, render_template
from faker import Faker
import csv
import requests
from database import DEFAULT_PATH, init_database, exec_query
import sqlite3

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/path/requirements')
def file_content():
    with open('requirements.txt', 'r') as f:
        return render_template('index.html', text=f.read())


@app.route('/generate-users')
def faker_content():
    fake = Faker()
    output = [fake.name().replace(' ', '_') + ' ' + fake.email() for i in range(100)]
    return render_template('generate.html', title='Generate user', output=output)


@app.route('/mean')
def content_csv():
    with open('/home/rodion/hw.csv') as csvfile:
        file_reader = csv.reader(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        result: list = [0, 0, 0]
        for row in file_reader:
            if row == ["Index", "Height(Inches)", "Weight(Pounds)"]:
                continue
            if not row:
                break
            result[0] = int(row[0])
            # print(f'{result[0]=}')
            result[1] += float(row[1].strip(' '))
            # print(f'{result[1]=}')
            result[2] += float(row[2].strip(' '))
            # print(f'{result[2]=}')
        result = [(result[1] * 2.54) / result[0], (result[2] * 0.453592) / result[0]]
        return render_template('index.html', title="Calculation csv file", result=result)


@app.route('/space')
def get_astronaut():
    r = requests.get('http://api.open-notify.org/astros.json')
    astronauts = r.json()['number']
    return render_template('generate.html', astronauts=astronauts)


@app.route('/names')
def amount_of_distinct_names():
    init_database()
    with sqlite3.connect(DEFAULT_PATH) as conn:
        with conn as cursor:
            c = cursor.execute("SELECT COUNT(DISTINCT name) FROM customers")
            rows = c.fetchone()
            for row in rows:
                return render_template('index.html', row=row)


@app.route('/tracks/')
def amount_of_tracks():
    with sqlite3.connect(DEFAULT_PATH) as conn:
        with conn as cursor:
            c = cursor.execute("SELECT COUNT(track) FROM tracks")
            rows = c.fetchone()
            for row2 in rows:
                return render_template('index.html', row2=row2)


@app.route('/track-sec')
def track_sec():
    with sqlite3.connect(DEFAULT_PATH) as conn:
        with conn as cursor:
            c = cursor.execute('SELECT track FROM tracks')
            row1 = c.fetchall()

            c1 = cursor.execute('SELECT duration FROM tracks')
            rows = c1.fetchall()
            for s in rows:
                a = s[0]
                convert = str(sum(int(i) * 60 ** index for index, i in enumerate(a.split(":")[::-1])))
            return render_template('index.html', convert=convert, row=row1)


@app.route('/track-sec/stat')
def sum_track():
    with sqlite3.connect(DEFAULT_PATH) as conn:
        with conn as cursor:
            c = cursor.execute('SELECT AVG(duration) FROM tracks')
            rows = c.fetchone()
            for s in rows:
                a = str(s)
                convert = sum(int(i) * 60 ** index for index, i in enumerate(a.split(".")[::-1]))

            c2 = cursor.execute('SELECT SUM(duration) FROM tracks')
            rows2 = c2.fetchone()
            for s_1 in rows2:
                a_1 = str(s_1)
                convert2 = sum(int(i) * 60 ** index for index, i in enumerate(a_1.split(".")[::-1]))
                return render_template('generate.html', convert=convert, convert2=convert2)


@app.route('/tracks/<genre>')
def tracks_genre(genre):
    choose_genre = exec_query(f"SELECT COUNT(id_track),genre FROM tracks GROUP BY genre HAVING COUNT({genre})")
    return render_template('generate.html', tracks=choose_genre)


if __name__ == '__main__':
    app.run(debug=True)
