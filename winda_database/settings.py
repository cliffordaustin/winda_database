"""
Django settings for winda_database project.

Generated by 'django-admin startproject using Django 3.2.6.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from pathlib import Path
import os
import json
import requests

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("WINDA_SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get("WINDA_DEBUG_VALUE") == "True"

ALLOWED_HOSTS = ["winda-database.herokuapp.com", "127.0.0.1", "localhost"]


INSTALLED_APPS = [
    "admin_interface",
    "colorfield",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "django.contrib.postgres",
    "allauth",
    "allauth.account",
    "dj_rest_auth.registration",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.google",
    "allauth.socialaccount.providers.facebook",
    "nested_inline",
    "anymail",
    "rest_framework",
    "rest_framework.authtoken",
    "dj_rest_auth",
    "phonenumber_field",
    "django_filters",
    "corsheaders",
    "imagekit",
    "tinymce",
    "user",
    "lodging",
    "activities",
    "transport",
    "recommended_trip",
    "curated_trip",
    "trip",
    "blog",
    "django_cleanup.apps.CleanupConfig",
]


TINYMCE_DEFAULT_CONFIG = {
    "height": "320px",
    "width": "960px",
    "menubar": "file edit view insert format tools table help",
    "plugins": "advlist autolink lists link image charmap print preview anchor searchreplace visualblocks code "
    "fullscreen insertdatetime media table paste code help wordcount spellchecker",
    "toolbar": "undo redo | bold italic underline strikethrough | fontselect fontsizeselect formatselect | alignleft "
    "aligncenter alignright alignjustify | outdent indent |  numlist bullist checklist | forecolor "
    "backcolor casechange permanentpen formatpainter removeformat | pagebreak | charmap emoticons | "
    "fullscreen  preview save print | insertfile image media pageembed template link anchor codesample | "
    "a11ycheck ltr rtl | showcomments addcomment code",
}

X_FRAME_OPTIONS = "SAMEORIGIN"
SILENCED_SYSTEM_CHECKS = ["security.W019"]

REST_FRAMEWORK = {
    "DEFAULT_FILTER_BACKENDS": ["django_filters.rest_framework.DjangoFilterBackend"],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
    "PAGE_SIZE": 100,
    "DEFAULT_PERMISSION_CLASSES": ("core.api.permissions.DenyAny",),
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_jwt.authentication.JSONWebTokenAuthentication",
    ),
}


COGNITO_AWS_REGION = "eu-west-2"
COGNITO_USER_POOL = "eu-west-2_yuwnSe3Jo"
COGNITO_AUDIENCE = None
COGNITO_POOL_URL = (
    None  # will be set few lines of code later, if configuration provided
)

rsa_keys = {}

if COGNITO_AWS_REGION and COGNITO_USER_POOL:
    COGNITO_POOL_URL = (
        f"https://cognito-idp.{COGNITO_AWS_REGION}.amazonaws.com/{COGNITO_USER_POOL}"
    )
    pool_jwks_url = f"{COGNITO_POOL_URL}/.well-known/jwks.json"

    try:
        response = requests.get(pool_jwks_url)
        response.raise_for_status()  # Raise an exception for HTTP errors (e.g., 404)

        rsa_keys = response.json()
        rsa_keys = {key["kid"]: json.dumps(key) for key in rsa_keys["keys"]}
    except requests.exceptions.RequestException as e:
        # Handle any exceptions that might occur during the HTTP request.
        print(f"Error fetching JWKS from Cognito: {str(e)}")


JWT_AUTH = {
    "JWT_PAYLOAD_GET_USERNAME_HANDLER": "core.api.jwt.get_username_from_payload_handler",
    "JWT_DECODE_HANDLER": "core.api.jwt.cognito_jwt_decode_handler",
    "JWT_PUBLIC_KEY": rsa_keys,
    "JWT_ALGORITHM": "RS256",
    "JWT_AUDIENCE": COGNITO_AUDIENCE,
    "JWT_ISSUER": COGNITO_POOL_URL,
    "JWT_AUTH_HEADER_PREFIX": "Bearer",
}


MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.auth.middleware.RemoteUserMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
]

if DEBUG:
    CORS_ALLOWED_ORIGINS = [
        "http://localhost:3000",
        "http://localhost:3001",
    ]
else:
    CORS_ALLOWED_ORIGINS = [
        "https://www.winda.guide",
        "https://winda.guide",
        "https://www.windastays.com",
        "http://localhost:3000",
        "https://windastays.com",
        "https://windapartner.vercel.app",
        "https://www.safaripricer.com",
    ]


ROOT_URLCONF = "winda_database.urls"


TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "winda_database.wsgi.application"

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.RemoteUserBackend",
    "django.contrib.auth.backends.ModelBackend",
]

AUTH_USER_MODEL = "user.CustomUser"

REST_AUTH_REGISTER_SERIALIZERS = {
    "REGISTER_SERIALIZER": "user.api.serializer.RegisterSerializer",
    # 'PASSWORD_RESET_SERIALIZER':'winda_database.adapter.CustomPasswordResetSerializer',
}

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
    }
}

import dj_database_url

if DEBUG:
    DATABASES["default"] = {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("WINDA_DATABASE_NAME"),
        "USER": os.environ.get("WINDA_DATABASE_USER"),
        "PASSWORD": os.environ.get("WINDA_DATABASE_PASSWORD"),
        "HOST": os.environ.get("WINDA_DATABASE_HOST"),
    }
else:
    db_from_env = dj_database_url.config(default=os.environ.get("DATABASE_URL"))
    DATABASES["default"].update(db_from_env)


DATA_UPLOAD_MAX_NUMBER_FIELDS = 10240


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


FRONTEND_URL = ""

if DEBUG:
    FRONTEND_URL = "http://localhost:3000"
else:
    FRONTEND_URL = "https://www.safaripricer.com"


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATIC_URL = "/static/"


MEDIA_ROOT = os.path.join(BASE_DIR, "media")

MEDIA_URL = "/media/"


SOCAILACCOUNT_PROVIDERS = {
    "google": {
        "APP": {
            "client_id": os.environ.get("WINDA_SOCIAL_AUTH_GOOGLE_OAUTH2_KEY"),
            "secret": os.environ.get("WINDA_SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET"),
        }
    }
}


EMAIL_BACKEND = "anymail.backends.mailjet.EmailBackend"

ANYMAIL = {
    "MAILJET_API_KEY": os.environ.get("WINDA_MAILJET_API_KEY"),
    "MAILJET_SECRET_KEY": os.environ.get("WINDA_MAILJET_SECRET_KEY"),
}
DEFAULT_FROM_EMAIL = os.environ.get("DEFAULT_FROM_EMAIL")


# EMAIL_HOST = os.environ.get("WINDA_SMTP_HOST")
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True
# EMAIL_HOST_USER = os.environ.get("WINDA_SMTP_USER")
# EMAIL_HOST_PASSWORD = os.environ.get("WINDA_SMTP_PASSWORD")

# AWS_SES_REGION_NAME = "eu-west-2"
# AWS_SES_REGION_ENDPOINT = "email.eu-west-2.amazonaws.com"

ACCOUNT_EMAIL_VERIFICATION = "mandatory"
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = True
ACCOUNT_EMAIL_CONFIRMATION_COOLDOWN = 110
OLD_PASSWORD_FIELD_ENABLED = True
ACCOUNT_ADAPTER = "winda_database.adapter.DefaultAccountAdapterCustom"

# ACCOUNT_EMAIL_SUBJECT_PREFIX = ""
ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_USER_MODEL_USERNAME_FIELD = None

# LOGIN_ON_EMAIL_CONFIRMATION = False


AWS_ACCESS_KEY_ID = os.environ.get("WINDA_AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.environ.get("WINDA_AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = os.environ.get("WINDA_AWS_STORAGE_BUCKET_NAME")

AWS_S3_FILE_OVERWRITE = False

DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"

AWS_S3_REGION_NAME = "eu-west-2"
AWS_S3_SIGNATURE_VERSION = "s3v4"


SITE_ID = 2


# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
