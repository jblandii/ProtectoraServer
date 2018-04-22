# -*- coding: utf-8 -*-

import settings
#Add Django Debug Toolbar application. (It's cool.)
EXTRA_MIDDLEWARE_CLASSES = (
    #'debug_toolbar.middleware.DebugToolbarMiddleware',
)

EXTRA_INSTALLED_APPS = (
    #'debug_toolbar',
    #'south',
)

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR+'/dbsqlite',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

#gunicorn
#DEBUG_TOOLBAR_PATCH_SETTINGS = False

"""HEROKU SETTINGS
# Parse database configuration from $DATABASE_URL
import dj_database_url
DATABASES['default'] =  dj_database_url.config()

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allow all host headers
ALLOWED_HOSTS = ['*']"""
