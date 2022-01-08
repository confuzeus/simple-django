import os
import environ
from django.contrib import messages
from django.urls import reverse_lazy

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

env = environ.Env()

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool("DJANGO_DEBUG")

TEST = env.bool("DJANGO_TEST", False)

PROJECT_NAME = "{{ cookiecutter.project_name }}"

DOMAIN_NAME = "{{ cookiecutter.domain_name }}"

# Internationalization
# https://docs.djangoproject.com/en/{{ cookiecutter.django_version }}/topics/i18n/

# https://docs.djangoproject.com/en/{{ cookiecutter.django_version }}/ref/settings/#language-code
LANGUAGE_CODE = '{{ cookiecutter.language_code }}'

TIME_ZONE = '{{ cookiecutter.timezone }}'

# https://docs.djangoproject.com/en/{{ cookiecutter.django_version }}/ref/settings/#use-i18n
USE_I18N = True

# https://docs.djangoproject.com/en/{{ cookiecutter.django_version }}/ref/settings/#use-l10n
USE_L10N = True

# https://docs.djangoproject.com/en/{{ cookiecutter.django_version }}/ref/settings/#use-tz
USE_TZ = True

# https://docs.djangoproject.com/en/{{ cookiecutter.django_version }}/ref/settings/#site-id
SITE_ID = 1

# https://docs.djangoproject.com/en/{{ cookiecutter.django_version }}/ref/settings/#locale-paths
LOCALE_PATHS = [os.path.join(BASE_DIR, "locale"),]

# DATABASES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/{{ cookiecutter.django_version }}/ref/settings/#databases
DATABASES = {
    "default": {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env.str("POSTGRES_DB"),
        'USER': env.str("POSTGRES_USER"),
        'PASSWORD': env.str("POSTGRES_PASSWORD"),
        'HOST': env.str("POSTGRES_HOST"),
        'PORT': env.str("POSTGRES_PORT"),
        'ATOMIC_REQUESTS': True
    }
}

if not DEBUG:
    DATABASES["default"]["CONN_MAX_AGE"] = env.int("DJANGO_DB_CONN_MAX_AGE", default=60)


# Default primary key field type
# https://docs.djangoproject.com/en/{{ cookiecutter.django_version }}/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# URLS
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/{{ cookiecutter.django_version }}/ref/settings/#root-urlconf
ROOT_URLCONF = "config.urls"

# https://docs.djangoproject.com/en/{{ cookiecutter.django_version }}/ref/settings/#wsgi-application
WSGI_APPLICATION = 'config.wsgi.application'

# APPS
# ------------------------------------------------------------------------------
DJANGO_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.humanize",
    "django.contrib.admin",
    "django.contrib.sitemaps",
    "django.forms",
]
THIRD_PARTY_APPS = [
    "django_extensions",
    "robots",
    "django_q",
    "allauth",
    "allauth.account",
    'allauth.socialaccount',
    "allauth.socialaccount.providers.google",
    "crispy_forms",
    "crispy_bootstrap5",
    "zen_queries",
]

LOCAL_APPS = [
    '{{ cookiecutter.project_slug }}.core',
    '{{ cookiecutter.project_slug }}.accounts',
]
# https://docs.djangoproject.com/en/{{ cookiecutter.django_version }}/ref/settings/#installed-apps
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

if DEBUG or TEST:
    INSTALLED_APPS = ["whitenoise.runserver_nostatic"] + INSTALLED_APPS
    INSTALLED_APPS += ["debug_toolbar"]

# AUTHENTICATION
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/{{ cookiecutter.django_version }}/ref/settings/#authentication-backends
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    'allauth.account.auth_backends.AuthenticationBackend',
]
# https://docs.djangoproject.com/en/{{ cookiecutter.django_version }}/ref/settings/#auth-user-model
AUTH_USER_MODEL = "accounts.User"
# https://docs.djangoproject.com/en/{{ cookiecutter.django_version }}/ref/settings/#login-redirect-url
LOGIN_REDIRECT_URL = "home"
# https://docs.djangoproject.com/en/{{ cookiecutter.django_version }}/ref/settings/#login-url
LOGIN_URL = "account_login"


# PASSWORDS
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/{{ cookiecutter.django_version }}/ref/settings/#password-hashers
if DEBUG or TEST:
    PASSWORD_HASHERS = ['django.contrib.auth.hashers.MD5PasswordHasher',]
