# SECURITY WARNING: keep the secret key used in production secret!
import os


SECRET_KEY = '&kz!1c*2(q)stzzso5$k@gqz7u@kd13x@!re86^edvh-xi%(rl'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['51.20.9.159']

EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
    }
}