from flask import Flask, render_template, flash, redirect, url_for, sessions, request
from wtforms import Form, StringField, validators, ValidationError, SelectField
from flask_pymongo import PyMongo
from search import *
from flask_paginate import Pagination, get_page_args

MODE = mode['product']  # test or product
list_res = []
content = ''

app = Flask(__name__)
app.config['SECRET_KEY'] = '123456'
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
    #type = SelectField('Type', choices=[('古代', '古代'), ('现代', '现代')])
    type = SelectField('Type', choices=[('All', 'All'), ('Poetry', 'Poetry'), ('Lyrics', 'Lyrics')])


index_for_search = load_pickle(pickle_index_p[MODE])  # load index
tokens_id = load_pickle(tokens_id_vb_p[MODE])


def get_users(offset=0, per_page=10, result_list=[]):
    return result_list[offset: offset + per_page]


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/search', methods=['POST'])
@app.route('/search')
def search():
    form = SearchForm(request.form)
    if request.method == 'POST' and form.validate():
        global content
        global c_type
        content = form.content.data
        c_type = form.type.data

        query, phrase = preprocess_query(content)
        result_list = final_search(query, phrase, index_for_search, tokens_id)

        search_result = []
        if c_type == 'Poetry':
            for i in range(len(result_list)):
                item = result_list[i]
                data = mongo.db.song_poem.find_one({"_id": decode_vbyte(item)})
                if "dynasty" in data:
                    search_result.append(data)
                    if len(search_result) >= 200:
                        break
        else:
            if c_type == 'Lyrics':
                for i in range(len(result_list)):
                    item = result_list[i]
                    data = mongo.db.song_poem.find_one({"_id": decode_vbyte(item)})
                    if "album_name" in data:
                        search_result.append(data)
                        if len(search_result) >= 200:
                            break
            else:
                if c_type == 'All':
                    for i in range(len(result_list)):
                        item = result_list[i]
                        data = mongo.db.song_poem.find_one({"_id": decode_vbyte(item)})
                        search_result.append(data)
                        if len(search_result) >= 200:
                            break
        #for i in range(len(result_list)):
        #    item = result_list[i]
        #    search_result.append(mongo.db.song_poem.find_one({"_id": decode_vbyte(item)}))
            # if len(search_result) >= 3:
            #     break
        global list_res
        list_res = search_result

        #if c_type == 'All':
        #    list_res = search_result
        #elif c_type == 'Poerty':
        #    list_res = [res for res in search_result if 'title' in res]
        #elif c_type == 'Lyrics':
        #    list_res = [res for res in search_result if 'song_name' in res]
    page, per_page, offset = get_page_args(page_parameter='page',
                                           per_page_parameter='per_page')

    total = len(list_res)
    pagination_users = get_users(offset=offset, per_page=per_page, result_list=list_res)
    # pagination_users = search_result
    pagination = Pagination(page=page, per_page=per_page, total=total,
                            css_framework='bootstrap4')

    return render_template('search.html', content=content, c_type=c_type,
                           users=pagination_users,
                           page=page,
                           per_page=per_page,
                           pagination=pagination)


@app.route('/result/<int:result_id>')
def result(result_id):
    res = mongo.db.song_poem.find_one({"_id": int(result_id)})
    return render_template('result.html', result=res)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0',port=5000)

