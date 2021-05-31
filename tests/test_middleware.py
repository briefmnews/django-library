import pytest

from django.conf import settings

from django_library.middleware import CASMiddleware

pytestmark = pytest.mark.django_db()

LIBRARY_QUERY_STRING_TRIGGER = settings.LIBRARY_QUERY_STRING_TRIGGER


class TestCASMiddleware:
    @staticmethod
    def test_init():
        """Testing the __init__ method"""
        # WHEN
        cas_middleware = CASMiddleware("dump_response")

        # THEN
        assert cas_middleware.get_response == "dump_response"

    def test_no_sso_id_no_ticket(self, request_builder):
        """Testing the middleware if not a connection to CAS Library"""
        # GIVEN
        cas_middleware = CASMiddleware(request_builder.get)

        # WHEN
        response = cas_middleware(request_builder.get())

        # THEN
        assert cas_middleware.get_response().path == "/"
        assert LIBRARY_QUERY_STRING_TRIGGER not in response.GET
        assert "ticket" not in response.GET

    def test_when_library_sso_id(self, user, request_builder):
        """Testing the __call__ method with uai_number in url"""
        # GIVEN
        query_params = "/?{}={}".format(
            LIBRARY_QUERY_STRING_TRIGGER, user.library.sso_id
        )
        request = request_builder.get(query_params)
        cas_middleware = CASMiddleware(request)

        # WHEN
        response = cas_middleware(request)

        # THEN
        assert "login?service" in response.url

    @pytest.mark.usefixtures("user")
    def test_when_cas_ticket_valid(
        self, mock_validate_valid_ticket, user, request_builder
    ):
        """
        Testing the __call__ method with valid cas_ticket in url and user
        has access (is_active is True)
        """
        # GIVEN
        cas_ticket = "this-is-a-ticket"
        query_params = "/?ticket={}".format(cas_ticket)
        request = request_builder.get(query_params)
        request.session["is_library"] = True
        cas_middleware = CASMiddleware(request_builder.get)

        # WHEN
        cas_middleware(request)

        # THEN
        assert mock_validate_valid_ticket.call_count == 1

    def test_when_cas_ticket_invalid(
        self, mock_validate_invalid_ticket, request_builder
    ):
        """
        Testing the __call__ method with invalid cas_ticket in url and user
        has access (is_active is True)
        """
        # GIVEN
        cas_ticket = "this-is-a-ticket"
        query_params = "/?ticket={}".format(cas_ticket)
        request = request_builder.get(query_params)
        request.session["is_library"] = True
        cas_middleware = CASMiddleware(request_builder.get)

        # WHEN
        response = cas_middleware(request)

        # THEN
        assert response.status_code == 302
        assert mock_validate_invalid_ticket.call_count == 1

    def test_validate_ticket(self, mock_verification_response, request_builder):
        # GIVEN
        request = request_builder.get()
        request.session["is_library"] = True

        # WHEN
        mock_verification_response.get()
        cas_middleware = CASMiddleware(request_builder.get)
        cas_middleware.validate_ticket(request, "dummy-ticket")

        # THEN
        mock_verification_response.assert_called_once()
