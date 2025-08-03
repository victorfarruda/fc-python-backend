from uuid import UUID

from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_201_CREATED

from core.category.application.use_cases.create_category import CreateCategoryRequest, CreateCategory, \
    CreateCategoryResponse
from django_project.category_app.serializers import ListCategoryResponseSerializer, RetrieveCategoryRequestSerializer, \
    CategoryResponseSerializer, RetrieveCategoryResponseSerializer, CreateCategoryRequestSerializer, \
    CreateCategoryResponseSerializer
from src.core.category.application.use_cases.exceptions import CategoryNotFound, InvalidCategoryData
from src.core.category.application.use_cases.get_category import GetCategory, GetCategoryRequest, GetCategoryResponse
from django_project.category_app.repository import DjangoORMCategoryRepository
from src.core.category.application.use_cases.list_category import ListCategoryRequest, ListCategory


class CategoryViewSet(viewsets.ViewSet):
    def list(self, request: Request) -> Response:
        input = ListCategoryRequest()
        use_case = ListCategory(repository=DjangoORMCategoryRepository())
        output = use_case.execute(input)

        serializer = ListCategoryResponseSerializer(instance=output)

        return Response(status=HTTP_200_OK, data=serializer.data)

    def retrieve(self, request: Request, pk=None):
        serializer = RetrieveCategoryRequestSerializer(data={'id': pk})
        serializer.is_valid(raise_exception=True)

        use_case = GetCategory(repository=DjangoORMCategoryRepository())

        try:
            output: GetCategoryResponse = use_case.execute(
                request=GetCategoryRequest(id=serializer.validated_data['id'])
            )
        except CategoryNotFound as e:
            return Response(status=HTTP_404_NOT_FOUND)

        category_output = RetrieveCategoryResponseSerializer(instance=output)
        return Response(
            status=HTTP_200_OK,
            data=category_output.data,
        )

    def create(self, request: Request) -> Response:
        serializer = CreateCategoryRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        input = CreateCategoryRequest(**serializer.validated_data)
        use_case = CreateCategory(repository=DjangoORMCategoryRepository())
        output: CreateCategoryResponse = use_case.execute(input)

        category_output = CreateCategoryResponseSerializer(instance=output)

        return Response(
            status=HTTP_201_CREATED,
            data=category_output.data,
        )
