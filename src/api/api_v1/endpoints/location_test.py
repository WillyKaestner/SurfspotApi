from fastapi.testclient import TestClient
from src.main import app
from src.crud.repository import get_crud_location
from src.crud import crud_location

client = TestClient(app)

# override dependency in API to get a repository based on the StorageType provided
def override_dependency():
    return crud_location.FakeDB()


app.dependency_overrides[get_crud_location] = override_dependency


def test_get_location_with_id():
    response = client.get("/location/1")
    response_data = response.json()
    assert response.status_code == 200
    assert response_data["id"] == 1
    assert response_data["name"] == "Mos"
    assert response_data["kitespot"] is True
    assert response_data["surfspot"] is True
    assert response_data["best_tide"] == "low to mid"
    assert response_data["best_wind"] == "north-west to south"
    # assert response.json() == {
    #     "id": 1,
    #     "name": "Mos",
    #     "kitespot": True,
    #     "surfspot": True,
    #     "best_tide": "low to mid",
    #     "best_wind": "north-west to south"
    # }

def test_create_new_location():
    pass