else:
    PASSWORD_HASHERS = [
        # https://docs.djangoproject.com/en/{{ cookiecutter.django_version }}/topics/auth/passwords/#using-argon2-with-django
        "django.contrib.auth.hashers.Argon2PasswordHasher",
        "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
        "django.contrib.auth.hashers.PBKDF2PasswordHasher",
        "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    ]

# Password validation
# https://docs.djangoproject.com/en/{{ cookiecutter.django_version }}/ref/settings/#auth-password-validators

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

# MIDDLEWARE
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/{{ cookiecutter.django_version }}/ref/settings/#middleware
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

if DEBUG or TEST:
    MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]

    def show_toolbar(request):
        return True

    DEBUG_TOOLBAR_CONFIG = {
        "DISABLE_PANELS": ["debug_toolbar.panels.redirects.RedirectsPanel"],
        "SHOW_TEMPLATE_CONTEXT": True,
        "SHOW_TOOLBAR_CALLBACK": show_toolbar,
    }

    INTERNAL_IPS = ["127.0.0.1",]

# STATIC
# ------------------------------------------------------------------------------
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
# https://docs.djangoproject.com/en/{{ cookiecutter.django_version }}/ref/settings/#static-root
STATIC_ROOT = os.path.join(BASE_DIR, 'static_collected')

STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]

# https://docs.djangoproject.com/en/{{ cookiecutter.django_version }}/ref/settings/#static-url
STATIC_URL = "/static/"

# https://docs.djangoproject.com/en/{{ cookiecutter.django_version }}/ref/contrib/staticfiles/#staticfiles-finders
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]


# MEDIA
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/{{ cookiecutter.django_version }}/ref/settings/#media-root
MEDIA_ROOT = env.str("DJANGO_MEDIA_ROOT", os.path.join(BASE_DIR, 'media'))

# https://docs.djangoproject.com/en/{{ cookiecutter.django_version }}/ref/settings/#media-url

if DEBUG or TEST:
    MEDIA_URL = "/media/"
else:
    MEDIA_URL = "https://media.{{ cookiecutter.domain_name }}/"


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates'),],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
            ],
            'debug': DEBUG or TEST
        },
    },
]

THIRD_PARTY_CONTEXT_PROCESSORS = [
    
]

OWN_CONTEXT_PROCESSORS = [
    '{{ cookiecutter.project_slug }}.core.context_processors.site_data',
]

TEMPLATES[0]['OPTIONS']['context_processors'] += THIRD_PARTY_CONTEXT_PROCESSORS + OWN_CONTEXT_PROCESSORS

# https://docs.djangoproject.com/en/{{ cookiecutter.django_version }}/ref/settings/#form-renderer
FORM_RENDERER = "django.forms.renderers.TemplatesSetting"

# Crispy forms

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"

CRISPY_TEMPLATE_PACK = "bootstrap5"

# SECURITY
# ------------------------------------------------------------------------------
SECRET_KEY = env("DJANGO_SECRET_KEY")

ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS")

if not DEBUG:
    # https://docs.djangoproject.com/en/{{ cookiecutter.django_version }}/ref/settings/#session-cookie-httponly
    SESSION_COOKIE_HTTPONLY = True

    # https://docs.djangoproject.com/en/{{ cookiecutter.django_version }}/ref/settings/#csrf-cookie-httponly
    CSRF_COOKIE_HTTPONLY = False

    # https://docs.djangoproject.com/en/{{ cookiecutter.django_version }}/ref/settings/#secure-browser-xss-filter
    SECURE_BROWSER_XSS_FILTER = True

    # https://docs.djangoproject.com/en/{{ cookiecutter.django_version }}/ref/settings/#x-frame-options
    X_FRAME_OPTIONS = "DENY"

    # https://docs.djangoproject.com/en/{{ cookiecutter.django_version }}/ref/settings/#secure-proxy-ssl-header
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

    # https://docs.djangoproject.com/en/{{ cookiecutter.django_version }}/ref/settings/#session-cookie-secure
    SESSION_COOKIE_SECURE = True

    # https://docs.djangoproject.com/en/{{ cookiecutter.django_version }}/ref/settings/#csrf-cookie-secure
    CSRF_COOKIE_SECURE = True

    # https://docs.djangoproject.com/en/{{ cookiecutter.django_version }}/topics/security/#ssl-https
    # https://docs.djangoproject.com/en/{{ cookiecutter.django_version }}/ref/settings/#secure-hsts-seconds
    SECURE_HSTS_SECONDS = 518400

    # https://docs.djangoproject.com/en/{{ cookiecutter.django_version }}/ref/settings/#secure-hsts-include-subdomains
    SECURE_HSTS_INCLUDE_SUBDOMAINS = env.bool(
        "DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS", default=True
    )

    # https://docs.djangoproject.com/en/{{ cookiecutter.django_version }}/ref/settings/#secure-hsts-preload
    SECURE_HSTS_PRELOAD = env.bool("DJANGO_SECURE_HSTS_PRELOAD", default=True)

    # https://docs.djangoproject.com/en/{{ cookiecutter.django_version }}/ref/middleware/#x-content-type-options-nosniff
    SECURE_CONTENT_TYPE_NOSNIFF = env.bool(
        "DJANGO_SECURE_CONTENT_TYPE_NOSNIFF", default=True
    )

