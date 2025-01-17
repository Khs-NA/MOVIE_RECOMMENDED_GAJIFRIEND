"""
Django settings for my_api project.

Generated by 'django-admin startproject' using Django 4.2.4.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
#environ을 기존 import에 추가
import environ
import os
import json

env = environ.Env(DEBUG=(bool, True)) #환경변수를 불러올 수 있는 상태로 세팅

BASE_DIR = Path(__file__).resolve().parent.parent

#환경변수 파일 읽어오기
environ.Env.read_env(
    env_file=os.path.join(BASE_DIR, '.env')
)

VITE_TMDB_API_KEY = env('VITE_TMDB_API_KEY') #SECEREY_KEY 값 불러오기


# Build paths inside the project like this: BASE_DIR / 'subdir'.


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = (
    'django-insecure-@fn#327r=8uv%&a25(l(jc-e5ir*pu)v_%cyy*l%u@o)(^fnzs'
)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition
INSTALLED_APPS = [
    'community',
    'movies',
    'accounts',
    'rest_framework',
    'rest_framework.authtoken',
    # 'dj_rest_auth',
    'corsheaders',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'dj_rest_auth.registration',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

SITE_ID = 1

REST_FRAMEWORK = {
    # Authentication
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        
    ],
#     # permission
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ],
}

ACCOUNT_EMAIL_VERIFICATION = 'none'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]

CORS_ALLOWED_ORIGINS = [
    'http://127.0.0.1:5173',
    'http://localhost:5173',
]


ROOT_URLCONF = 'project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'ko-KR'

TIME_ZONE = 'Asia/Seoul'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'
# STATICFILES_DIRS = [
#     BASE_DIR / 'static',
#     ]
# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'accounts.User'


REST_AUTH = {
 'REGISTER_SERIALIZER': 'accounts.serializers.CustomRegisterSerializer',
 'USER_DETAILS_SERIALIZER': 'accounts.serializers.CustomUserDetailsSerializer',

}



MEDIA_ROOT = BASE_DIR / 'media'
MEDIA_URL = '/media/'


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

ACCOUNT_ADAPTER = 'accounts.adapters.CustomAccountAdapter'

# json 파일 불러오기 - loc
LOC_JSON_PATH = os.path.join(BASE_DIR, 'asset', 'loc.json')

# loc.json 파일 읽기
with open(LOC_JSON_PATH, 'r', encoding='utf-8') as f:
    LOCATION_DATA = json.load(f)

# do_city.json 파일 경로 설정
DO_CITY_JSON_PATH = os.path.join(BASE_DIR, 'asset', 'do_city.json')

# do_city.json 파일 읽기
with open(DO_CITY_JSON_PATH, 'r', encoding='utf-8') as f:
    DO_CITY_DATA = json.load(f)


REST_AUTH = {
 'REGISTER_SERIALIZER': 'accounts.serializers.CustomRegisterSerializer',
 'USER_DETAILS_SERIALIZER': 'accounts.serializers.CustomUserDetailsSerializer',

}



MEDIA_ROOT = BASE_DIR / 'media'
MEDIA_URL = '/media/'


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

ACCOUNT_ADAPTER = 'accounts.adapters.CustomAccountAdapter'

# json 파일 불러오기 - loc
LOC_JSON_PATH = os.path.join(BASE_DIR, 'asset', 'loc.json')

# loc.json 파일 읽기
with open(LOC_JSON_PATH, 'r', encoding='utf-8') as f:
    LOCATION_DATA = json.load(f)

# do_city.json 파일 경로 설정
DO_CITY_JSON_PATH = os.path.join(BASE_DIR, 'asset', 'do_city.json')

# do_city.json 파일 읽기
with open(DO_CITY_JSON_PATH, 'r', encoding='utf-8') as f:
    DO_CITY_DATA = json.load(f)