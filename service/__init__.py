from flask import Flask

app = Flask(__name__)

from service import views, models

