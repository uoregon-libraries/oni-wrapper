SITE_TITLE = "Historic Oregon Newspapers"
PROJECT_NAME = "Oregon Digital Newspapers Initiative"

DEBUG = True

BASE_URL="http://example.com"
#LOG_LOCATION = "/tmp"
MARC_RETRIEVAL_URLFORMAT = "https://raw.githubusercontent.com/open-oni/marc-mirror/master/marc/%s/marc.xml"

INSTALLED_APPS = (
    'django.contrib.humanize',
    'django.contrib.staticfiles',

    # Make sure oregon theme files override plugin and core pages
    'themes.oregon',

    'onisite.plugins.featured_content',
    'onisite.plugins.map',
    'core',

    # These should come last so static pages can't accidentally override theme/core pages
    'onisite.plugins.staticpages',
)

STATIC_PAGES_PATH="/opt/openoni/themes/oregon/staticpages"
