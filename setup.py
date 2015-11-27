import os
import sys
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.txt')).read()
CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()

requires = [
    'scarab-util',
    'BeautifulSoup',
    'requests',
    'celery[redis]',
    'pyramid==1.6b2',
    'SQLAlchemy',
    'transaction',
    'pyramid_tm',
    'pyramid_debugtoolbar',
    'pyramid-jinja2',
    'zope.sqlalchemy',
    'formencode',
    'lxml',
    'webtest',
    'waitress',
    #'MySQL-python',
    #'PyMySQL', #pure python
    #'uwsgi',
    'psycopg2', #for postgresql, there is only non-pure pyhton lib
    'pytest-capturelog',
    'pytest-cov',
    'pytest',
    ]


class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', 'Arguments to pass to py.test')]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []

    def finalize_options(self):
        TestCommand.finalize_options(self)
        #self.test_args = ["-s", "-m", "voice"]
        self.test_args = []
        self.test_suite = True

    def run(self):
        import pytest
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)


setup(name='scarab',
      version='0.1',
      description='scarab',
      long_description=README + '\n\n' + CHANGES,
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Pyramid",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
      author='samuelololol',
      author_email='samuelololol@gmail.com',
      url='',
      keywords='web wsgi pylons pyramid',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      test_suite='scarab',
      tests_require=['pytest', 'webtest'],
      cmdclass = {'test': PyTest},
      install_requires=requires,
      dependency_links=['https://github.com/samuelololol/scarab_util/archive/master.zip#egg=scarab_util'],
      entry_points="""\
      [paste.app_factory]
      main = scarab:main
      [console_scripts]
      initialize_scarab_db = scarab.scripts.initializedb:main
      """,
      )

