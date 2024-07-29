from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, Regexp

import os
debug = os.getenv("FLASK_DEBUG")
import re
bases_re = re.compile("^[ACGTRYSWKMBDHV]*$", flags = re.IGNORECASE)
non_base_msg = "Sequence contains non-base letters. Only ACGTRYSWKMBDHV are allowed."

class InputForm(FlaskForm):
    primer_f = StringField('Forward Primer', 
        validators=[
            DataRequired(),
            Regexp(bases_re, message = non_base_msg)
        ],
        default = "CTGGTCCAGTGCGTTATTGG" if debug else None)
    primer_r = StringField('Reverse Primer', 
        validators=[
            DataRequired(),
            Regexp(bases_re, message = non_base_msg)
        ],
        default = "AGCCAAATGCTTCTTGCTCTTTT" if debug else None)
    guide_seq = StringField('Guide Sequence and context (Must be at least 38 bp)',
        validators=[
            DataRequired(),
            Regexp(bases_re, message = non_base_msg),
            Length(min = 38, message="The gRNA target sequence (including PAM) and at least 15 bp afterwards must be provided")
        ],
        default = "CTACAGGACGTACCTGCACCCGGATTCACCAGCGCCCG" if debug else None)
    orientation = SelectField('Orientation', 
        choices = [("sense", "Forward"), ("antisense", "Reverse")], 
        validators=[DataRequired()])
    submit = SubmitField('Design Headloop Primers')

class DownloadForm(FlaskForm):
    primer_f = StringField()
    primer_r = StringField()
    hl_sense = StringField()
    notes_sense = StringField()
    hl_antisense = StringField()
    notes_antisense = StringField()
    submit = SubmitField('Download results as CSV')
