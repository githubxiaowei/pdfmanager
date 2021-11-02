import re
import hashlib
from flask_wtf import FlaskForm
from flask import flash
from wtforms import StringField, SubmitField, TextAreaField, FileField
from wtforms.validators import DataRequired
from flask_wtf.file import FileRequired, FileAllowed
from .DBclient import MongoConnection
import traceback
import os
import sys
sys.path.append('..')
from main import app


class UploadForm(FlaskForm):
    comment = '请上传PDF文件，并补充必要信息'
    name = StringField('文件名', 
        validators=[],
        render_kw = {
            "placeholder": "",
        }
    )
    author = StringField('作者', 
        validators=[],
        render_kw = {
            "placeholder": "",
        }
    )
    publisher = StringField('出版社', 
        validators=[],
        render_kw = {
            "placeholder": "",
        }
    )
    year = StringField('年份', 
        validators=[],
        render_kw = {
            "placeholder": "",
        }
    )

    data = FileField(
        label="PDF文件",
        validators=[
            FileRequired(),
            FileAllowed(['pdf'], 'Only *.pdf is allowed')
        ]
    )
    submit = SubmitField('提交')

    def _save(self,):
        save_path = app.config['SAVE_PATH']
        file_bytes = self.data.data.read()
        file_dict = {}
        file_dict['author'] = self.author.data.strip()
        file_dict['year'] = self.year.data.strip()
        file_dict['publisher'] = self.publisher.data.strip()
        file_dict['file_name'] = self.data.data.filename if self.name.data.strip() == '' else self.name.data.strip()
        file_dict['file_size'] = len(file_bytes)//1024
        file_dict['data'] = file_bytes
        file_dict['hash_code'] = hashlib.md5(file_bytes).hexdigest()
        with MongoConnection('pdf') as conn:
            if len(list(conn.find({'hash_code':file_dict['hash_code']},{'_id':1}))) > 0:
                flash('File exists!')

            else:
                conn.insert(file_dict)
                flash('Upload success!  File size: {:.3f} MB'.format(
                len(file_bytes)/(1024*1024)
            ))

    def run(self, ):
        try:
            self._save()
        except Exception as e:
            flash(e)
            print(traceback.format_exc())



