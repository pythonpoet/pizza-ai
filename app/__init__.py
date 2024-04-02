from flask import Flask


#from backend.app import *
#
app = Flask(__name__)
from .backend.routes import *


if __name__ == 'app':
    print(__name__)