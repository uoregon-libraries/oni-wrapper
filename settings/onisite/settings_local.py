import os
import urllib

###
# Custom stuff that doesn't exist in the core settings example
###

# Where the static pages live for the staticpages plugin
STATIC_PAGES_PATH = "/opt/openoni/themes/oregon/pages"

# Time zone - we don't go with the UTC default
TIME_ZONE = 'America/Los_Angeles'

###
# Settings example, customized for us
###

# For initial customization, search and update values beginning with 'YOUR_'

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

################################################################
# ENVIRONMENT SETTINGS
################################################################
# BASE_URL can NOT include any path elements!
BASE_URL = os.getenv("ONI_BASE_URL")
url = urllib.parse.urlparse(BASE_URL)
ALLOWED_HOSTS = [url.netloc]

if url.scheme == 'https':
    """
    Enable HSTS by setting SECURE_HSTS_SECONDS > 0.
    Test with a low value (e.g. 300)
    before setting a high value (e.g. 15552000) for long-term use
    """
    SECURE_HSTS_SECONDS = int(os.getenv('ONI_HSTS_SECONDS', 300))

DATABASES = {
    'default': {
        'ENGINE':   'django.db.backends.mysql',
        'HOST':     os.getenv('ONI_DB_HOST', 'rdbms'),
        'PORT':     os.getenv('ONI_DB_PORT', 3306),
        'NAME':     os.getenv('ONI_DB_NAME', 'openoni'),
        'USER':     os.getenv('ONI_DB_USER', 'openoni'),
        'PASSWORD': os.getenv('ONI_DB_PASSWORD', 'openoni'),
        'OPTIONS': { 'init_command': "SET sql_mode='STRICT_TRANS_TABLES'" },
    }
}

# DEBUG defaults to false, and is only true if ONI_DEBUG is set to "1" to avoid
# any kind of accident putting production into debug mode
DEBUG = False
if os.getenv("ONI_DEBUG") == "1":
    logging.getLogger(__name__).info("Enabling debug settings")
    DEBUG = True


# IIIF server public URL endpoint
IIIF_URL = os.getenv('ONI_IIIF_URL', 'http://localhost/images/iiif')

SECRET_KEY = os.getenv("ONI_SECRET_KEY")

SOLR_BASE_URL = os.getenv('ONI_SOLR_URL', 'http://solr:8983')

# Absolute path on disk to the data directory
STORAGE = os.getenv('ONI_STORAGE_PATH', '/opt/openoni/data/')

"""
Django logging outputs in Apache logs by default.
Log to file when Apache logs don't provide info or tracebacks.
Ensure file is writeable by Apache user with SELinux writeable context:
    chcon -t httpd_sys_rw_content_t /path/to/debug.log
Start with INFO level; change to DEBUG if insufficient
"""
if os.getenv('ONI_LOG_TO_FILE', 0) == '1':
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'handlers': {
            'file': {
                'level': 'INFO',
                'class': 'logging.FileHandler',
                'filename': os.path.join(BASE_DIR, 'log', 'debug.log'),
            },
        },
        'loggers': {
            'django': {
                'handlers': ['file'],
                'level': 'INFO',
                'propagate': True,
            },
        },
    }


################################################################
# DJANGO SETTINGS
################################################################
# Keep database connections open until idle for this many seconds
CONN_MAX_AGE = 30

# List of configuration classes / app packages in order of priority high to low.
# The first item in the list has final say when collisions occur.
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

"""
'From' address on general emails sent by Django:
If sending email from different server, replace `@' + url.netloc` with host.
Space at the end of EMAIL_SUBJECT_PREFIX intentional
to separate subject from prefix.
"""
DEFAULT_FROM_EMAIL = 'YOUR_PROJECT_NAME_ABBREVIATION-no-reply@' + url.netloc
EMAIL_SUBJECT_PREFIX = '[YOUR_PROJECT_NAME_ABBREVIATION] '


