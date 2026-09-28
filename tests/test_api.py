def test_register_and_login(client):
    # Register user
    reg_res = client.post("/user/", json={
        "name": "Alice",
        "email": "alice@example.com",
        "password": "password123"
    })
    assert reg_res.status_code == 201
    assert reg_res.json()["email"] == "alice@example.com"
    assert reg_res.json()["name"] == "Alice"

    # Login user
    login_res = client.post("/login", data={
        "username": "alice@example.com",
        "password": "password123"
    })
    assert login_res.status_code == 200
    token_data = login_res.json()
    assert "access_token" in token_data
    assert token_data["token_type"] == "bearer"


def test_duplicate_email(client):
    # Register first user
    client.post("/user/", json={
        "name": "Alice",
        "email": "alice@example.com",
        "password": "password123"
    })

    # Try duplicate registration
    dup_res = client.post("/user/", json={
        "name": "Alice Duplicate",
        "email": "alice@example.com",
        "password": "password456"
    })
    assert dup_res.status_code == 409
    assert dup_res.json()["detail"] == "A user with this email already exists"


def test_invalid_login_credentials(client):
    # Register user
    client.post("/user/", json={
        "name": "Alice",
        "email": "alice@example.com",
        "password": "password123"
    })

    # Wrong password
    res_wrong_pw = client.post("/login", data={
        "username": "alice@example.com",
        "password": "wrongpassword"
    })

    # Unknown user
    res_unknown_user = client.post("/login", data={
        "username": "unknown@example.com",
        "password": "password123"
    })

    assert res_wrong_pw.status_code == 401
    assert res_unknown_user.status_code == 401

    assert res_wrong_pw.json() == {"detail": "Invalid credentials"}
    assert res_unknown_user.json() == {"detail": "Invalid credentials"}

    assert res_wrong_pw.headers.get("www-authenticate") == "Bearer"
    assert res_unknown_user.headers.get("www-authenticate") == "Bearer"


def test_unauthenticated_blog_access(client):
    assert client.get("/blog/").status_code == 401
    assert client.post("/blog/", json={"title": "T", "body": "B"}).status_code == 401
    assert client.get("/blog/1").status_code == 401
    assert client.put("/blog/1", json={"title": "T", "body": "B"}).status_code == 401
    assert client.delete("/blog/1").status_code == 401


def test_create_and_read_blog(client):
    # Register and login
    client.post("/user/", json={"name": "Alice", "email": "alice@example.com", "password": "password123"})
    login_res = client.post("/login", data={"username": "alice@example.com", "password": "password123"})
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Create blog
    create_res = client.post("/blog/", json={"title": "My First Post", "body": "Hello World!"}, headers=headers)
    assert create_res.status_code == 201
    blog_data = create_res.json()
    assert blog_data["title"] == "My First Post"
    assert blog_data["body"] == "Hello World!"
    assert blog_data["creator"]["email"] == "alice@example.com"

    # Get all blogs
    all_res = client.get("/blog/", headers=headers)
    assert all_res.status_code == 200
    blogs = all_res.json()
    assert len(blogs) == 1
    assert blogs[0]["title"] == "My First Post"

    # Get single blog (assuming ID is 1)
    single_res = client.get("/blog/1", headers=headers)
    assert single_res.status_code == 200
    assert single_res.json()["title"] == "My First Post"


def test_owner_update_and_delete(client):
    # Register and login
    client.post("/user/", json={"name": "Alice", "email": "alice@example.com", "password": "password123"})
    login_res = client.post("/login", data={"username": "alice@example.com", "password": "password123"})
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Create blog
    client.post("/blog/", json={"title": "Original Title", "body": "Original Body"}, headers=headers)

    # Update blog
    update_res = client.put("/blog/1", json={"title": "Updated Title", "body": "Updated Body"}, headers=headers)
    assert update_res.status_code == 202
    updated_data = update_res.json()
    assert updated_data["title"] == "Updated Title"
    assert updated_data["body"] == "Updated Body"

    # Delete blog
    delete_res = client.delete("/blog/1", headers=headers)
    assert delete_res.status_code == 200

    # Verify blog is deleted
    get_res = client.get("/blog/1", headers=headers)
    assert get_res.status_code == 404


def test_second_user_cannot_modify_or_delete(client):
    # User 1 registers and creates blog
    client.post("/user/", json={"name": "Alice", "email": "alice@example.com", "password": "password123"})
    login1_res = client.post("/login", data={"username": "alice@example.com", "password": "password123"})
    token1 = login1_res.json()["access_token"]
    headers1 = {"Authorization": f"Bearer {token1}"}

    client.post("/blog/", json={"title": "Alice Post", "body": "Alice Content"}, headers=headers1)

    # User 2 registers and logins
    client.post("/user/", json={"name": "Bob", "email": "bob@example.com", "password": "password456"})
    login2_res = client.post("/login", data={"username": "bob@example.com", "password": "password456"})
    token2 = login2_res.json()["access_token"]
    headers2 = {"Authorization": f"Bearer {token2}"}

    # User 2 tries to update Alice's blog
    put_res = client.put("/blog/1", json={"title": "Hacked Title", "body": "Hacked Body"}, headers=headers2)
    assert put_res.status_code == 403
    assert put_res.json()["detail"] == "You can only modify your own blogs"

    # User 2 tries to delete Alice's blog
    del_res = client.delete("/blog/1", headers=headers2)
    assert del_res.status_code == 403
    assert del_res.json()["detail"] == "You can only modify your own blogs"

    # Verify blog remains unchanged
    get_res = client.get("/blog/1", headers=headers1)
    assert get_res.status_code == 200
    assert get_res.json()["title"] == "Alice Post"
    assert get_res.json()["body"] == "Alice Content"


def test_delete_missing_blog(client):
    client.post("/user/", json={"name": "Alice", "email": "alice@example.com", "password": "password123"})
    login_res = client.post("/login", data={"username": "alice@example.com", "password": "password123"})
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    del_res = client.delete("/blog/999", headers=headers)
    assert del_res.status_code == 404
