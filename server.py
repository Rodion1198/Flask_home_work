from flask import Flask, render_template
from faker import Faker

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


if __name__ == '__main__':
    app.run()