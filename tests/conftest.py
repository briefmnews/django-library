import datetime
import pytest

from django.contrib.auth.models import AnonymousUser
from django.contrib.sessions.middleware import SessionMiddleware
from django.test import RequestFactory

from .factories import UserFactory


@pytest.fixture
def user():
    return UserFactory()


@pytest.fixture
def user_without_library():
    user = UserFactory()
    user.library.delete()
    return user


@pytest.fixture
def mock_validate_valid_ticket(mocker, user):
    return mocker.patch(
        "django_library.middleware.CASMiddleware.validate_ticket",
        return_value="OK",
    )


@pytest.fixture
def mock_validate_invalid_ticket(mocker):
    return mocker.patch(
        "django_library.middleware.CASMiddleware.validate_ticket", return_value=""
    )


@pytest.fixture
def request_builder():
    """Create a request object"""
    return RequestBuilder()


class RequestBuilder(object):
    @staticmethod
    def get(path="?"):
        rf = RequestFactory()
        request = rf.get(path)
        request.user = AnonymousUser()

        middleware = SessionMiddleware("dummy")
        middleware.process_request(request)
        request.session.save()

        return request


@pytest.fixture
def mock_verification_response(mocker):
    file = "tests/fixtures/valid_ticket.xml"

    with open(file, "r") as xml_response:
        return mocker.patch(
            "cas.CASClientV2.get_verification_response",
            return_value=xml_response.read(),
        )


@pytest.fixture
def response_from_gar():
    """Create a response object from GAR ent"""
    return ResponseBuilder


class ResponseBuilder:
    status_code = None
    text = None

    def __init__(self, status_code, message):
        self.status_code = status_code
        self.text = message
