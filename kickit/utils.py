import os
import time
import subprocess
from git import Repo
from jinja2.ext import Markup
from pygments import highlight
from pygments.lexers import get_lexer_by_name, guess_lexer, get_lexer_for_mimetype
from pygments.formatters import HtmlFormatter
from pygments.util import ClassNotFound

def system(cmd):
    """ 
    Invoke a shell command.
    """
    ret = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE,
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, close_fds=True)
    out, err = ret.communicate()
    return out

def get_git_directories(path):
    '''
    Return a list containing list of git directories

    :arg path: Path to directory to search
    '''
    return [x for x in os.listdir(path) if os.path.exists(os.path.join(
                                                            path,x,'.git'))]

def get_files(path, branchname='master', param=''):
    '''
    Returns a tuple containing list of directories and files from given git repo.

    :arg path: Path to the git
    '''
    repo = Repo(path)
    dirs = []
    files = []
    head = get_head(repo, branchname)
    tree = head.commit.tree
    if param:
        tree = tree[param]
    for data in tree:
        if data.type == 'blob':
            files.append(data.name)
        else:
            dirs.append(data.name)
    dirs.sort()
    files.sort()
    return set(dirs), files

def get_head(repo, name):
    '''
    :arg repo: Repo object
    :arg name: Name of the branch we are looking for.

    :return: Branch object pointing to master or None.
    '''
    for head in repo.heads:
        if head.name == name:
            return head

def get_branches(path):
    repo = Repo(path)
    return [r.name for r in repo.heads]


def get_mime_type(repo, branchname, path):
    '''
    Find the mime-type of the given path.
    '''
    branch = None
    for head in repo.heads:
        if head.name == branchname:
            branch = head
            break

    if branch:
        blob = branch.commit.tree[path]
        return blob.mime_type

def get_blob_text(repopath, path, branchname='master'):
    repo = Repo(repopath)
    git = repo.git
    text = None
    text = git.show('%s:%s' % (branchname, path))
    mime_type = get_mime_type(repo, branchname, path)
    try:
        lexer = get_lexer_for_mimetype(mime_type)
    except ClassNotFound:
        lexer = get_lexer_by_name('text')
    formatter = HtmlFormatter(linenos=True, lineanchors='line', anchorlinenos=True)
    result = highlight(Markup(text).unescape(), lexer, formatter)
    return result

def show_commit_index(repopath='', branchname='master', page=1):
    '''
    Provides the index data for commits.

    :arg repopath: Path to the git repo
    :arg branchname: Branch we want to show, default is `master`.
    :arg page: Integer pagenumber
    '''
    repo = Repo(repopath)
    skip = (page - 1 ) * 5
    itercommits = repo.iter_commits(branchname, max_count=5, skip=skip)
    result = []
    for com in itercommits:
        data = {}
        data['author'] = com.author
        data['text'] = com.summary
        data['hex'] = com.hexsha
        data['time'] = time.asctime(time.gmtime(com.committed_date))
        result.append(data)

    return result
