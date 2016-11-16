import random
from fabric.api import env, run, local
from fabric.contrib.files import exists, sed, append

REPO_URL = 'https://github.com/ZzAntares/tdd-with-python-exercises'


def _create_directory_structure_if_necessary(site_folder):
    for subfolder in ('database', 'static', 'virtualenv', 'source'):
        run('mkdir -p %s/%s' % (site_folder, subfolder))


def _get_latest_source(source_folder):
    if exists(source_folder + '/.git'):
        run('cd {} && git fetch'.format(source_folder))
    else:
        run('git clone {} {}'.format(REPO_URL, source_folder))

    current_commit = local("git log -n 1 --format=%H", capture=True)
    run('cd {} && git reset --hard {}'.format(source_folder, current_commit))


def _update_settings(source_folder, site_name):
    settings_path = source_folder + '/superlists/settings.py'
    sed(settings_path, "DEBUG = True", "DEBUG = False")
    sed(settings_path,
        'ALLOWED_HOSTS =.+$',
        'ALLOWED_HOSTS = ["{}"]'.format(site_name))

    secret_key_file = source_folder + '/superlists/secret_key.py'
    if not exists(secret_key_file):
        chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
        key = ''.join(random.SystemRandom().choice(chars) for _ in range(50))
        append(secret_key_file, "SECRET_KEY = '{}'".format(key))

    append(settings_path, '\nfrom .secret_key import SECRET_KEY')


def _update_virtualenv(source_folder):
    virtualenv_folder = source_folder + '/../virtualenv'
    pip = virtualenv_folder + '/bin/pip'

    if not exists(pip):
        run('virtualenv --python=python3 {}'.format(virtualenv_folder))

    run('{} install -r {}/requirements.txt'.format(pip, source_folder))


def _update_static_files(source_folder):
    managepy = '../virtualenv/bin/python3 manage.py'
    run('cd {} && {} collectstatic --noinput'.format(source_folder, managepy))


def _update_database(source_folder):
    managepy = '../virtualenv/bin/python3 manage.py'
    run('cd {} && {} migrate --noinput'.format(source_folder, managepy))


def deploy():
    site_folder = '/home/{}/sites/{}'.format(env.user, env.host)
    source_folder = site_folder + '/source'
    _create_directory_structure_if_necessary(site_folder)
    _get_latest_source(source_folder)
    _update_settings(source_folder, env.host)
    _update_virtualenv(source_folder)
    _update_static_files(source_folder)
    _update_database(source_folder)
