import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'saddling-partridge-vending'
    TMP_FOLDER = 'tmp_files'