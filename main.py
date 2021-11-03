from flask import Flask,render_template,request,\
                  redirect,Response,session, url_for
from utils import *
from bson.objectid import ObjectId
from flask_bootstrap import Bootstrap


app = Flask(__name__)
bootstrap = Bootstrap(app)

app.config['SECRET_KEY'] = 'OH ITS A SECRET!'
app.config['SAVE_PATH'] = 'mongodb://localhost:27017'

@app.route('/',methods=['GET'])
def index():
    return redirect(url_for('.search'))


@app.route('/upload',methods=['GET','POST'])
def upload():
  
    form_in = UploadForm()
 
    if form_in.validate_on_submit():
        form_in.run()

    return render_template(
        'form.html',
        name = '文件上传',
        form_in = form_in
        )



@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


@app.route('/search',methods=['GET','POST'])
def search():

    form_in = SearchBox()
    result = []
    if form_in.validate_on_submit():
        result = form_in.run()

    return render_template(
        'search.html',
        name = '文件搜索',
        form_in = form_in,
        results = result
        )

@app.route('/pdf/<id>',methods=['GET'])
def download(id):
    try:
        with MongoConnection('pdf') as conn:
            q = {
                "_id":ObjectId(id)
            }
            p = {"data":1}
            res = conn.find(q, p)
            res = list(res)
            file_bytes = res[0]['data']

    except Exception as e:
        print(traceback.format_exc())
        return render_template('404.html'), 404

    return Response(file_bytes, content_type='application/pdf')

@app.route('/img/<id>',methods=['GET'])
def first_page(id):
    try:
        with MongoConnection('pdf') as conn:
            q = {
                "_id":ObjectId(id)
            }
            p = {"first_page":1}
            res = conn.find(q, p)
            res = list(res)
            file_bytes = res[0]['first_page']

    except Exception as e:
        print(traceback.format_exc())
        return render_template('404.html'), 404

    return Response(file_bytes, content_type='image/png')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

