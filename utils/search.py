import re
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, FileField
from wtforms.validators import DataRequired
from .DBclient import MongoConnection

class SearchBox(FlaskForm):
	comment = '请在搜索框内输入文件名'
	input_data = StringField('文件名', 
	    validators=[],
	    render_kw = {
	        "placeholder": "",
	    }
	)
	submit = SubmitField('提交')

	def _parse(self, query):
		s = query.strip()
		s = re.sub(r'[\s]+', '(.*)', s)
		s = '(?i)'+s
		return s

	def run(self,):
		with MongoConnection('pdf') as conn:
			q = {
				"file_name":{
					'$regex': self._parse(self.input_data.data)
				}
			}
			p = {"data":0}
			res = list(conn.find(q, p))

		return res