################################################################
# OPEN-ONI SETTINGS
################################################################
"""
SITE_TITLE that will be used for display purposes throughout app.
PROJECT_NAME may be the same as SITE_TITLE but can be used for longer
descriptions that will only show up occasionally.
For example: 'Open ONI' for most headers, 'Open Online Newspapers Initiative'
for introduction / about / further information / etc
"""
SITE_TITLE = "Historic Oregon Newspapers"
PROJECT_NAME = "Oregon Digital Newspapers Initiative"

# Make sure it's really obvious when the site is in debug mode
if Debug:
    SITE_TITLE = "** DEBUG ** | " + SITE_TITLE

# Relative path from core and theme apps to subdirectory with essay templates.
# For example: 'essays' will find files in themes/*/templates/essays
ESSAY_TEMPLATES = 'essays'

"""
Use below only if LoC is down and MARC requests fail.
We've mirrored a *lot* of MARC records on GitHub for use with
"""
#MARC_RETRIEVAL_URLFORMAT = 'https://raw.githubusercontent.com/open-oni/marc-mirror/master/marc/%s/marc.xml'
"""
To serve locally, clone open-oni/marc-mirror repository
to static/compiled/marc and use setting below.
MARC files may be updated periodically with getlc.go Go script.
"""
#MARC_RETRIEVAL_URLFORMAT = BASE_URL + '/static/marc/%s/marc.xml'

"""
Number of processes in system run queue averaged over last minute beyond which
Open ONI will return a 'Server Too Busy' response. If unsure, leave at default.
Requires core.middleware.TooBusyMiddleware in MIDDLEWARE.
"""
TOO_BUSY_LOAD_AVERAGE = 64


if DEBUG:
    """
    DEBUG mode (not production) disables Django cache, sends emails to console,
    and adds middleware that disables all client-side caching.
    SQL logging is optional in DEBUG mode with env var ONI_LOG_SQL.
    Note that SQL logging will override logging to a file with ONI_LOG_TO_FILE.
    """
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.dummy.DummyCache'
        }
    }

    # Output emails to console
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

    # Suggested order: https://docs.djangoproject.com/en/2.2/ref/middleware/#middleware-ordering
    MIDDLEWARE = (
        'django.middleware.security.SecurityMiddleware',
        'core.middleware.DisableClientSideCachingMiddleware',         # Open ONI
        'core.middleware.TooBusyMiddleware',                          # Open ONI
        'django.middleware.http.ConditionalGetMiddleware',            # Open ONI
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    )

    if os.getenv('ONI_LOG_SQL', 0) == '1':
        LOGGING = {
            'version': 1,
            'disable_existing_loggers': False,
            'filters': {
                'require_debug_true': {
                    '()': 'django.utils.log.RequireDebugTrue',
                }
            },
            'handlers': {
                'console': {
                    'level': 'DEBUG',
                    'filters': ['require_debug_true'],
                    'class': 'logging.StreamHandler',
                }
            },
            'loggers': {
                'django.db.backends': {
                    'level': 'DEBUG',
                    'handlers': ['console'],
                }
            }
        }


else:
    """
    Production mode (DEBUG is off) uses filesystem cache, adds middleware for
    optional error reporting emails, and fingerprints static files
    """
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
            'LOCATION': '/var/tmp/django_cache',
            'TIMEOUT': 60 * 60 * 24 * 7 * 8  # Eight weeks
        }
    }

    # Suggested order: https://docs.djangoproject.com/en/2.2/ref/middleware/#middleware-ordering
    MIDDLEWARE = (
        'django.middleware.security.SecurityMiddleware',
        'core.middleware.TooBusyMiddleware',                          # Open ONI
        'django.middleware.http.ConditionalGetMiddleware',            # Open ONI
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    )

    # Fingerprint compiled static files with MD5 hash of contents
    # Store hashes in STATIC_ROOT directory as staticfiles.json
    STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'

