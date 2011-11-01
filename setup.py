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
    packages=['gitlog', 'gitlog.templatetags', 'gitlog.management'],
    package_data={ 'gitlog' : ['templates/*.html', 'templates/projects/*.html', 'templates/account/*.html', 'static/css/*.css', 'static/img/*']},
    zip_safe=False,
    install_requires=[
        'gitpython', 
        'pygments >=1.4', 
        'Django>=1.3',
        'Markdown>=2.0.3',
        'south>=0.7.2', 
        'docutils>=0.8.1'
    ],
)

