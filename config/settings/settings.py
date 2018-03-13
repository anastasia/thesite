import dj_database_url
from config.settings.settings_base import *

try:
    if os.environ['DJANGO_ENVIRONMENT'] == 'heroku':
        # Allow all host hosts/domain names for this site
        ALLOWED_HOSTS = ['*']

        # Parse database configuration from $DATABASE_URL
        DATABASES = {'default': dj_database_url.config()}
except KeyError:
    pass