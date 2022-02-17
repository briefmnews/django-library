import logging

from django.conf import settings

from cas import CASClient

logger = logging.getLogger(__name__)

LIBRARY_INACTIVE_USER_REDIRECT = getattr(
    settings, "LIBRARY_INACTIVE_USER_REDIRECT", "/"
)
LIBRARY_GMINVENT_BASE_URL = getattr(settings, "LIBRARY_GMINVENT_BASE_URL", "")
LIBRARY_C3RB_BASE_URL = getattr(settings, "LIBRARY_C3RB_BASE_URL", "")
LIBRARY_ARCHIMED_BASE_URL = getattr(settings, "LIBRARY_ARCHIMED_BASE_URL", "")
LIBRARY_QUERY_STRING_TRIGGER = getattr(
    settings, "LIBRARY_QUERY_STRING_TRIGGER", "library_sso_id"
)

BASE_URLS = {
    "GMINVENT": LIBRARY_GMINVENT_BASE_URL,
    "C3RB": LIBRARY_C3RB_BASE_URL,
    "ARCHIMED": LIBRARY_ARCHIMED_BASE_URL,
}


def get_redirect_url(request, path=None):
    """Get redirect url for cas"""

    scheme = request.scheme
    host = request.get_host()
    if path:
        url = "{}://{}{}".format(scheme, host, path)
    else:
        url = "{}://{}".format(scheme, host)

    return url


def get_cas_client(request):
    """Create a CAS client"""

    library_sso_id = request.session.get("library_sso_id")
    connector = request.session.get("connector")
    logger.info(f"connector: {connector}; library_sso_id: {library_sso_id}")
    cas_version = 2

    server_url = BASE_URLS.get(connector, LIBRARY_GMINVENT_BASE_URL)

    if connector == "ARCHIMED":
        server_url.format(library_sso_id)

    next_page = request.get_full_path()
    # Strip ticket query string to avoid error in validate ticket
    next_page = next_page.split("&ticket")[0]

    service_url = get_redirect_url(request, next_page)

    return CASClient(
        version=cas_version, server_url=server_url, service_url=service_url
    )
