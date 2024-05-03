import pytest

from flask import session

def test_config(test_app):
    assert test_app.testing

# routes
def test_404(client):
    response = client.get('/cheese')
    assert response.status_code == 404
    assert b'Page Not Found' in response.data

def test_input(client):
    response = client.get('/')
    assert b'Design headloop primers for testing cutting efficiency of CRISPR/Cas9 guide RNAs' in response.data
    assert b'<form action="/"' in response.data
    assert b'<p>CAGGTCGAGG<b>GTTCTGTCAGGACGT' in response.data

test_primer_f = 'CTGGTCCAGTGCGTTATTGG'
test_primer_r = 'AGCCAAATGCTTCTTGCTCTTTT'
test_guide_seq = 'CTACAGGACGTACCTGCACCCGGATTCACCAGCGCCCG'
test_orientation = 'antisense'

@pytest.mark.parametrize(('primer_f', 'primer_r', 'guide_seq', 'orientation', 'message'), (
    ('CTGGTCCAGTGCGPTATTGG', 'AGCCAAATGCTTCTTGCTCTTTT', 
    'CTACAGGACGTACCTGCACCCGGATTCACCAGCGCCCG', 'antisense', b'Sequence contains non-base letters'),
    ('CTGGTCCAGTGCGTTATTGG', 'AGCCAAATZCTTCTTGCTCTTTT', 
    'CTACAGGACGTACCTGCACCCGGATTCACCAGCGCCCG', 'antisense', b'Sequence contains non-base letters'),
    ('CTGGTCCAGTGCGTTATTGG', 'AGCCAAATGCTTCTTGCTCTTTT', 
    'CTACAGGACGTACCTGCOCCCGGATTCACCAGCGCCCG', 'antisense', b'Sequence contains non-base letters'),
))
def test_input_validation(client, primer_f, primer_r, guide_seq, orientation, message):
    response = client.post('/', 
        data={
            'primer_f': primer_f,
            'primer_r': primer_r,
            'guide_seq': guide_seq,
            'orientation': orientation
        })
    assert message in response.data

test_results = [
    ("Sense HL", "CCTGCACCCGGATTCACCAGCTGGTCCAGTGCGTTATTGG", 
    "WARNING: Could not optimise sense headloop tag (Tm difference > 3°C)", 
    "warning"),
    ("Antisense HL", "GGTGCAGGTACGTCCTGTAGAGCCAAATGCTTCTTGCTCTTTT", 
    "Tm difference < 3°C", 
    "success")
]
def test_output(client):
    with client:
        response = client.post('/', 
            data={
                'primer_f': test_primer_f,
                'primer_r': test_primer_r,
                'guide_seq': test_guide_seq,
                'orientation': test_orientation
            },
            follow_redirects=True)
        assert response.status_code == 200
        assert b'<th scope="col">Type</th>' in response.data
        assert session["primer_f"] == test_primer_f
        assert session["primer_r"] == test_primer_r
        assert session["hl_results"] == test_results

def test_download(client):
    with client.session_transaction() as session:
        # set a user id without going through the login route
        session["primer_f"] = test_primer_f
        session["primer_r"] = test_primer_r
        session["hl_results"] = test_results

    response = client.post('/download')
    assert response.status_code == 200
    assert response.headers['Content-Disposition'] == 'filename="hl.csv"'
    assert response.headers['Content-type'] == 'text/csv'
