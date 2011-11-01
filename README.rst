######
GitLog
######
Gitoris repository browser build on django.

************
Requirements
************
* Django >= 1.3
* Pygments >= 1.4
* GitPython >= 0.3.2
* Makrdown >= 2.0.3
* South >= 0.7.2
* Docutils >= 0.8.1

***********
Instalation
***********

1. Register these following applications in the INSTALLED_APPS section of your project’s settings
 * 'gitlog'
 * 'south'
 * 'django.contrib.markup'
2. Add these following template context processors if not already present.
 * 'django.core.context_processors.static'
 * 'gitlog.context_processors.gitlog'
 * 'django.core.context_processors.auth',
 * 'django.core.context_processors.i18n',
 * 'django.core.context_processors.request',
3. Add this in urls.py
 * url(r'^', include('gitlog.urls')),
4. Copy hooks/post-receive to /home/git/repositories/gitosis-admin.git/hooks/, uncomment last 2 lines and fix path
 
5. Run following commands

 * python manage.py syncdb --all
 * python manage.py migrate --fake
 * python manage.py collectstatic

 * sudo python manage runserver

Sudo is required for access to repository directories

*************
Configuration
*************

See *gitlog/settings.py* for available settings.

Users and repositories are managed from post-receive hook. User is created only if it starts with '@'. Example

[group username]

members = user@home user@office


[group repositories]

members = @username

writable = repo1

readonly = repo2


In this case after gitosis-admin push 1 user will be created with username "username" and 2 repositories (repo1, repo2)

Additional and necessary settings

[repo repo1]

owner = username

[repo repo2]

owner = otheruser

[user username]

email = user@email

password = secret
