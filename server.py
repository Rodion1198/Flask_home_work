from flask import Flask, render_template
from faker import Faker
import csv


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
    output = [fake.name() + fake.email() for i in range(100)]
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
            print(f'{result[0]=}')
            result[1] += float(row[1].strip(' '))
            print(f'{result[1]=}')
            result[2] += float(row[2].strip(' '))
            print(f'{result[2]=}')
        result = [(result[1] * 2.54) / result[0], (result[2] * 0.453592) / result[0]]
        return render_template('index.html', title="Calculation csv file", result=result)


if __name__ == '__main__':
    app.run()