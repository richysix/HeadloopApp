import os

def create_file_for_download(app, form, hl_design):
    ''' Create a temporary tsv file from the design results '''
    # create temp file
    tmp_file_name = os.path.join(
        app.root_path, app.config['TMP_FOLDER'], "tmp_results.tsv")
    # print(app.root_path, app.config['TMP_FOLDER'], tmp_file_name)
    with open(tmp_file_name, "w") as out_file:
        # header
        print("\t".join(
            ["Name", "ForwardPrimer", "ReversePrimer", 
             "HeadloopPrimer", "Notes"]),
             file=out_file)
        for design in hl_design:
            print("\t".join(
                [design.id, form.primer_f.data, form.primer_r.data,
                str(design.seq), design.description]),
                file=out_file)
    return(tmp_file_name)
