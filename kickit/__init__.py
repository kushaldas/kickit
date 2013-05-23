import os
from .utils import get_files, get_branches, get_blob_text
from flask import Flask
from flask import render_template
from jinja2.ext import Markup

app = Flask(__name__)

PATH = '/home/kdas/code/git/'

# @app.route('/<reponame>')
# def index(reponame):
#     repopath = os.path.join(PATH, reponame)
#     if not os.path.exists(repopath):
#         return "Sorry"
#     dirs, files = get_files(repopath, 'master')
#     branches = get_branches(repopath)
#     return render_template('index.html', dirs=dirs, files=files, projectname=reponame, branches=branches)

@app.route('/<reponame>')
@app.route('/<reponame>/tree/<branchname>', defaults={'path': ''})
@app.route('/<reponame>/tree/<branchname>/<path:path>')
def index_branch(reponame, branchname='master', path=''):
    print path
    repopath = os.path.join(PATH, reponame)
    if not os.path.exists(repopath):
        return "Sorry"
    dirs, files = get_files(repopath, branchname, param=path)
    branches = get_branches(repopath)
    return render_template('index.html', dirs=dirs, files=files, projectname=reponame, branches=branches, param=path,
                           branch=branchname)

@app.route('/<reponame>/blob/<branchname>/<path:path>')
def show_blob(reponame, branchname, path):
    '''
    Shows a given blob for the git repo
    '''
    repopath = os.path.join(PATH, reponame)
    if not os.path.exists(repopath):
        return "Sorry"
    data = get_blob_text(repopath, path, branchname)
    return render_template('blob.html', text=Markup(data).unescape())