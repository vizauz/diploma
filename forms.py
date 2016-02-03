from flask_wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email

class AddUser(Form):
	username = StringField('User name', validators=[DataRequired('Enter user name')])
	email = StringField('User email', validators=[DataRequired('Enter email'), Email('Enter valid eamil addres')])
	submit = SubmitField('Add user')

class CreateGroup(Form):
	groupname = StringField('Group name', validators=[DataRequired('Enter group name')])
	submit = SubmitField('Add group')