# EMAIL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/{{ cookiecutter.django_version }}/ref/settings/#email-backend
DEFAULT_FROM_EMAIL = env(
    "DJANGO_DEFAULT_FROM_EMAIL", default="{{ cookiecutter.project_name }} <{{ cookiecutter.email }}>"
)

SERVER_EMAIL = env("DJANGO_SERVER_EMAIL", default=DEFAULT_FROM_EMAIL)

EMAIL_SUBJECT_PREFIX = env(
    "DJANGO_EMAIL_SUBJECT_PREFIX", default="[{{ cookiecutter.project_name }}]"
)

if DEBUG:
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
    EMAIL_HOST = env.str("DJANGO_SMTP_HOST", default="mailhog")
    EMAIL_PORT = env.int("DJANGO_SMTP_PORT", default=1025)
else:
    EMAIL_BACKEND = "anymail.backends.amazon_ses.EmailBackend"
    ANYMAIL = {
        "AMAZON_SES_CLIENT_PARAMS": {
            "aws_access_key_id": env.str("DJANGO_AWS_ACCESS_KEY_ID"),
            "aws_secret_access_key": env.str("DJANGO_AWS_SECRET_ACCESS_KEY"),
            "region_name": env.str("DJANGO_AWS_REGION_NAME"),
            "config": {
                "connect_timeout": 30,
                "read_timeout": 30,
            },
        },
    }

# https://docs.djangoproject.com/en/{{ cookiecutter.django_version }}/ref/settings/#email-timeout
EMAIL_TIMEOUT = 5

# ADMIN
# ------------------------------------------------------------------------------
# Django Admin URL.
ADMIN_URL = env("DJANGO_ADMIN_URL")

# https://docs.djangoproject.com/en/{{ cookiecutter.django_version }}/ref/settings/#admins
ADMINS = [("""{{ cookiecutter.author_name }}""", "{{ cookiecutter.email }}")]
# https://docs.djangoproject.com/en/{{ cookiecutter.django_version }}/ref/settings/#managers
MANAGERS = ADMINS

# LOGGING
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/{{ cookiecutter.django_version }}/ref/settings/#logging
# See https://docs.djangoproject.com/en/{{ cookiecutter.django_version }}/topics/logging for
# more details on how to customize your logging configuration.
if DEBUG:
    LOGGING = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "verbose": {
                "format": "%(levelname)s %(asctime)s %(module)s "
                "%(process)d %(thread)d %(message)s"
            }
        },
        "handlers": {
            "console": {
                "level": "DEBUG",
                "class": "logging.StreamHandler",
                "formatter": "verbose",
            }
        },
        "root": {"level": "DEBUG", "handlers": ["console"]},
    }
else:
    LOGGING = {
        "version": 1,
        "disable_existing_loggers": False,
        "filters": {"require_debug_false": {"()": "django.utils.log.RequireDebugFalse"}},
        "formatters": {
            "verbose": {
                "format": "%(levelname)s %(asctime)s %(module)s "
                "%(process)d %(thread)d %(message)s"
            }
        },
        "handlers": {
            "mail_admins": {
                "level": "ERROR",
                "filters": ["require_debug_false"],
                "class": "django.utils.log.AdminEmailHandler",
            },
            "console": {
                "level": "DEBUG",
                "class": "logging.StreamHandler",
                "formatter": "verbose",
            },
        },
        "root": {"level": "INFO", "handlers": ["console"]},
        "loggers": {
            "django.request": {
                "handlers": ["mail_admins"],
                "level": "ERROR",
                "propagate": True,
            },
            "django.security.DisallowedHost": {
                "level": "ERROR",
                "handlers": ["console", "mail_admins"],
                "propagate": True,
            },
        },
    }

