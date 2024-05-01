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

# this test doesn't currently work
def test_output(client):
    with client:
        client.post('/', 
            data={
                'primer_f': 'CTGGTCCAGTGCGTTATTGG', 
                'primer_r': 'AGCCAAATGCTTCTTGCTCTTTT',
                'guide_seq': 'CTACAGGACGTACCTGCACCCGGATTCACCAGCGCCCG',
                'orientation': 'antisense'
            },
            follow_redirects=True)
        assert session["primer_f"] == 'CTGGTCCAGTGCGTTATTGG'
