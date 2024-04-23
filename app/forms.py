from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length

class InputForm(FlaskForm):
    primer_f = StringField('Forward Primer', validators=[DataRequired()])
    primer_r = StringField('Reverse Primer', validators=[DataRequired()])
    guide_seq = StringField('Guide Sequence and context (>=15 bp)',
        validators=[
            DataRequired(),
            Length(min = 38, message="The gRNA target sequence (including PAM) and at least 15 bp afterwards must be provided")
        ])
    orientation = SelectField('Orientation', 
        choices = ["Forward", "Reverse"], validators=[DataRequired()])
    submit = SubmitField('Design Headloop Primers')
