SECRET_KEY = "dump-secret-key"

INSTALLED_APPS = (
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.admin",
    "django_library",
)


DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3"}}

LIBRARY_ARCHIMED_BASE_URL = "https://syracuse.archimed.fr/EXPLOITATION/logon.aspx"
LIBRARY_QUERY_STRING_TRIGGER = "library_sso_id"
