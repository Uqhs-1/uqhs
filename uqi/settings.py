"""
Django settings for uqi project.

Generated by 'django-admin startproject' using Django 2.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'cg#p$g+j9tax!#a3cup@1$8obt2_+&k3q+pmu)5%asj6yjpkag')
DEBUG = os.environ.get('DJANGO_DEBUG', '') != 'False'

                      
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
#AUTH_USER_MODEL = 'score_log.User'
# The URL to use when referring to static files (where they will be served from)
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)###

settings_dir = os.path.dirname(__file__)
PROJECT_ROOT = os.path.abspath(os.path.dirname(settings_dir))
FILES_FOLDER = os.path.join(PROJECT_ROOT, 'file_folder/')
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
#SECRET_KEY = 'dqtx4k0&m9expsji^cwgqec=3vmc0cyk-k_8^50ei5_0$b!ub='

# SECURITY WARNING: don't run with debug turned on in production!
#DEBUG = True

#ALLOWED_HOSTS = []
ALLOWED_HOSTS = ['uqhs.herokuapp.com', '127.0.0.1', 'uqhi.herokuapp.com']
#add email settings
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'uqhs2019@gmail.com'
EMAIL_HOST_PASSWORD = 'Ll018311'
DEFAULT_FROM_EMAIL = 'uqhs2019@gmail.com'

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'book_shelf.apps.BookShelfConfig',
    'result.apps.ResultConfig',
    'crispy_forms',
    'corsheaders',
    #How to Use Bootstrap 4 Forms With Django
]

#CRISPY_TEMPLATE_PACK = 'bootstrap4'
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.common.corsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

CORS_ALLOWED_ORIGINS = [
   #"https://example.com",
    #"https://sub.example.com",
    "http://localhost:8838",
    "http://127.0.0.1:8838"
]


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
ROOT_URLCONF = 'uqi.urls'
AUTH_PROFILE_MODULE = 'result.Edit_User'
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates'),],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                #'result.context_processors.logon_images',
            ],
        },
    },
]

WSGI_APPLICATION = 'uqi.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Africa/Lagos'

USE_I18N = True

USE_L10N = True

USE_TZ = False




import dj_database_url
db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(db_from_env)
###for image upload
MEDIA_URL = '/result/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'result')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

# The absolute path to the directory where collectstatic will collect static files for deployment.
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# The URL to use when referring to static files (where they will be served from)
STATIC_URL = '/static/'


