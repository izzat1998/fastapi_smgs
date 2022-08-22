import pytest

from app import schemas


def test_train_get_all(client, test_trains):
    response = client.get('/api/v1/train/')

    def validate(train):
        return schemas.TrainOut(**train)

    trains_map = map(validate, response.json())
    trains_list = list(trains_map)
    assert len(trains_list) == len(test_trains)
    assert response.status_code == 200


def test_get_one_train(client, test_trains):
    response = client.get(f'/api/v1/train/{test_trains[0].id}')
    train = schemas.TrainOut(**response.json())
    assert train.id == test_trains[0].id


def test_get_non_exist_train(client):
    response = client.get(f'/api/v1/train/888888888')
    assert response.status_code == 404


@pytest.mark.parametrize("name", [
    "name 1",
    "name 2",
    "name 3",
])
def test_create_train(client, test_trains, name):
    response = client.post('/api/v1/train/', json={"name": name})
    created_train = schemas.TrainCreate(**response.json())
    assert created_train.name == name


def test_update_train(client, test_trains):
    data = {
        "name": "testTrain",
    }
    response = client.post('/api/v1/train/', json=data)
    updated_train = schemas.TrainUpdate(**response.json())
    assert updated_train.name == "testTrain"
    assert response.status_code == 200


def test_delete_train(client, test_trains):
    res = client.delete(
        f"/api/v1/train/{test_trains[1].id}"
    )
    assert res.status_code == 204
