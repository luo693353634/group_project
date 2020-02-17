from flask import Flask, render_template, flash, redirect, url_for, sessions, request
from wtforms import Form, StringField, validators, ValidationError, SelectField
import algorithm
from flask_pymongo import PyMongo
from search import *

MODE = mode['product']  # test or product

index_for_search = load_pickle(pickle_index_p[MODE])  # load index
tokens_id = load_pickle(tokens_id_vb_p[MODE])

app = Flask(__name__)
# app.config['SECRET_KEY'] = '123456'
app.config["MONGO_URI"] = "mongodb://localhost:27017/firstdb"
# app.config.update(
#     MONGO_HOST='localhost',
#     MONGO_PORT=27017,
#     # MONGO_USERNAME='ttdspj',
#     # MONGO_PASSWORD='123456',
#     MONGO_DBNAME='flask'
# )
mongo = PyMongo(app)


class SearchForm(Form):
    content = StringField('Content', [
        validators.Length(min=1, max=20, message=u'Search content should less than 20')
    ])

    type = SelectField('Type', choices=[('Type 1', 'Type 1'), ('Type 2', 'Type 2')])


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/search', methods=['POST'])
def search():
    form = SearchForm(request.form)
    if request.method == 'POST' and form.validate():
        content = form.content.data
        c_type = form.type.data
        """
        将查询的词传入算法，然后返回查询结果。查询结果应当使用SQL或者字典以加快运行速度
        如果涉及到属性，应定义一个类，规范化检索过程
        """
        query, phrase = preprocess_query(content)
        # res = search(query, phrase, index_for_search, tokens_id)
        result_list = search(query, phrase, index_for_search, tokens_id)
        # search_result = algorithm.tf_idf(content)
        # search_result = mongo.db.song_inf.find_one_or_404({"song_id": content})
        # search_result = mongo.db.song_inf.find({"song_id": content})
        search_result = []
        for item in result_list:
            search_result.append(mongo.db.song_poem.find_one({"doc_id": int(item)}))

        return render_template('search.html', content=content, c_type=c_type, search_result=search_result)


@app.route('/result/<int:result_id>')
def result(result_id):
    res = mongo.db.song_poem.find_one({"doc_id": int(result_id)})
    return render_template('result.html', result=res)


if __name__ == '__main__':
    app.run(debug=True)
