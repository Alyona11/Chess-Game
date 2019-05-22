# Налаштування для запуску Flask-проекту
from flask import Flask

app = Flask(__name__)

from app import routes
