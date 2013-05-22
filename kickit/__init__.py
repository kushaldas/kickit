import os
from flask import Flask
from flask import render_template

app = Flask(__name__)

PATH = '/home/kdas/code/git/'

@app.route('/<reponame>')
def index(reponame):
    repopath = os.path.join(PATH, reponame)
    if not os.path.exists(repopath):
        return "Sorry"
    fd = [(name) for name in os.listdir(repopath) if not name.startswith('.')]
    return render_template('index.html', files=fd)
