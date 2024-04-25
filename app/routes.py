from flask import render_template, flash, url_for, make_response
from app import app
from app.forms import InputForm, DownloadForm

import os
from headloop.designer import design

@app.get('/')
def input():
    form = InputForm()
    return render_template('input.html', form=form)

@app.post('/')
def output_primers():
    form = InputForm()
    if form.validate_on_submit():
        if os.getenv("FLASK_DEBUG"):
            flash('Form submitted F={}, R={}, G={}, O={}'.format(
                form.primer_f.data, form.primer_r.data,
                form.guide_seq.data, form.orientation.data))
        hl_design = design(form.primer_f.data, form.primer_r.data,
            form.guide_seq.data, form.orientation.data)
        # tmp_file_name = create_file_for_download(app, form, hl_design)
        hl_results = []
        for result in hl_design:
            if result.description[0:8] == "WARNING:":
                desc_class = "warning"
            else:
                desc_class = "success"
            hl_results.append((result.id, str(result.seq),
                result.description, desc_class))
    download_form = DownloadForm()
    return render_template(
        'output.html',
        primer_f = form.primer_f.data,
        primer_r = form.primer_r.data,
        hl_results = hl_results,
        download_form = download_form
    )

@app.post('/download')
def download():
    download_form = DownloadForm()
    if download_form.validate_on_submit():
        lines = [
            ",".join(['Name', 'ForwardPrimer', 'ReversePrimer', 'HeadloopPrimer', 'Notes']),
            ",".join([
                "SenseHL",
                download_form.primer_f.data,
                download_form.primer_r.data,
                download_form.hl_sense.data,
                download_form.notes_sense.data,
            ]),
            ",".join([
                "AntisenseHL",
                download_form.primer_f.data,
                download_form.primer_r.data,
                download_form.hl_antisense.data,
                download_form.notes_antisense.data,
            ])
        ]
        text = "\n".join(lines)
    resp = make_response(text)
    resp.headers['Content-Disposition'] = 'filename="hl.csv"'
    resp.headers['Content-type'] = 'text/csv'
    return resp

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404
