from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import BooleanField, SubmitField
from wtforms.validators import DataRequired


class JobsForm(FlaskForm):
    job = StringField('Job title', validators=[DataRequired()])
    team_lead = StringField('Team leader id', validators=[DataRequired()])
    duration = StringField('Work Size', validators=[DataRequired()])
    collaborators = StringField('Collaborators', validators=[DataRequired()])
    is_finished = BooleanField('Is job fished?')
    submit = SubmitField('Submit')
