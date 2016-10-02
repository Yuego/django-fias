#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
import codecs
import os
import re
import subprocess
import sys

from fias.version import __version__


def execute(cmd):
    assert isinstance(cmd, (list, tuple)), 'cmd must be a list or tuple'

    proc = subprocess.Popen(cmd, cwd=os.path.abspath(os.path.dirname(__name__)),
                            stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
    return proc.communicate()


def check_tag_exists():
    tag_out, tag_err = execute(['git', 'tag', '-l', __version__])

    if tag_out.strip():
        print("Уже существует тег для версии: {0}.".format(__version__))
        sys.exit()


PY3 = sys.version_info[0] == 3

sys.path.insert(0, '..')

if sys.argv[-1] == 'test':
    req_split = re.compile(r'[a-z_][a-z0-9_]+', re.I | re.U | re.M)

    req_file = codecs.open('requirements.txt', mode='r').read()
    test_req_file = codecs.open('test_requirements.txt', mode='r').read()
    test_requirements = req_split.findall(req_file) + req_split.findall(test_req_file)

    try:
        modules = list(map(__import__, test_requirements))
    except ImportError as e:
        err_msg = e.msg.replace("No module named ", "")
        msg = "%s is not installed. Install your test requirments." % err_msg
        raise ImportError(msg)

    os.system('py.test')
    sys.exit()


if sys.argv[-1] == 'tag':
    check_tag_exists()

    os.system("git tag -a %s -m 'version %s'" % (__version__, __version__))
    os.system("git push --tags")
    sys.exit()


if sys.argv[-1] == 'publish':
    check_tag_exists()

    tox_out, tox_err = execute(['tox'])

    sys.stdout.write(tox_out)

    if 'FAILURES' in str(tox_out):
        print('Не все тесты прошли. Нельзя публиковать!')
        sys.exit()

    os.system("python setup.py sdist upload")
    os.system("python setup.py bdist_wheel upload")
    print("Не забудь добавить тег:")
    print("  git tag -a %s -m 'ver.%s'" % (__version__, __version__))
    print("  git push --tags")
    print("Или:")
    print(" python setup.py tag")
    sys.exit()


extra_requirements = []
if PY3:
    extra_requirements = [
        'suds-jurko>=0.6',
    ]
else:
    extra_requirements = [
        'suds>=0.4',
    ]


setup(
    name='django-fias',
    version=__version__,
    author='Artem Vlasov',
    author_email='root@proscript.ru',
    url='https://github.com/Yuego/django-fias',
    download_url='https://github.com/Yuego/django-fias/archive/{0}.tar.gz'.format(__version__),

    description='FIAS Django integration',
    long_description=codecs.open('README.rst', encoding='utf8').read(),

    license='MIT license',
    install_requires=[
        'django >= 1.8, < 1.10',
        'django_select2>=5.3.0',
        # 'zeep>=0.8.0',
        'rarfile',
        'six',
        'lxml',
        'unrar',
        'dbfread>=2.0.5',
        'progress',
    ] + extra_requirements,
    packages=find_packages(exclude=('tests', 'tests.*')),
    include_package_data=True,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: Russian',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
