def test_signup_adds_new_participant(client):
    # Arrange
    activity_name = "Chess Club"
    new_email = "newstudent@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={new_email}")
    activities_response = client.get("/activities")
    activities_data = activities_response.json()

    # Assert
    assert response.status_code == 200
    assert new_email in response.json()["message"]
    assert new_email in activities_data[activity_name]["participants"]


def test_signup_duplicate_returns_bad_request(client):
    # Arrange
    activity_name = "Chess Club"
    duplicate_email = "michael@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={duplicate_email}")

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_signup_unknown_activity_returns_not_found(client):
    # Arrange
    activity_name = "Nonexistent Club"
    new_email = "newstudent@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={new_email}")

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_signup_after_unregister_allows_reregistration(client):
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"

    # Act
    unregister_response = client.post(f"/activities/{activity_name}/unregister?email={email}")
    re_register_response = client.post(f"/activities/{activity_name}/signup?email={email}")
    activities_data = client.get("/activities").json()

    # Assert
    assert unregister_response.status_code == 200
    assert re_register_response.status_code == 200
    assert email in activities_data[activity_name]["participants"]
