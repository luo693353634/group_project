from flask import Flask, render_template, flash, redirect, url_for, sessions, request
from wtforms import Form, StringField, validators, ValidationError, SelectField


app = Flask(__name__)
app.config['SECRET_KEY'] = '123456'


class SearchForm(Form):
    content = StringField('Content', [
        validators.Length(min=1, max=20, message=u'Search content should less than 20')
    ])

    type = SelectField('Type', choices=[('Type 1', 'Type 1'), ('Type 2', 'Type 2')])


@app.route('/', methods=['GET', 'POST'])
def home():
    form = SearchForm(request.form)
    if request.method == 'POST' and form.validate():
        content = form.content.data
        c_type = form.type.data
        return redirect(url_for('search', content=content, c_type=c_type))
    return render_template('home.html')


@app.route('/search', methods=['POST'])
def search():
    form = SearchForm(request.form)
    if request.method == 'POST' and form.validate():
        content = form.content.data
        c_type = form.type.data
        return content + c_type


@app.route('/result')
def result():
    return render_template('result.html')


if __name__ == '__main__':
    app.run(debug=True)
