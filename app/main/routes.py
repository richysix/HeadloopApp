from flask import (
    render_template, redirect, request, flash, url_for,
    make_response, session
)

from app.main import bp
from app.forms import InputForm, DownloadForm

import os
from headloop.designer import design

@bp.route('/', methods=['GET', 'POST'])
def input():
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
                desc_class = "warning"
            else:
                desc_class = "success"
            hl_results.append((result.id, str(result.seq),
                result.description, desc_class))
        session['primer_f'] = form.primer_f.data
        session['primer_r'] = form.primer_r.data
        session['hl_results'] = hl_results
        return redirect(url_for('main.output'))
    return render_template('input.html', form=form)

@bp.get('/output')
def output():
    download_form = DownloadForm()
    return render_template(
        'output.html',
        primer_f = session['primer_f'],
        primer_r = session['primer_r'],
        hl_results = session['hl_results'],
        download_form = download_form
    )

@bp.post('/download')
def download():
    download_form = DownloadForm()
    hl_results = session['hl_results']
    primer_f = session['primer_f']
    primer_r = session['primer_r']
    if download_form.validate_on_submit():
        lines = [
            ",".join([
                'Name', 'ForwardPrimer', 'ReversePrimer', 'HeadloopPrimer',
                'Notes']) ]
        for result in hl_results:
            line = ",".join([
                result[0],
                primer_f,
                primer_r,
                result[1],
                result[2],
            ])
            lines.append(line)
        text = "\n".join(lines)
    resp = make_response(text)
    resp.headers['Content-Disposition'] = 'filename="hl.csv"'
    resp.headers['Content-type'] = 'text/csv'
    return resp
