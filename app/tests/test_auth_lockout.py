import pytest
from axes.helpers import get_cache
from django.urls import reverse

pytestmark = pytest.mark.django_db


@pytest.fixture(autouse=True)
def clear_axes_cache():
    get_cache().clear()


@pytest.fixture
def user(django_user_model):
    return django_user_model.objects.create_user(username="user", password="pass")


def login(client, attempts):
    for _ in range(attempts):
        response = client.post(
            reverse("account_login"), {"login": "user", "password": "bad"}
        )
    return response


def test_too_few_attemps(client, user, settings, caplog):
    settings.AXES_ENABLED = True
    response = login(client, settings.AXES_FAILURE_LIMIT - 1)
    assert response.status_code == 200
    assert "Locking out" not in caplog.text
