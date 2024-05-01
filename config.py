import os

from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'saddling-partridge-vending'
    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')
