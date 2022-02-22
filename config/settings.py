import configparser
from pathlib import Path
from django.core.exceptions import ImproperlyConfigured
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy

BASE_DIR = Path(__file__).resolve().parent.parent

CONFIG_FILE = BASE_DIR / 'appconfig.ini'

if not CONFIG_FILE.is_file():
    raise ImproperlyConfigured(f"appconfig.ini not found in {BASE_DIR}")

app_config = configparser.ConfigParser()

app_config.read(CONFIG_FILE)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = app_config['core'].getboolean("DJANGO_DEBUG", False)

TEST = config['core'].getboolean("DJANGO_TEST", False)

PROJECT_NAME = "Simple Django"

DOMAIN_NAME = "example.com"

PORT_NUMBER = app_config['core'].getboolean("DJANGO_SITE_PORT_NUMBER")

# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

# https://docs.djangoproject.com/en/3.2/ref/settings/#language-code
LANGUAGE_CODE = 'en-us'

LANGUAGES = (
    ("en", _("English")),
)

TIME_ZONE = 'UTC'

# https://docs.djangoproject.com/en/3.2/ref/settings/#use-i18n
USE_I18N = True

# https://docs.djangoproject.com/en/3.2/ref/settings/#use-l10n
USE_L10N = True

# https://docs.djangoproject.com/en/3.2/ref/settings/#use-tz
USE_TZ = True

# https://docs.djangoproject.com/en/3.2/ref/settings/#site-id
SITE_ID = 1

# https://docs.djangoproject.com/en/3.2/ref/settings/#locale-paths
LOCALE_PATHS = [BASE_DIR / 'locale',]

# DATABASES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases
DATABASES = {
    "default": {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': app_config['db'].get("POSTGRES_DB"),
        'USER': app_config['db'].get("POSTGRES_USER"),
        'PASSWORD': app_config['db'].get("POSTGRES_PASSWORD"),
        'HOST': app_config['db'].get("POSTGRES_HOST"),
        'PORT': app_config['db'].get("POSTGRES_PORT"),
        'ATOMIC_REQUESTS': True
    }
}

if not DEBUG:
    DATABASES["default"]["CONN_MAX_AGE"] = app_config['db'].getint("DJANGO_DB_CONN_MAX_AGE", 60)


# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# URLS
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/3.2/ref/settings/#root-urlconf
ROOT_URLCONF = "config.urls"

# https://docs.djangoproject.com/en/3.2/ref/settings/#wsgi-application
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
    "django_q",
    "crispy_forms",
    "crispy_bootstrap5",
    "zen_queries",
    "allcaptcha",
]

LOCAL_APPS = [
    'simple_django.core',
]
# https://docs.djangoproject.com/en/3.2/ref/settings/#installed-apps
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

if DEBUG or TEST:
    INSTALLED_APPS = ["whitenoise.runserver_nostatic"] + INSTALLED_APPS
    INSTALLED_APPS += ["debug_toolbar"]

# AUTHENTICATION
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/3.2/ref/settings/#authentication-backends
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
]
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-user-model
AUTH_USER_MODEL = "core.User"
# https://docs.djangoproject.com/en/3.2/ref/settings/#login-redirect-url
LOGIN_REDIRECT_URL = "home"
# https://docs.djangoproject.com/en/3.2/ref/settings/#login-url
LOGIN_URL = "account_login"


# PASSWORDS
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/3.2/ref/settings/#password-hashers
if DEBUG or TEST:
    PASSWORD_HASHERS = ['django.contrib.auth.hashers.MD5PasswordHasher',]
else:
    PASSWORD_HASHERS = [
        # https://docs.djangoproject.com/en/3.2/topics/auth/passwords/#using-argon2-with-django
        "django.contrib.auth.hashers.Argon2PasswordHasher",
        "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
        "django.contrib.auth.hashers.PBKDF2PasswordHasher",
        "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    ]

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/ref/settings/#middleware
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

    DEBUG_TOOLBAR_CONFIG = {
        "DISABLE_PANELS": ["debug_toolbar.panels.redirects.RedirectsPanel"],
        "SHOW_TEMPLATE_CONTEXT": True,
    }

    INTERNAL_IPS = ["127.0.0.1",]

# STATIC
# ------------------------------------------------------------------------------
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
# https://docs.djangoproject.com/en/3.2/ref/settings/#static-root
STATIC_ROOT = BASE_DIR / 'static_collected'

STATICFILES_DIRS = [BASE_DIR / "static",]

# https://docs.djangoproject.com/en/3.2/ref/settings/#static-url
STATIC_URL = "/static/"

# https://docs.djangoproject.com/en/3.2/ref/contrib/staticfiles/#staticfiles-finders
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]


# MEDIA
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/3.2/ref/settings/#media-root
MEDIA_ROOT = Path(app_config['core'].get("DJANGO_MEDIA_ROOT", BASE_DIR / 'media'))

# https://docs.djangoproject.com/en/3.2/ref/settings/#media-url

if DEBUG or TEST:
    MEDIA_URL = "/media/"
else:
    MEDIA_URL = "https://media.example.com/"


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates',],
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
    'simple_django.core.context_processors.site_data',
]

TEMPLATES[0]['OPTIONS']['context_processors'] += THIRD_PARTY_CONTEXT_PROCESSORS + OWN_CONTEXT_PROCESSORS

# https://docs.djangoproject.com/en/3.2/ref/settings/#form-renderer
FORM_RENDERER = "django.forms.renderers.TemplatesSetting"

