import os
from pathlib import Path
from environ import Env

env = Env()
Env.read_env()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = env.str('SECRET_KEY')

DEBUG = env.bool('DEBUG', default=True)

ALLOWED_HOSTS = ['*']

if env.bool('PROD', default=False):
    ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'f3dd-2800-bf0-8014-9d-8c87-63c-34e1-35d.ngrok-free.app']

CSRF_TRUSTED_ORIGINS = ['https://f3dd-2800-bf0-8014-9d-8c87-63c-34e1-35d.ngrok-free.app']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core',
    'dashboard',
    'accounts',
    'corsheaders',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'core.context.context_processors.drawer'
            ],
        },
    },
]

WSGI_APPLICATION = 'project.wsgi.application'

X_FRAME_OPTIONS = 'ALLOWALL'
CORS_ALLOW_ALL_ORIGINS = True


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': env.str('DATABASE_NAME_LOCAL'),
        'USER': env.str('DATABASE_USER_LOCAL'),
        'PASSWORD': env.str('DATABASE_PASSWORD_LOCAL'),
        'HOST': env.str('DATABASE_HOST_LOCAL'),
        'PORT': '',
    }
}

# if env.bool('PROD', default=False):
#     DATABASES = {
#         'default': {
#             'ENGINE': 'django.db.backends.postgresql',
#             'NAME': env.str('DATABASE_NAME'),
#             'USER': env.str('DATABASE_USER'),
#             'PASSWORD': env.str('DATABASE_PASSWORD'),
#             'HOST': env.str('DATABASE_HOST'),
#             'PORT': env.str('DATABASE_PORT'),
#         }
#     }

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'es'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

MEDIA_PATH = os.path.abspath(os.path.dirname(__name__))
# MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(MEDIA_PATH, 'media')

STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(
    MEDIA_PATH, 'static'), os.path.join(MEDIA_PATH, 'media')]
STATIC_ROOT = os.path.join(MEDIA_PATH, 'local-cdn', 'static')

# AWS_S3_REGION_NAME = 'us-east-2'
# AWS_STORAGE_BUCKET_NAME = env.str('AWS_STORAGE_BUCKET_NAME')
# MEDIA_URL = f'https://{AWS_STORAGE_BUCKET_NAME}.s3.{AWS_S3_REGION_NAME}.amazonaws.com/media/'

# S3 Config
# AWS_ACCESS_KEY_ID = env.str('AWS_ACCESS_KEY_ID')
# AWS_SECRET_ACCESS_KEY = env.str('AWS_SECRET_ACCESS_KEY')
# AWS_STORAGE_BUCKET_NAME = env.str('AWS_STORAGE_BUCKET_NAME')

# Smtp
# EMAIL_SUBJECT_PREFIX = ""
# EMAIL_HOST = env.str('EMAIL_HOST')
# EMAIL_HOST_USER = env.str('EMAIL_HOST_USER')
# DEFAULT_FROM_EMAIL = env.str('DEFAULT_FROM_EMAIL')
# EMAIL_HOST_PASSWORD = env.str('EMAIL_HOST_PASSWORD')
# EMAIL_PORT = env.int('EMAIL_PORT', default=587)
# EMAIL_USE_TLS = env.bool('EMAIL_USE_TLS', default=True)
# EMAIL_USE_SSL = env.bool('EMAIL_USE_SSL', default=False)

# Configuración de almacenamiento para S3
# DEFAULT_FILE_STORAGE = 'core.utils.storage_backend.PublicUploadStorage'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'core.user'

LOCAL = False
LOGIN = 'accounts:login'
NOT_ALLOWED = 'dashboard:notAllowed'
