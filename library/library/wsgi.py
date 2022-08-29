"""
WSGI config for library project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/wsgi/
"""

import os
import sys

python_home = '/home/kai_reytsu/.local/share/virtualenvs/book_library-8l-tcd1l'
sys.path.append(python_home)

activate_this = python_home + '/bin/activate_this.py'
exec(open(activate_this).read(), dict(__file__=activate_this))
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library.settings')

application = get_wsgi_application()
