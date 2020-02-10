from flask import Flask, render_template, flash, redirect, url_for, sessions, request
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')


if __name__ == '__main__':
    app.run(debug=True)