# Crispy forms

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"

CRISPY_TEMPLATE_PACK = "bootstrap5"

# SECURITY
# ------------------------------------------------------------------------------
SECRET_KEY = app_config['security'].get("DJANGO_SECRET_KEY")

ALLOWED_HOSTS = app_config['security'].get("DJANGO_ALLOWED_HOSTS").split(',')

if not DEBUG:
    # https://docs.djangoproject.com/en/3.2/ref/settings/#session-cookie-httponly
    SESSION_COOKIE_HTTPONLY = True

    # https://docs.djangoproject.com/en/3.2/ref/settings/#session-engine
    SESSION_ENGINE = "django.contrib.sessions.backends.signed_cookies"

    # https://docs.djangoproject.com/en/3.2/ref/settings/#csrf-cookie-httponly
    CSRF_COOKIE_HTTPONLY = False

    # https://docs.djangoproject.com/en/3.2/ref/settings/#secure-browser-xss-filter
    SECURE_BROWSER_XSS_FILTER = True

    # https://docs.djangoproject.com/en/3.2/ref/settings/#x-frame-options
    X_FRAME_OPTIONS = "DENY"

    # https://docs.djangoproject.com/en/3.2/ref/settings/#secure-proxy-ssl-header
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

    # https://docs.djangoproject.com/en/3.2/ref/settings/#session-cookie-secure
    SESSION_COOKIE_SECURE = True

    # https://docs.djangoproject.com/en/3.2/ref/settings/#csrf-cookie-secure
    CSRF_COOKIE_SECURE = True

    # https://docs.djangoproject.com/en/3.2/topics/security/#ssl-https
    # https://docs.djangoproject.com/en/3.2/ref/settings/#secure-hsts-seconds
    SECURE_HSTS_SECONDS = 518400

    # https://docs.djangoproject.com/en/3.2/ref/settings/#secure-hsts-include-subdomains
    SECURE_HSTS_INCLUDE_SUBDOMAINS = env.bool(
        "DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS", default=True
    )

    # https://docs.djangoproject.com/en/3.2/ref/settings/#secure-hsts-preload
    SECURE_HSTS_PRELOAD = env.bool("DJANGO_SECURE_HSTS_PRELOAD", default=True)

    # https://docs.djangoproject.com/en/3.2/ref/middleware/#x-content-type-options-nosniff
    SECURE_CONTENT_TYPE_NOSNIFF = env.bool(
        "DJANGO_SECURE_CONTENT_TYPE_NOSNIFF", default=True
    )

# EMAIL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/3.2/ref/settings/#email-backend
DEFAULT_FROM_EMAIL = app_config['email'].get(
    "DJANGO_DEFAULT_FROM_EMAIL", "Simple Django <admin@example.com>"
)

SERVER_EMAIL = app_config['email'].get("DJANGO_SERVER_EMAIL", DEFAULT_FROM_EMAIL)

EMAIL_SUBJECT_PREFIX = app_config['email'].get(
    "DJANGO_EMAIL_SUBJECT_PREFIX", "[Simple Django]"
)

if DEBUG:
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
    EMAIL_HOST = app_config['email'].get("DJANGO_SMTP_HOST", "localhost")
    EMAIL_PORT = app_config['email'].getint("DJANGO_SMTP_PORT", 1025)
else:
    EMAIL_BACKEND = "anymail.backends.amazon_ses.EmailBackend"
    ANYMAIL = {
        "AMAZON_SES_CLIENT_PARAMS": {
            "aws_access_key_id": app_config['email'].get("DJANGO_AWS_ACCESS_KEY_ID"),
            "aws_secret_access_key": app_config['email'].get("DJANGO_AWS_SECRET_ACCESS_KEY"),
            "region_name": app_config['email'].get("DJANGO_AWS_REGION_NAME"),
            "config": {
                "connect_timeout": 30,
                "read_timeout": 30,
            },
        },
    }

# https://docs.djangoproject.com/en/3.2/ref/settings/#email-timeout
EMAIL_TIMEOUT = 5

# ADMIN
# ------------------------------------------------------------------------------
# Django Admin URL.
ADMIN_URL = app_config['core'].get("DJANGO_ADMIN_URL")

# https://docs.djangoproject.com/en/3.2/ref/settings/#admins
ADMINS = [("""Josh Michael Karamuth""", "admin@example.com")]
# https://docs.djangoproject.com/en/3.2/ref/settings/#managers
MANAGERS = ADMINS

# LOGGING
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/3.2/ref/settings/#logging
# See https://docs.djangoproject.com/en/3.2/topics/logging for
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
# https://docs.djangoproject.com/en/3.2/ref/settings/#caches

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": app_config['core'].get("DJANGO_REDIS_CACHE_URL"),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            # Mimicing memcache behavior.
            # http://niwinz.github.io/django-redis/latest/#_memcached_exceptions_behavior
            "IGNORE_EXCEPTIONS": True,
        },
    }
}

# Captcha

HCAPTCHA_SECRET_KEY = app_config['captcha'].get("HCAPTCHA_SECRET_KEY")

HCAPTCHA_SITE_KEY = app_config['captcha'].get("HCAPTCHA_SITE_KEY")

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
    'name': 'simple_django',
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

THUMBNAIL_REDIS_HOST = app_config['core'].get("SORL_REDIS_HOST")

THUMBNAIL_PRESERVE_FORMAT = True
