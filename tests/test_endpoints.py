import pytest

from party.calculations import calculate


def test_parties_list(client, prepare_inactive_party):
    response = client.get('http://localhost:8000/party/parties/')
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_party_detail(client, create_party, small_party_setup):
    party, members = small_party_setup
    calculate(party)
    base_url = 'http://localhost:8000/party/parties/'
    url = base_url + f'{party.id}/'
    response = client.get(url)
    assert response.status_code == 200
    response = response.json()
    assert response.get('total_spent') == 20
    assert len(response.get('members')) == 3
    assert len(response.get('exchanges')) == 2
