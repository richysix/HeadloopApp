from flask import render_template, flash, url_for
from app import app
from app.forms import InputForm

import os
from headloop.designer import design

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    form = InputForm()
    if form.validate_on_submit():
        if os.getenv("FLASK_DEBUG"):
            flash('Form submitted F={}, R={}, G={}, O={}'.format(
                form.primer_f.data, form.primer_r.data,
                form.guide_seq.data, form.orientation.data))
        hl_design = design(form.primer_f.data, form.primer_r.data,
            form.guide_seq.data, form.orientation.data)
        hl_results = []
        for result in hl_design:
            if result.description[0:8] == "WARNING:":
                desc = result.description[9:]
                desc_class = "warning"
            else:
                desc = result.description
                desc_class = "success"
            hl_results.append((result.id, str(result.seq),
                desc, desc_class))
        return render_template(
            'output.html',
            primer_f = form.primer_f.data,
            primer_r = form.primer_r.data,
            hl_results = hl_results
        )
    return render_template('index.html', form=form)
