import pytest
from pydantic import ValidationError
from app.shemas import URLCreate


def test_valid_https_url_accepted():
    data = URLCreate(original_url="https://example.com/path?q=1")
    assert "example.com" in str(data.original_url)


def test_valid_http_url_accepted():
    data = URLCreate(original_url="http://example.com")
    assert data.original_url is not None


def test_plain_string_without_scheme_rejected():
    with pytest.raises(ValidationError):
        URLCreate(original_url="example.com")


def test_totally_invalid_string_rejected():
    with pytest.raises(ValidationError):
        URLCreate(original_url="not-a-url-at-all")


def test_missing_url_field_rejected():
    with pytest.raises(ValidationError):
        URLCreate()


def test_empty_string_rejected():
    with pytest.raises(ValidationError):
        URLCreate(original_url="")
