import pytest
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.utils.crypto import get_random_string


@pytest.mark.parametrize("password", ["qwerty", "1qaz2wsx3edc", "password1"])
def test_invalid_passwords(password):
    with pytest.raises(ValidationError):
        validate_password(password)


def test_password_too_short(settings):
    password = get_random_string(length=settings.AUTH_PASSWORD_MIN_LENGTH - 1)
    with pytest.raises(ValidationError):
        validate_password(password)


def test_valid_password(settings):
    password = get_random_string(length=settings.AUTH_PASSWORD_MIN_LENGTH)
    validate_password(password)
    