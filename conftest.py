import factory
import pytest
from django.core.management import call_command
from pytest_django.lazy_django import skip_if_no_django


@pytest.fixture(scope='session')
def django_db_setup(django_db_setup, django_db_blocker):
    """Fixture for DB setup."""
    with django_db_blocker.unblock():
        call_command('loadmetadata')
        call_command('load_omis_metadata')


@pytest.fixture(scope='session', autouse=True)
def set_faker_locale():
    """Sets the default locale for Faker."""
    with factory.Faker.override_default_locale('en_GB'):
        yield


@pytest.fixture
def api_request_factory():
    """Django REST framework ApiRequestFactory instance."""
    skip_if_no_django()

    from rest_framework.test import APIRequestFactory

    return APIRequestFactory()


@pytest.fixture
def api_client():
    """Django REST framework ApiClient instance."""
    skip_if_no_django()

    from rest_framework.test import APIClient
    return APIClient()
