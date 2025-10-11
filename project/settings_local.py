# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-ku2xz^ufkx-e^x*m26$f#bc%dd+rjyu@cug*f$yc)n*eq3&cje'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'theaterdb',
        'USER': 'master',
        'PASSWORD': 'mainpass132',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}