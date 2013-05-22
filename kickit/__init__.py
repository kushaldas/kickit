import os
from .utils import get_files
from flask import Flask
from flask import render_template

app = Flask(__name__)

PATH = '/home/kdas/code/git/'

@app.route('/<reponame>')
def index(reponame):
    repopath = os.path.join(PATH, reponame)
    if not os.path.exists(repopath):
        return "Sorry"
    dirs, files = get_files(repopath)
    return render_template('index.html', dirs=dirs, files=files)
