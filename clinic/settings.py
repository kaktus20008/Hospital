from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/6.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-=%(817=28ux*#%qi929khicvsh%*pm)6(xm-!h=q@-m499657q'

DEBUG = True
ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'django.contrib.sessions',
    'app',
]

MIDDLEWARE = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.common.CommonMiddleware',
]

ROOT_URLCONF = 'clinic.urls'

TEMPLATES = [{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [],
    'APP_DIRS': True,
    'OPTIONS': {
        'context_processors': [],
    },
}]

WSGI_APPLICATION = 'clinic.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'mssql',
        'NAME': 'Hospital_Tyrin_3ISP965',
        'HOST': 'localhost',
        'PORT': '',
        'OPTIONS': {
            'driver': 'ODBC Driver 18 for SQL Server',
            'extra_params': 'Trusted_Connection=yes;TrustServerCertificate=yes;',
        },
    }
}

LANGUAGE_CODE = 'ru-ru'
TIME_ZONE = 'Europe/Moscow'
USE_I18N = True
USE_TZ = False

SESSION_ENGINE = 'django.contrib.sessions.backends.signed_cookies'
MIGRATION_MODULES = {'sessions': None}

STATIC_URL = 'static/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'