from flask import Flask, render_template
from faker import Faker
import csv
import requests
from database import DEFAULT_PATH, init_database
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


@app.route('/peace')
def amount_of_distinct_names():
    init_database()
    with sqlite3.connect(DEFAULT_PATH) as conn:
        with conn as cursor:
            c = cursor.execute("SELECT COUNT(DISTINCT name) FROM customers")
            rows = c.fetchall()
            for row in rows:
                return render_template('index.html', row=row)



if __name__ == '__main__':
    app.run()
