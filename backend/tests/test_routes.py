async def test_shorten_url_returns_201(client):
    response = await client.post(
        "/api/urls/", json={"original_url": "http://example.com"}
    )
    assert response.status_code == 201


async def test_shorten_url_response_has_expected_fields(client):
    response = await client.post(
        "/api/urls/", json={"original_url": "http://example.com"}
    )
    data = response.json()
    assert "id" in data
    assert "short_code" in data
    assert "short_url" in data
    assert data["original_url"] == "http://example.com"
    assert data["click_count"] == 0


async def test_shorten_url_short_url_includes_short_code(client):
    response = await client.post(
        "/api/urls/", json={"original_url": "http://example.com"}
    )
    data = response.json()
    assert data["short_code"] in data["short_url"]


async def test_shorten_url_rejects_invalid_url(client):
    response = await client.post("/api/urls/", json={"original_url": "not-url"})
    assert response.status_code == 422


async def test_list_urls_empty_initially(client):
    response = await client.get("/api/urls/")
    data = response.json()
    assert data == []
    assert response.status_code == 200


async def test_list_urls_contains_created_entry(client):
    await client.post("/api/urls/", json={"original_url": "http://example.com"})
    response = await client.get("/api/urls/")
    data = response.json()
    assert len(data) == 1
    assert response.status_code == 200


async def test_redirect_returns_302(client):
    post = await client.post("/api/urls/", json={"original_url": "http://example.com"})
    code = post.json()["short_code"]
    # Add follow_redirects = False, or else it will call immediately GET http://example.com
    # and return the final 200 response
    response = await client.get(f"/{code}", follow_redirects=False)
    assert response.status_code == 302


async def test_redirect_location_points_to_original(client):
    post = await client.post("/api/urls/", json={"original_url": "http://example.com"})
    code = post.json()["short_code"]
    response = await client.get(f"/{code}", follow_redirects=False)
    assert "http://example.com" in response.headers["location"]


async def test_redirect_unknown_code_returns_404(client):
    response = await client.get("/xxxxxxx", follow_redirects=False)
    assert response.status_code == 404
