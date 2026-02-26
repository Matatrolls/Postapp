import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = "dev"
    DATABASE = os.path.join(BASE_DIR, "notes.db")