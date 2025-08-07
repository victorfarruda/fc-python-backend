import pytest
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT

from rest_framework.test import APIClient


@pytest.mark.django_db
class TestCreateAndEditCategory:
    def test_user_can_create_and_edit_category(self) -> None:
        api_client = APIClient()

        list_response = api_client.get('/api/categories/')
        assert list_response.data == {'data': []}

        create_response = api_client.post(
            '/api/categories/',
            data={
                'name': 'Movie',
                'description': 'Movie Description',
            }
        )

        assert HTTP_201_CREATED == create_response.status_code
        created_category_id = create_response.data['id']

        list_response = api_client.get('/api/categories/')
        assert {
            'data': [
                {
                    'id': created_category_id,
                    'name': 'Movie',
                    'description': 'Movie Description',
                    'is_active': True,
                }
            ]
        } == list_response.data

        update_request = api_client.put(
            f'/api/categories/{created_category_id}/',
            data={
                'name': 'Documentary',
                'description': 'Documentary description',
                'is_active': False,
            }
        )

        assert HTTP_204_NO_CONTENT == update_request.status_code

        list_response = api_client.get('/api/categories/')
        assert {
            'data': [
                {
                    'id': created_category_id,
                    'name': 'Documentary',
                    'description': 'Documentary description',
                    'is_active': False,
                }
            ]
        } == list_response.data
