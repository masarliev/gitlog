GitLog is gitoris administration tool and repository browser build on django.

Python version must be greater than or equal to **2.6**


Requirements
---
- Django >= 1.3
- Pygments >= 1.4
- GitPython >= 0.3.2
- Makrdown >= 2.0.3
- South >= 0.7.2

Instalation
---

1. Register these following applications in the INSTALLED_APPS section of your project’s settings
 > 'gitlog', 'django.contrib.markup',
2. Add these following template context processors if not already present.
 > 'django.core.context_processors.static', 'gitlog.context_processors.gitlog'
4. Run following commands

 > python manage.py syncdb --all
 > python manage.py migrate --fake
 > python manage.py collectstatic

 > sudo python manage runserver


Configuration
---
See **gitlog/settings.py** for available settings.
