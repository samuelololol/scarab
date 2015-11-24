import os
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.txt')).read()
CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()

requires = [
    'pyramid==1.6b2',
    'SQLAlchemy',
    'transaction',
    'pyramid_tm',
    'pyramid_debugtoolbar',
    'pyramid-jinja2',
    'zope.sqlalchemy',
    'formencode',
    'waitress',
    #'MySQL-python',
    #'PyMySQL', #pure python
    'celery[redis]',
    'BeautifulSoup',
    'requests',
    #'uwsgi',
    'psycopg2', #for postgresql, there is only non-pure pyhton lib
    'pytest',
    'pytest-capturelog',
    'webtest'
    'scarab-util',
    ]

class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = ["-s"]
        self.test_suite = True

    def run(self):
        import pytest
        pytest.main(self.test_args)

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

