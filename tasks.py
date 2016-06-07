import os

from invoke import run, task

VENV_DIR = os.path.join(os.path.dirname(__file__), '.venv')


@task
def init():
    mkvenv(VENV_DIR, version='3.5')
    run_in_venv('pip install -r requirements.txt')


@task
def analyze(in_video, out_html):
    run_in_venv('python main.py "{}" -o "{}"'.format(in_video, out_html))


@task
def run_in_venv(command):
    kwargs = {'echo': True}
    if os.name != 'nt':
        kwargs['pty'] = True
    run(venv_activate_wrap(command, VENV_DIR), **kwargs)


def mkdir(path):
    if not os.path.exists(path):
        mkdir(os.path.dirname(path))
        os.mkdir(path)


def mkvenv(venv_path, version='3'):
    if os.name == 'nt':
        cmd = 'py -{0} -q -V'.format(version)
        r = run(cmd, warn=True)
        if not r.ok:
            raise RuntimeError('"{0}" do\'t work =/. Try reinstall Python or '
                               'check PATH environment variable'.format(cmd))
        return run("py -{0} -m venv {1}".format(version, venv_path))

    return run('virtualenv --python=python{1} "{0}"'
               .format(venv_path, version))


def venv_activate_wrap(cmd, path):
    venv_bin_path = os.path.join(path, 'bin')
    if os.name == 'nt':
        venv_bin_path = os.path.join(path, 'Scripts')

    active_path = os.path.normpath(os.path.join(venv_bin_path, 'activate'))
    wrapped_cmd = '. ' + active_path + " && " + cmd
    if os.name == 'nt':
        wrapped_cmd = active_path + ' && ' + cmd
    return "({})".format(wrapped_cmd)
