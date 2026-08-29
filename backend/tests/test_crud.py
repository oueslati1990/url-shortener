import pytest
from unittest.mock import patch
from app import crud


async def test_create_url_returns_persisted_object(db):
    url = await crud.create_url(db, "https://example.com")
    assert url.id is not None
    assert url.original_url == "https://example.com"
    assert len(url.short_code) == 7
    assert url.click_count == 0


async def test_create_url_generates_unique_codes(db):
    url1 = await crud.create_url(db, "https://first.com")
    url2 = await crud.create_url(db, "https://second.com")
    assert url1.short_code != url2.short_code


async def test_get_by_code_returns_none_for_unknown(db):
    result = await crud.get_by_code(db, "xxxxxxx")
    assert result is None


async def test_get_by_code_returns_matching_url(db):
    url = await crud.create_url(db, "https://example.com")
    found = await crud.get_by_code(db, url.short_code)
    assert found is not None
    assert found.id == url.id
    assert found.original_url == url.original_url


async def test_increment_clicks_increases_count(db):
    url = await crud.create_url(db, "https://example.com")
    assert url.click_count == 0
    await crud.increment_clicks(db, url)
    assert url.click_count == 1


async def test_increment_clicks_is_cumulative(db):
    url = await crud.create_url(db, "https://example.com")
    await crud.increment_clicks(db, url)
    await crud.increment_clicks(db, url)
    assert url.click_count == 2


async def test_list_urls_empty_on_fresh_db(db):
    urls = await crud.list_urls(db)
    assert urls == []


async def test_list_urls_returns_newest_first(db):
    url1 = await crud.create_url(db, "https://first.com")
    url2 = await crud.create_url(db, "https://second.com")
    urls = await crud.list_urls(db)
    # most recently created comes first
    assert urls[0].id == url2.id
    assert urls[1].id == url1.id


async def test_create_url_raises_after_exhausting_retries(db):
    # Force _generate_code to always return the same value.
    # First call succeeds; the rest of calls fail and exhaust the 5-attempt limit.
    with patch("app.crud._generate_code", return_value="AAAAAAA"):
        await crud.create_url(db, "https://first.com")  # short_code = AAAAAAA
        with pytest.raises(RuntimeError, match="unique"):
            await crud.create_url(db, "https://second.com")
