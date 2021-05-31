import logging

from django.http import HttpResponseRedirect

from django.conf import settings
from django.contrib.auth import login

from xml.etree import ElementTree
from xml.etree.ElementTree import ParseError

from .backends import CASBackend
from .utils import get_cas_client
from .models import Library

logger = logging.getLogger(__name__)

LIBRARY_INACTIVE_USER_REDIRECT = getattr(
    settings, "LIBRARY_INACTIVE_USER_REDIRECT", "/"
)
LIBRARY_QUERY_STRING_TRIGGER = getattr(
    settings, "LIBRARY_QUERY_STRING_TRIGGER", "library_sso_id"
)


class CASMiddleware:
    """
    Middleware that allows CAS authentication with different kind of Library
    (GMInvent, C3RB and Archimed)
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        library_sso_id = request.GET.get(LIBRARY_QUERY_STRING_TRIGGER)
        cas_ticket = request.GET.get("ticket", "")
        redirect = request.GET.get("redirect", "")

        if cas_ticket and request.session.get("is_library"):
            library_sso_id = self.validate_ticket(request, cas_ticket)

            user = CASBackend.authenticate(request, sso_id=library_sso_id)
            if user:
                login(
                    request, user, backend="django_library.backends.LibraryCASBackend"
                )
                request.session["library_user"] = True

                if redirect:
                    return HttpResponseRedirect(redirect)
            else:
                return HttpResponseRedirect(LIBRARY_INACTIVE_USER_REDIRECT)

        elif library_sso_id:
            try:
                connector = Library.objects.get(sso_id=library_sso_id).connector
            except Library.DoesNotExist:
                return HttpResponseRedirect(LIBRARY_INACTIVE_USER_REDIRECT)

            request.session["library_sso_id"] = library_sso_id
            request.session["connector"] = connector
            request.session["is_library"] = True

            url = self.get_cas_login_url(request)
            return HttpResponseRedirect(url)

        response = self.get_response(request)

        return response

    @staticmethod
    def get_cas_login_url(request):
        """Returns the CAS login url"""

        client = get_cas_client(request)

        return client.get_login_url()

    @staticmethod
    def validate_ticket(request, cas_ticket):
        """
        Validate the CAS ticket. Ticket lifetime is around 5 seconds.
        Returns the sso_id if the ticket is validated None otherwise.
        """

        client = get_cas_client(request)
        response = client.get_verification_response(cas_ticket)

        logger.info(response)

        try:
            tree = ElementTree.fromstring(response)
            ns = {"cas": "http://www.yale.edu/tp/cas"}
            assert tree.find("cas:authenticationSuccess", ns)

            return request.session.get("library_sso_id", "")

        except (AttributeError, ParseError):
            return None
