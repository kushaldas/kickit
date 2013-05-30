import os
import ConfigParser
from .utils import get_files, get_branches, get_blob_text, show_commit_index, \
                    get_git_directories
from flask import Flask, request
from flask import render_template
from jinja2.ext import Markup

app = Flask(__name__)

config = ConfigParser.ConfigParser();
config.readfp(open('./kickit.conf'))
PATH = config.get('kickit', 'PATH')


@app.route('/')
def home():
    if PATH is None:
        return 'PATH not set properly. Check the settings/settings.py file'
    dirs = get_git_directories(PATH)
    return render_template('home.html', dirs=dirs)


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
    is_prev = False
    is_next = False
    next_page = prev_page = 0
    try:
        if 'page' in request.args:
            page = int(request.args['page'])
            if page != 1:
                is_prev = True
                prev_page = page - 1
    except Exception:
        pass
    if not path: # We need to show the index
        data = show_commit_index(repopath, branchname, page)
        if show_commit_index(repopath, branchname, page+1) != []:
            is_next = True
            next_page = page + 1

    ret_dict = {
        'is_prev' : is_prev,
        'is_next' : is_next,
        'prev_page' : prev_page,
        'next_page' : next_page,
        'branchname': branchname,
        'reponame' : reponame,
    }
    return render_template('commit_index.html', data=data, r_dict = ret_dict)