# CACHES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/{{ cookiecutter.django_version }}/ref/settings/#caches

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": env("DJANGO_REDIS_CACHE_URL"),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            # Mimicing memcache behavior.
            # http://niwinz.github.io/django-redis/latest/#_memcached_exceptions_behavior
            "IGNORE_EXCEPTIONS": True,
        },
    }
}

# django-allauth
# https://django-allauth.readthedocs.io/en/latest/configuration.html
# ------------------------------------------------------------------------------
ACCOUNT_ALLOW_REGISTRATION = env.bool("DJANGO_ACCOUNT_ALLOW_REGISTRATION", True)

ACCOUNT_AUTHENTICATION_METHOD = "email"

ACCOUNT_EMAIL_REQUIRED = True

ACCOUNT_EMAIL_VERIFICATION = "mandatory"

ACCOUNT_ADAPTER = "{{ cookiecutter.project_slug }}.accounts.adapters.AccountAdapter"

ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = True

ACCOUNT_SIGNUP_PASSWORD_ENTER_TWICE = False

SOCIALACCOUNT_ADAPTER = "{{ cookiecutter.project_slug }}.accounts.adapters.SocialAccountAdapter"

ACCOUNT_LOGIN_ON_PASSWORD_RESET = True

ACCOUNT_PRESERVE_USERNAME_CASING = False

ACCOUNT_FORMS = {
    "login": "{{ cookiecutter.project_slug }}.accounts.forms.LoginForm",
    "signup": "{{ cookiecutter.project_slug }}.accounts.forms.SignupForm",
    # 'add_email': 'allauth.account.forms.AddEmailForm',
    "change_password": "{{ cookiecutter.project_slug }}.accounts.forms.ChangePasswordForm",
    # 'set_password': 'allauth.account.forms.SetPasswordForm',
    "reset_password": "{{ cookiecutter.project_slug }}.accounts.forms.ResetPasswordForm",
    "reset_password_from_key": "{{ cookiecutter.project_slug }}.accounts.forms.ResetPasswordKeyForm",
    # 'disconnect': 'allauth.socialaccount.forms.DisconnectForm',
}

SOCIALACCOUNT_PROVIDERS = {
    "facebook": {
        "METHOD": "js_sdk",
        "SDK_URL": "//connect.facebook.net/{locale}/sdk.js",
        "SCOPE": ["email", "public_profile"],
        "AUTH_PARAMS": {"auth_type": "reauthenticate"},
        "INIT_PARAMS": {"cookie": True},
        "FIELDS": [
            "id",
            "first_name",
            "last_name",
            "middle_name",
            "name",
            "name_format",
            "picture",
            "short_name",
        ],
        "EXCHANGE_TOKEN": True,
        "LOCALE_FUNC": lambda request: "en_US",
        "VERIFIED_EMAIL": False,
        "VERSION": "v7.0",
    },
    "google": {
        "SCOPE": [
            "profile",
            "email",
        ],
        "AUTH_PARAMS": {
            "access_type": "online",
        },
    },
}

# Captcha

HCAPTCHA_SECRET_KEY = env.str("HCAPTCHA_SECRET_KEY")

HCAPTCHA_SITE_KEY = env.str("HCAPTCHA_SITE_KEY")

# django.contrib.messages

MESSAGE_TAGS = {
    messages.DEBUG: "debug",
    messages.INFO: "info",
    messages.SUCCESS: "success",
    messages.WARNING: "warning",
    messages.ERROR: "danger",  # 'error' by default
}

# Django q

Q_CLUSTER = {
    'name': '{{ cookiecutter.project_slug }}',
    'workers': 4,
    'recycle': 500,
    'timeout': 60,
    'compress': True,
    'save_limit': 250,
    'queue_limit': 500,
    'cpu_affinity': 1,
    'label': 'Django Q',
    'django_redis': 'default'
}

# sorl thumbnail

THUMBNAIL_QUALITY = 70

THUMBNAIL_KVSTORE = "sorl.thumbnail.kvstores.redis_kvstore.KVStore"

THUMBNAIL_ENGINE = "sorl.thumbnail.engines.convert_engine.Engine"

THUMBNAIL_CONVERT = "gm convert"

THUMBNAIL_IDENTIFY = "gm identify"

THUMBNAIL_REDIS_HOST = env.str("SORL_REDIS_HOST")

THUMBNAIL_PRESERVE_FORMAT = True