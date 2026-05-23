from uuid import uuid4

import pytest
from rest_framework import status
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
)
from rest_framework.test import APIClient

from src.core.cast_member.domain.cast_member import CastMember, CastMemberType
from src.django_project.cast_member_app.repository import DjangoORMCastMemberRepository


@pytest.fixture
def cast_member_actor() -> CastMember:
    return CastMember(
        id=uuid4(),
        name="Actor name",
        type=CastMemberType.ACTOR,
    )


@pytest.fixture
def cast_member_director() -> CastMember:
    return CastMember(id=uuid4(), name="Director name", type=CastMemberType.DIRECTOR)


@pytest.fixture
def cast_member_repository() -> DjangoORMCastMemberRepository:
    return DjangoORMCastMemberRepository()


@pytest.mark.django_db
class TestListAPI:
    def test_list_cast_members(
        self,
        cast_member_actor: CastMember,
        cast_member_director: CastMember,
        cast_member_repository: DjangoORMCastMemberRepository,
    ):
        cast_member_repository.save(cast_member_actor)
        cast_member_repository.save(cast_member_director)

        url = "/api/cast_members/"

        response = APIClient().get(url)

        expected_response = {
            "data": [
                {
                    "id": str(cast_member_actor.id),
                    "name": cast_member_actor.name,
                    "type": cast_member_actor.type.value,
                },
                {
                    "id": str(cast_member_director.id),
                    "name": cast_member_director.name,
                    "type": cast_member_director.type.value,
                },
            ]
        }
        assert response.status_code == HTTP_200_OK
        assert expected_response == response.data


@pytest.mark.django_db
class TestCreateAPI:
    def test_create_cast_member_then_returns_201(
        self,
        cast_member_repository: DjangoORMCastMemberRepository,
    ):

        url = "/api/cast_members/"
        data = {
            "id": str(uuid4()),
            "name": "Actor name",
            "type": "ACTOR",
        }

        response = APIClient().post(url, data=data, format="json")

        assert response.status_code == HTTP_201_CREATED
        created_cast_member_id = response.data["id"]
        assert created_cast_member_id == response.data["id"]

        saved_cast_member = cast_member_repository.get_by_id(created_cast_member_id)
        assert saved_cast_member is not None
        assert saved_cast_member.name == "Actor name"
        assert saved_cast_member.type.value == "ACTOR"

    def test_create_cast_member_with_invalid_data_then_returns_400(self):
        url = "/api/cast_members/"
        data = {
            "id": "invalid-uuid",
            "name": "",
            "type": "INVALID_TYPE",
        }

        response = APIClient().post(url, data=data, format="json")

        assert response.status_code == HTTP_400_BAD_REQUEST
        assert "id" in response.data
        assert "name" in response.data
        assert "type" in response.data


@pytest.mark.django_db
class TestUpdateAPI:
    def test_when_request_data_is_valid_then_update_cast_member(
        self,
        cast_member_repository: DjangoORMCastMemberRepository,
        cast_member_actor: CastMember,
    ) -> None:
        cast_member_repository.save(cast_member_actor)

        url = f"/api/cast_members/{str(cast_member_actor.id)}/"
        data = {
            "name": "Other name",
            "type": "DIRECTOR",
        }
        response = APIClient().put(url, data=data)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        updated_cast_member = cast_member_repository.get_by_id(cast_member_actor.id)
        assert updated_cast_member.name == "Other name"
        assert updated_cast_member.type.value == "DIRECTOR"

    def test_when_request_data_is_invalid_then_return_400(
        self,
        cast_member_director: CastMember,
    ) -> None:
        url = f"/api/cast_members/{str(cast_member_director.id)}/"
        data = {
            "name": "",
            "type": "DIRECTOR",
        }
        response = APIClient().put(url, data=data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        print(response.data)
        assert response.data == {"name": ["This field may not be blank."]}

    def test_when_pk_is_invalid_then_return_400(self) -> None:
        url = "/api/cast_members/invalid-uuid/"
        data = {
            "name": "Other name",
            "type": "DIRECTOR",
        }
        response = APIClient().put(url, data=data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == {"id": ["Must be a valid UUID."]}

    def test_when_request_data_has_invalid_type_then_return_400(self) -> None:
        url = f"/api/cast_members/{str(uuid4())}/"
        data = {
            "name": "Other name",
            "type": "INVALID_TYPE",
        }
        response = APIClient().put(url, data=data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == {"type": ['"INVALID_TYPE" is not a valid choice.']}

    def test_when_cast_member_does_not_exist_then_return_404(self) -> None:
        url = f"/api/cast_members/{str(uuid4())}/"
        data = {
            "name": "Other name",
            "type": "DIRECTOR",
        }
        response = APIClient().put(url, data=data)

        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestDeleteAPI:
    def test_when_cast_member_does_not_exist_then_return_404(self):
        url = "/api/cast_members/00000000-0000-0000-0000-000000000000/"

        response = APIClient().delete(url)

        assert response.status_code == HTTP_404_NOT_FOUND

    def test_when_pk_is_invalid_then_return_400(self):
        url = "/api/cast_members/invalid-uuid/"

        response = APIClient().delete(url)

        assert response.status_code == HTTP_400_BAD_REQUEST

    def test_delete_cast_member_from_repository(
        self,
        cast_member_actor: CastMember,
        cast_member_repository: DjangoORMCastMemberRepository,
    ):
        cast_member_repository.save(cast_member_actor)

        assert cast_member_repository.get_by_id(cast_member_actor.id) is not None

        url = f"/api/cast_members/{cast_member_actor.id}/"
        response = APIClient().delete(url)

        assert response.status_code == HTTP_204_NO_CONTENT
        assert cast_member_repository.get_by_id(cast_member_actor.id) is None
