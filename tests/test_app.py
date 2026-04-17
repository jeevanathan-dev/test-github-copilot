from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)


def test_get_activities():
    """Test GET /activities returns activity data"""
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "description" in data["Chess Club"]
    assert "schedule" in data["Chess Club"]
    assert "max_participants" in data["Chess Club"]
    assert "participants" in data["Chess Club"]
    assert isinstance(data["Chess Club"]["participants"], list)


def test_signup_success():
    """Test successful signup for an activity"""
    # Get initial participant count
    response = client.get("/activities")
    initial_count = len(response.json()["Chess Club"]["participants"])

    # Perform signup
    response = client.post("/activities/Chess Club/signup?email=newstudent@mergington.edu")
    assert response.status_code == 200
    assert "Signed up newstudent@mergington.edu for Chess Club" == response.json()["message"]

    # Verify participant was added
    response = client.get("/activities")
    data = response.json()
    new_count = len(data["Chess Club"]["participants"])
    assert new_count == initial_count + 1
    assert "newstudent@mergington.edu" in data["Chess Club"]["participants"]


def test_signup_invalid_activity():
    """Test signup for non-existent activity"""
    response = client.post("/activities/Invalid Activity/signup?email=test@example.com")
    assert response.status_code == 404
    assert "Activity not found" == response.json()["detail"]


def test_root_redirect():
    """Test root URL redirects to static index.html"""
    response = client.get("/", follow_redirects=False)
    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"