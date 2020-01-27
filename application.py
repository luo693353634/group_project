from flask import Flask
app = Flask(__name__)
@app.route('/')
def index():
    return 'hello world  supervisor gunicorn '
@app.route('/1')
def index1():
    return 'hello world  supervisor gunicorn  ffffff'
@app.route('/qw/1')
def indexqw():
    return 'hello world  supervisor gunicorn fdfdfbdfbfb '
if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000, debug = True)
