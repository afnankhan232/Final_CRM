from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = 'django-insecure-l3!d6qap(m@zdf^ap$y&p!88k)!zhca0p-j!6c29zuw^ml6ij_'
SECRET_KEY = os.environ.get("SECRET_KEY") 

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = True
DEBUG = (os.environ.get("DEBUG_VALUE") == "True")

ALLOWED_HOSTS = [
    "CtrlCRM.pythonanywhere.com",
    "http://localhost:8000/",
    "localhost",
    "*",
]


# Application definition

SITE_ID = 3

INSTALLED_APPS = [
    'featuredApp.apps.FeaturedappConfig',
    'client.apps.ClientConfig',
    'accounts.apps.AccountsConfig',

    'crispy_forms',
    'crispy_bootstrap4',
    'widget_tweaks',

    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        }
    }
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]

ROOT_URLCONF = 'projectCRM.urls'

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

                # Custom processor
                'featuredApp.context_processor.accessible_accounts',
            ],
        },
    },
]

WSGI_APPLICATION = 'projectCRM.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

# Change the Time Zone from 'UTC' to 'IST'.
TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# No longer needed
# # Changed Auth model to BusinessUser which allows more specific fields..
# # company email; company name; + AbstractBaseUser + exceptional fields
# AUTH_USER_MODEL = 'accounts.BusinessUser'


AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',  # Default Django backend
    'allauth.account.auth_backends.AuthenticationBackend', # Cutom [GOOGLE LOGIN]
]

# ---- ==== Specific to CRM Software ==== ----

# Crispy forms used at userCreation, userLogin, and other..
CRISPY_TEMPLATE_PACK = 'bootstrap4'

# Added media path (to store logo of company and storing Documents)
# Secured folder can't be accessed directly
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Login and Logout Redirect's
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"

# Set login page
# LOGIN_URL = 'login'

# For local development
# if DEBUG:
#     import mimetypes
#     mimetypes.add_type("image/png", ".png", True)