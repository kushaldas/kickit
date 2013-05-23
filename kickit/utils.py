import os
import subprocess
from git import Repo

def system(cmd):
    """ 
    Invoke a shell command.
    """
    ret = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE,
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, close_fds=True)
    out, err = ret.communicate()
    return out

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
    #for o in repo.iter_commits():
    #    from ipdb import set_trace;set_trace()
    for head in repo.heads:
        if head.name == name:
            return head

def get_branches(path):
    repo = Repo(path)
    return [r.name for r in repo.heads]

def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()
