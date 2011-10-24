from setuptools import setup
import gitlog
setup(
    name='gitlog',
    version=gitlog.__version__,
    description='git admin',
    classifiers = [ 'Development Status :: 3 - Alpha',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    author='Mitko Masarliev',
    author_email='mitko@masarliev.net',
    url='http://dev.masarliev.net',
    packages=['gitlog', 'gitlog.templatetags'],
    package_data={ 'gitlog' : ['templates/gitlog/*.html', 'templates/gitlog/repositories/*.html', 'templates/gitlog/account/*.html']},
    zip_safe=False,
    install_requires=['GitPython >=0.3.2', 'Pygments >=1.4', 'Django >=1.3', 'ConfigObj >=4.7.2', 'Makrdown >=2.0.3'],
)

