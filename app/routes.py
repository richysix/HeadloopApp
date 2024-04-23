from flask import render_template, flash, redirect
from app import app
from app.forms import InputForm

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    form = InputForm()
    if form.validate_on_submit():
        flash('Form submitted F={}, R={}, G={}, O={}'.format(
            form.primer_f.data, form.primer_r.data,
            form.guide_seq.data, form.orientation.data))
        return redirect('/index')
    return render_template('index.html', form=form)
