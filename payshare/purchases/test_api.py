import pytest
from django.contrib.auth.hashers import check_password
from model_mommy import mommy
from rest_framework import status


def test_collective_password_not_saved_as_plain_test(db):
    collective = mommy.make("purchases.Collective")
    collective.password = "foobar"
    collective.save()
    assert collective.password != "foobar"
    assert check_password("foobar", collective.password)


@pytest.fixture
def collective(db):
    collective = mommy.make("purchases.Collective", password="foobar")
    return collective


def test_collective_check_password(collective):
    assert collective.check_password("foobar")


def test_collective_add_member(collective):
    user = mommy.make("auth.User")
    assert not collective.is_member(user)

    collective.add_member(user)
    assert collective.is_member(user)

    collective.add_member(user)
    assert collective.is_member(user)


@pytest.fixture
def collective_with_members(collective):
    user_1 = mommy.make("auth.User", username="user_1")
    user_2 = mommy.make("auth.User", username="user_2")
    collective.add_member(user_1)
    collective.add_member(user_2)
    return collective, user_1, user_2


def test_collective_members(collective_with_members):
    collective, user_1, user_2 = collective_with_members
    assert len(collective.members) == 2
    assert user_1 in collective.members
    assert user_2 in collective.members


def test_collective(collective_with_members, client):
    collective, user_1, user_2 = collective_with_members

    url = "/api/v1/{}".format(collective.key)
    response = client.get(url, follow=True, HTTP_AUTHORIZATION="foobar")
    assert response.status_code == status.HTTP_200_OK

    assert response.data["id"] == collective.id
    assert response.data["name"] == collective.name
    assert response.data["key"] == str(collective.key)

    assert len(response.data["members"]) == 2
    member_ids = [member["id"] for member in response.data["members"]]
    assert user_1.id in member_ids
    assert user_2.id in member_ids
