from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response

from src.core.genre.application.exceptions import InvalidGenre, RelatedCategoriesNotFound
from src.core.genre.application.use_cases.create_genre import CreateGenre
from src.core.genre.application.use_cases.list_genre import ListGenre
from src.django_project.category_app.repository import DjangoORMCategoryRepository
from src.django_project.genre_app.repository import DjangoORMGenreRepository
from src.django_project.genre_app.serializers import (
    CreateGenreInputSerializer,
    CreateGenreOutputSerializer,
    ListGenreOutputSerializer,
)


class GenreViewSet(viewsets.ViewSet):
    def list(self, request: Request) -> Response:
        use_case = ListGenre(repository=DjangoORMGenreRepository())
        output: ListGenre.Output = use_case.execute(input=ListGenre.Input())

        serializer = ListGenreOutputSerializer(instance=output)

        return Response(status=HTTP_200_OK, data=serializer.data)

    def create(self, request: Request) -> Response:
        serializer = CreateGenreInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        use_case: CreateGenre = CreateGenre(
            repository=DjangoORMGenreRepository(),
            category_repository=DjangoORMCategoryRepository(),
        )
        try:
            output: CreateGenre.Output = use_case.execute(
                input=CreateGenre.Input(**serializer.validated_data)
            )
        except (InvalidGenre, RelatedCategoriesNotFound) as e:
            return Response(status=HTTP_400_BAD_REQUEST, data={"error": str(e)})

        genre_output_serializer = CreateGenreOutputSerializer(instance=output)
        return Response(status=HTTP_201_CREATED, data=genre_output_serializer.data)
