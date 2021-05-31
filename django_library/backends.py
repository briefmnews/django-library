from django.contrib.auth import get_user_model

User = get_user_model()


class CASBackend:
    """
    CAS authentication with unique sso_id
    """

    @staticmethod
    def authenticate(request, sso_id):
        user = User.objects.filter(library__sso_id=sso_id).last()
        return user

    @staticmethod
    def get_user(user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
