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
    return CastMember(
        id=uuid4(),
        name="Director name",
        type=CastMemberType.DIRECTOR
    )


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
    def test_create_cast_member(
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
        assert "id" in response.data
        assert response.data["name"] == "Actor name"
        assert response.data["type"] == "ACTOR"
        

        created_cast_member_id = response.data["id"]
        saved_cast_member = cast_member_repository.get_by_id(created_cast_member_id)
        assert saved_cast_member is not None
        assert saved_cast_member.name == "Actor name"
        assert saved_cast_member.type.value == "ACTOR"


# @pytest.mark.django_db
# class TestUpdateAPI:
#     def test_when_request_data_is_valid_then_update_cast_member(
#         self,
#         category_repository: DjangoORMCategoryRepository,
#         category_movie: Category,
#         category_documentary: Category,
#         cast_member_repository: DjangoORMCastMemberRepository,
#         cast_member_actor: CastMember,
#     ) -> None:
#         category_repository.save(category_movie)
#         category_repository.save(category_documentary)
#         cast_member_repository.save(cast_member_actor)

#         url = f"/api/cast_members/{str(cast_member_actor.id)}/"
#         data = {
#             "name": "Drama",
#             "is_active": True,
#             "categories_id": [category_documentary.id],
#         }
#         response = APIClient().put(url, data=data)

#         assert response.status_code == status.HTTP_204_NO_CONTENT
#         updated_cast_member = cast_member_repository.get_by_id(cast_member_actor.id)
#         assert updated_cast_member.name == "Drama"
#         assert updated_cast_member.is_active is True
#         assert updated_cast_member.categories == {category_documentary.id}

#     def test_when_request_data_is_invalid_then_return_400(
#         self,
#         cast_member_director: CastMember,
#     ) -> None:
#         url = f"/api/cast_members/{str(cast_member_director.id)}/"
#         data = {
#             "name": "",
#             "is_active": True,
#             "categories_id": [],
#         }
#         response = APIClient().put(url, data=data)

#         assert response.status_code == status.HTTP_400_BAD_REQUEST
#         assert response.data == {"name": ["This field may not be blank."]}

#     def test_when_related_categories_do_not_exist_then_return_400(
#         self,
#         category_repository: DjangoORMCategoryRepository,
#         category_movie: Category,
#         category_documentary: Category,
#         cast_member_repository: DjangoORMCastMemberRepository,
#         cast_member_actor: CastMember,
#     ) -> None:
#         category_repository.save(category_movie)
#         category_repository.save(category_documentary)
#         cast_member_repository.save(cast_member_actor)

#         url = f"/api/cast_members/{str(cast_member_actor.id)}/"
#         data = {
#             "name": "Romance",
#             "is_active": True,
#             "categories_id": [uuid4()],  # non-existent category
#         }
#         response = APIClient().put(url, data=data)

#         assert response.status_code == status.HTTP_400_BAD_REQUEST
#         assert "Categories with provided IDs not found" in response.data["error"]

#     def test_when_cast_member_does_not_exist_then_return_404(self) -> None:
#         url = f"/api/cast_members/{str(uuid4())}/"
#         data = {
#             "name": "Romance",
#             "is_active": True,
#             "categories_id": [],
#         }
#         response = APIClient().put(url, data=data)

#         assert response.status_code == status.HTTP_404_NOT_FOUND


# @pytest.mark.django_db
# class TestDeleteAPI:
#     def test_when_cast_member_does_not_exist_then_return_404(self):
#         url = "/api/cast_members/00000000-0000-0000-0000-000000000000/"

#         response = APIClient().delete(url)

#         assert response.status_code == HTTP_404_NOT_FOUND

#     def test_when_pk_is_invlid_then_return_400(self):
#         url = "/api/cast_members/invalid-uuid/"

#         response = APIClient().delete(url)

#         assert response.status_code == HTTP_400_BAD_REQUEST

#     def test_delete_cast_member_from_repository(
#         self, cast_member_actor: CastMember, cast_member_repository: DjangoORMCastMemberRepository
#     ):
#         cast_member_repository.save(cast_member_actor)

#         assert cast_member_repository.get_by_id(cast_member_actor.id) is not None

#         url = f"/api/cast_members/{cast_member_actor.id}/"
#         response = APIClient().delete(url)

#         assert response.status_code == HTTP_204_NO_CONTENT
#         assert cast_member_repository.get_by_id(cast_member_actor.id) is None
