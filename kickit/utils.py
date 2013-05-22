import os
import subprocess

def system(cmd):
    """ 
    Invoke a shell command.
    """
    ret = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE,
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, close_fds=True)
    out, err = ret.communicate()
    return out

def get_files(path):
    '''
    Returns a tuple containing list of directories and files from given git repo.

    :arg path: Path to the git
    '''
    command = 'git --git-dir %s/.git ls' % path
    names = system(command)
    dirs = []
    files = []
    for name in names.split('\n'):
        if name.find('/') != -1:
            dirs.append(name.split('/')[0])
        else:
            files.append(name)

    dirs.sort()
    files.sort()
    return set(dirs), files