from flask import Flask
from .backend.chaosChain import *
app = Flask(__name__)
llm = ChaosLLM()
from .backend.routes import *





if __name__ == 'app':
    print(__name__)