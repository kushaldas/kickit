import os
from .utils import get_files, get_branches, get_blob_text, show_commit_index, \
                    shutdown_server, get_git_directories
from flask import Flask, request
from flask import render_template
from jinja2.ext import Markup

app = Flask(__name__)

try:
    from settings.settings import PATH
except:
    raise RuntimeError('settings/settings.py file not configured properly.')
    shutdown_server()

@app.route('/')
def home():
    if PATH is None:
        return 'PATH not set properly. Check the settings/settings.py file'
    dirs = get_git_directories(PATH)
    return render_template('home.html', dirs=dirs)

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

@app.route('/<reponame>/commits/')
@app.route('/<reponame>/commits/<branchname>', defaults={'path': ''})
@app.route('/<reponame>/commits/<branchname>/<path:path>')
def index_commits(reponame, branchname='master', path=''):
    repopath = os.path.join(PATH, reponame)
    if not os.path.exists(repopath):
        return "Sorry"
    page = 1
    try:
        if 'page' in request.args:
            page = int(request.args['page'])
    except Exception:
        pass
    if not path: # We need to show the index
        data = show_commit_index(repopath, branchname, page)
    return render_template('commit_index.html', data=data)
