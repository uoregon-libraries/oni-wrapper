import os
import urllib
from .settings_base import *

###
# Custom stuff that doesn't exist in the core settings example
###

# Where the static pages live for the staticpages plugin
STATIC_PAGES_PATH = "/opt/openoni/themes/oregon/pages"

# Time zone - we don't go with the UTC default
TIME_ZONE = 'America/Los_Angeles'

# Make sure this defaults to precisely what we need in staging and production,
# not whatever BASE_DIR might point to
STORAGE = os.getenv('ONI_STORAGE_PATH', '/opt/openoni/data/')

# We don't allow SECRET_KEY to have a default
SECRET_KEY = os.getenv("ONI_SECRET_KEY")

###
# Settings example, customized for us
###

# Copy to settings_local.py, update YOUR_ values, and follow our documentation:
# https://github.com/open-oni/open-oni/blob/dev/docs/customization/configuration.md


################################################################
# DJANGO SETTINGS
################################################################
# BASE_URL can NOT include any path elements!
BASE_URL = os.getenv('ONI_BASE_URL')
url = urllib.parse.urlparse(BASE_URL)
ALLOWED_HOSTS = ["*"]

if url.scheme == 'https':
    """
    Enable HSTS by setting ONI_HSTS_SECONDS > 0.
    Test with a low value (e.g. 300)
    before setting a high value (e.g. 31536000) for long-term use
    """
    SECURE_HSTS_SECONDS = int(os.getenv('ONI_HSTS_SECONDS', 300))

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
    'onisite.plugins.map',
    'onisite.plugins.calendar',
    'core',

    # These should come last so static pages can't accidentally override theme/core pages
    'onisite.plugins.staticpages',
)

"""
'From' address on general emails sent by Django:
If sending email from different server, replace `@' + url.hostname` with host.
Space at the end of EMAIL_SUBJECT_PREFIX intentional
to separate subject from prefix.
"""
DEFAULT_FROM_EMAIL = 'YOUR_PROJECT_NAME_ABBREVIATION-no-reply@' + url.hostname
EMAIL_SUBJECT_PREFIX = '[YOUR_PROJECT_NAME_ABBREVIATION] '


################################################################
# OPEN-ONI SETTINGS
################################################################
# IIIF server public URL endpoint
# Docker compose Apache config defines proxy as 'BASE_URL + /images/iiif'
IIIF_URL = os.getenv('ONI_IIIF_URL', BASE_URL + '/images/iiif')

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
if DEBUG:
    SITE_TITLE = "** DEBUG ** | " + SITE_TITLE

"""
Use below only if LoC is down and MARC requests fail.
We've mirrored a *lot* of MARC records on GitHub for use with
"""
#MARC_RETRIEVAL_URLFORMAT = 'https://raw.githubusercontent.com/open-oni/marc-mirror/main/marc/%s/marc.xml'

# This is used on our staging server so we only have to ingest titles once
#MARC_RETRIEVAL_URLFORMAT = 'https://oregonnews.uoregon.edu/lccn/%s/marc.xml'

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
