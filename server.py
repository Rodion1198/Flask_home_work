from flask import Flask, render_template


app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/path/requirements')
def file_content():
    with open('requirements.txt', 'r') as f:
        return render_template('index.html', text=f.read())


if __name__ == '__main__':
    app.run()