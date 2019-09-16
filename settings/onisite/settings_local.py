import os
import logging
import urllib

###
# Site customizations: these settings are what make oregonnews
###

SITE_TITLE = "Historic Oregon Newspapers"
PROJECT_NAME = "Oregon Digital Newspapers Initiative"
STATIC_PAGES_PATH = "/opt/openoni/themes/oregon/pages"
TIME_ZONE = 'America/Los_Angeles'

INSTALLED_APPS = (
    'django.contrib.humanize',
    'django.contrib.staticfiles',

    # Make sure oregon theme files override plugin and core pages
    'themes.oregon',

    'onisite.plugins.title_locations',
    'onisite.plugins.featured_content',
    'onisite.plugins.map',
    'onisite.plugins.calendar',
    'core',

    # These should come last so static pages can't accidentally override theme/core pages
    'onisite.plugins.staticpages',
)

###
# Site-specific settings we are keeping as-is from ONI defaults
###

LOG_LOCATION = '/opt/openoni/log/'
CONN_MAX_AGE = 30

# Absolute path on disk to the data directory
STORAGE = os.getenv('ONI_STORAGE_PATH', '/opt/openoni/data/')

# Various storage subdirectories
BATCH_STORAGE = os.path.join(STORAGE, 'batches')
COORD_STORAGE = os.path.join(STORAGE, 'word_coordinates')
OCR_DUMP_STORAGE = os.path.join(STORAGE, 'ocr')
TEMP_TEST_DATA = os.path.join(STORAGE, 'temp_test_data')

# URL path to the data directory
STORAGE_URL = '/data/'

# Displays newspaper titles with medium ("volume", "microform") when available
TITLE_DISPLAY_MEDIUM = False

###
# ONI environment-specific settings
###

# 1. Stuff that could be in openoni.ini, but which we now pull from the
# environment to ease cloudiness

BASE_URL = os.getenv("ONI_BASE_URL")

RESIZE_SERVER = BASE_URL + '/images/resize'
TILE_SERVER = BASE_URL + '/images/iiif'

DATABASES = {
    'default': {
        'ENGINE':   'django.db.backends.mysql',
        'HOST':     os.getenv('ONI_DB_HOST', 'rdbms'),
        'PORT':     os.getenv('ONI_DB_PORT', 3306),
        'NAME':     os.getenv('ONI_DB_NAME', 'openoni'),
        'USER':     os.getenv('ONI_DB_USER', 'openoni'),
        'PASSWORD': os.getenv('ONI_DB_PASSWORD', 'openoni'),
    }
}

SOLR = os.getenv('ONI_SOLR_URL', 'http://solr:8983/solr/openoni')
SECRET_KEY = os.getenv("ONI_SECRET_KEY")

# DEBUG defaults to false, and is only true if ONI_DEBUG is set to "1" to avoid
# any kind of accident putting production into debug mode
DEBUG = False
if os.getenv("ONI_DEBUG") == "1":
    logging.getLogger(__name__).info("Enabling debug settings")
    DEBUG = True

# 2. Stuff which hinges on other environmental settings
RESIZE_SERVER = BASE_URL + "/images/resize"
TILE_SERVER = BASE_URL + "/images/iiif"

IS_PRODUCTION = not DEBUG

# If we're in an https environment, let's make sure we do it right
url = urllib.parse.urlparse(BASE_URL)
if url.scheme == "https":
    logging.getLogger(__name__).info("Enabling HTTPS settings")
    # HTTPS Settings
    CSRF_COOKIE_SECURE = True
    SESSION_COOKIE_SECURE = True

    # Enable HSTS by setting SECURE_HSTS_SECONDS > 0
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True

    # Test with a low value (e.g. 300)
    # before setting a high value (e.g. 15552000) for long-term use
    SECURE_HSTS_SECONDS = 300
    SECURE_SSL_REDIRECT = True

ALLOWED_HOSTS = [url.netloc]

###
# Core ONI settings we want to preserve unless something major changes - don't
# change anything below unless absolutely necessary
###

# Number of processes in system run queue averaged over last minute beyond which
# Open ONI will return a 'Server Too Busy' response; If unsure, leave at default
# Requires core.middleware.TooBusyMiddleware in MIDDLEWARE_CLASSES
TOO_BUSY_LOAD_AVERAGE = 64

# Suggested order: https://docs.djangoproject.com/en/1.10/ref/middleware/#middleware-ordering
MIDDLEWARE = (
    'django.middleware.security.SecurityMiddleware',
    'core.middleware.DisableClientSideCachingMiddleware',             # Open ONI
    'core.middleware.TooBusyMiddleware',                              # Open ONI
    'django.middleware.http.ConditionalGetMiddleware',                # Open ONI
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': '/var/tmp/django_cache',
        'TIMEOUT': 60 * 60 * 24 * 7 * 8
    }
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
        },
    },
}

# Fingerprint compiled static files with MD5 hash of contents
# Store hashes in STATIC_ROOT directory as staticfiles.json
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'

# Relative path from core and theme apps to subdirectory where essay templates are stored
# example: "essays" would find files in themes/default/templates/essays
ESSAY_TEMPLATES = "essays"
