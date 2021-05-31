import datetime
import factory

from django.contrib.auth import get_user_model

from django_library.models import Library


class LibraryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Library

    name = factory.Sequence(lambda n: "Lycée {0}".format(n))
    connector = factory.Sequence(lambda n: "connector_{0}".format(n))
    ends_at = datetime.datetime.today()
    sso_id = factory.Sequence(lambda n: "prefix_{0}".format(n))


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = get_user_model()

    email = factory.Sequence(lambda n: "noel{0}@flantier.com".format(n))
    is_active = True
    library = factory.RelatedFactory(LibraryFactory, "user")
