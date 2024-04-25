import app.helpers as helpers
import unittest
from unittest.mock import Mock
import filecmp
from os import path

primer_f = Mock(data = 'CTGGTCCAGTGCGTTATTGG')
primer_r = Mock(data = 'AGCCAAATGCTTCTTGCTCTTTT')
guide_seq = Mock(data = 'CTACAGGACGTACCTGCACCCGGATTCACCAGCGCCCG')
form = Mock(
    primer_f = primer_f, primer_r = primer_r,
    guide_seq = guide_seq)

sense = Mock(
    seq = 'CCTGCACCCGGATTCACCAGCTGGTCCAGTGCGTTATTGG',
    id = 'Sense HL',
    name = '<unknown name>',
    description = 'WARNING: Could not optimise sense headloop tag (Tm difference > 3°C)',
    dbxrefs = []
)
antisense = Mock(
    seq = 'GGTGCAGGTACGTCCTGTAGAGCCAAATGCTTCTTGCTCTTTT',
    id = 'Antisense HL',
    name = '<unknown name>',
    description = 'Tm difference < 3°C',
    dbxrefs=[]
)

hl_design = (sense, antisense)

hl_dir = path.abspath(path.join(path.dirname(path.realpath(__file__)), '..'))

app_root = path.join(hl_dir, 'app')
app = Mock(
    root_path = app_root,
    config = {
        'TMP_FOLDER': 'tmp_files'
    })

class TestMultiply(unittest.TestCase):
    tmp_file_path = path.join(app_root, "tmp_files", "tmp_results.tsv")
    # returns a path for temp file
    def test_returns_file_name(self):
        self.assertEqual(
            helpers.create_file_for_download(app, form, hl_design),
            self.tmp_file_path)
    # must create a temporary file
    def test_file_exists(self):
        self.assertTrue(path.exists(self.tmp_file_path))

    # check files match
    def test_files_match(self):
        self.assertTrue(filecmp.cmp(self.tmp_file_path, 
            path.join(hl_dir, "tests", "result_file.tsv")))
