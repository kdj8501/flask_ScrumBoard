from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired

class JobForm(FlaskForm):
    subject = StringField('제목', validators = [DataRequired('업무 제목을 입력해주세요.')])
    content = TextAreaField('내용', validators = [DataRequired('업무의 내용을 입력해주세요.')])
    start_day = StringField('시작', validators = [DataRequired('시작일을 입력해주세요.')])
    end_day = StringField('종료', validators = [DataRequired('종료일을 입력해주세요.')])
    
class CommentForm(FlaskForm):
    content = TextAreaField('내용', validators = [DataRequired('코멘트 내용을 입력해주세요.')])
