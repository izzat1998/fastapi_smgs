import pytest

from app import schemas


def test_smgs_get_all(client, test_smgs):
    response = client.get('/api/v1/smgs/')

    def validate(smgs):
        return schemas.SMGSOut(**smgs)

    smgs_map = map(validate, response.json())
    smgs_list = list(smgs_map)
    assert len(smgs_list) == len(test_smgs)
    assert response.status_code == 200


def test_smgs_get_one(client, test_smgs):
    response = client.get(f'/api/v1/smgs/{test_smgs[0].id}/')
    assert response.status_code == 200


def test_get_one_smgs_not_exist(client, test_smgs):
    response = client.get(f'api/v1/smgs/888888888')
    assert response.status_code == 404


@pytest.mark.parametrize("smgs_dict", [
    {
        "railway_code": "12346",
        "sender": "sender",
        "departure_station": "departure_station",
        "sender_statement": "sender_statement",
        "recipient": "recipient",
        "destination_station": "destination_station",
        "border_crossing_stations": "border_crossing_stations",
        "railway_carriage": "railway_carriage",
        "shipping_name": "shipping_name",
        "container_owner": "container_owner",
        "container": "WSCU19982132",
        "type_of_packaging": "type_of_packaging",
        "number_of_seats": "number_of_seats",
        "net": "net",
        "tara": "tara",
        "gross": "gross",
        "seals": "seals",
        "seal_quantity": "seal_quantity",
        "submerged": "submerged",
        "method_of_determining_mass": "method_of_determining_mass",
        "payment_of_legal_fees": "payment_of_legal_fees",
        "carriers": "carriers",
        "documents_by_sender": "documents_by_sender",
        "additional_information": "additional_information",
        "custom_seal": "custom_seal",
        "inspector_name": "inspector_name",
        "date": "2022/16/8",
        "train_name": "Train 1"
    }, {
        "railway_code": "12346",
        "sender": "sender",
        "departure_station": "departure_station",
        "sender_statement": "sender_statement",
        "recipient": "recipient",
        "destination_station": "destination_station",
        "border_crossing_stations": "border_crossing_stations",
        "railway_carriage": "railway_carriage",
        "shipping_name": "shipping_name",
        "container_owner": "container_owner",
        "container": "WSCU19982132",
        "type_of_packaging": "type_of_packaging",
        "number_of_seats": "number_of_seats",
        "net": "net",
        "tara": "tara",
        "gross": "gross",
        "seals": "seals",
        "seal_quantity": "seal_quantity",
        "submerged": "submerged",
        "method_of_determining_mass": "method_of_determining_mass",
        "payment_of_legal_fees": "payment_of_legal_fees",
        "carriers": "carriers",
        "documents_by_sender": "documents_by_sender",
        "additional_information": "additional_information",
        "custom_seal": "custom_seal",
        "inspector_name": "inspector_name",
        "date": "2022/16/8",
        "train_name": "Train 1"
    }, {
        "railway_code": "12346",
        "sender": "sender",
        "departure_station": "departure_station",
        "sender_statement": "sender_statement",
        "recipient": "recipient",
        "destination_station": "destination_station",
        "border_crossing_stations": "border_crossing_stations",
        "railway_carriage": "railway_carriage",
        "shipping_name": "shipping_name",
        "container_owner": "container_owner",
        "container": "WSCU19982132",
        "type_of_packaging": "type_of_packaging",
        "number_of_seats": "number_of_seats",
        "net": "net",
        "tara": "tara",
        "gross": "gross",
        "seals": "seals",
        "seal_quantity": "seal_quantity",
        "submerged": "submerged",
        "method_of_determining_mass": "method_of_determining_mass",
        "payment_of_legal_fees": "payment_of_legal_fees",
        "carriers": "carriers",
        "documents_by_sender": "documents_by_sender",
        "additional_information": "additional_information",
        "custom_seal": "custom_seal",
        "inspector_name": "inspector_name",
        "date": "2022/16/8",
        "train_name": "Train 2"
    }
])
def test_create_smgs(client, smgs_dict):
    response = client.post("api/v1/smgs/", json=smgs_dict)
    assert response.status_code == 201


def test_delete_smgs(client, test_smgs):
    response = client.delete(f"api/v1/smgs/{test_smgs[1].id}")
    assert response.status_code == 204


def test_update_smgs(client, test_smgs):
    smgs_data = {
        "railway_code": "12qqw",
        "sender": "sender",
        "departure_station": "departure_station",
        "sender_statement": "sender_statement",
        "recipient": "recipient",
        "destination_station": "destination_station",
        "border_crossing_stations": "border_crossing_stations",
        "railway_carriage": "railway_carriage",
        "shipping_name": "shipping_name",
        "container_owner": "container_owner",
        "container": "qwqwqwqw",
        "type_of_packaging": "type_of_packaging",
        "number_of_seats": "number_of_seats",
        "net": "net",
        "tara": "tara",
        "gross": "gross",
        "seals": "seals",
        "seal_quantity": "seal_quantity",
        "submerged": "submerged",
        "method_of_determining_mass": "method_of_determining_mass",
        "payment_of_legal_fees": "payment_of_legal_fees",
        "carriers": "carriers",
        "documents_by_sender": "documents_by_sender",
        "additional_information": "additional_information",
        "custom_seal": "custom_seal",
        "inspector_name": "inspector_name",
        "date": "2022/16/8",
        "train_id": 1
    }
    response = client.put(f'api/v1/smgs/{test_smgs[0].id}', json=smgs_data)
    updated_smgs = schemas.SMGSOut(**response.json())
    assert response.status_code == 200
    assert updated_smgs.railway_code == smgs_data['railway_code']
