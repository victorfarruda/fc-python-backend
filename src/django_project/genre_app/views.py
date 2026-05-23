from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
)
from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response

from src.core.genre.application.exceptions import (
    GenreNotFound,
    InvalidGenre,
    RelatedCategoriesNotFound,
)
from src.core.genre.application.use_cases.create_genre import CreateGenre
from src.core.genre.application.use_cases.delete_genre import DeleteGenre
from src.core.genre.application.use_cases.list_genre import ListGenre
from src.core.genre.application.use_cases.update_genre import UpdateGenre
from src.django_project.category_app.repository import DjangoORMCategoryRepository
from src.django_project.genre_app.repository import DjangoORMGenreRepository
from src.django_project.genre_app.serializers import (
    CreateGenreInputSerializer,
    CreateGenreOutputSerializer,
    DeleteGenreInputSerializer,
    ListGenreOutputSerializer,
    UpdateGenreInputSerializer,
)


class GenreViewSet(viewsets.ViewSet):
    def list(self, request: Request) -> Response:
        order_by = request.query_params.get("order_by", "name")
        use_case = ListGenre(repository=DjangoORMGenreRepository())
        output: ListGenre.Output = use_case.execute(input=ListGenre.Input(order_by=order_by))

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

    def destroy(self, request: Request, pk=None) -> Response:
        serializer = DeleteGenreInputSerializer(data={"id": pk})
        serializer.is_valid(raise_exception=True)
        input = DeleteGenre.DeleteGenreInput(**serializer.validated_data)
        use_case = DeleteGenre(repository=DjangoORMGenreRepository())

        try:
            use_case.execute(input)
        except GenreNotFound:
            return Response(status=HTTP_404_NOT_FOUND)

        return Response(status=HTTP_204_NO_CONTENT)

    def update(self, request: Request, pk=None) -> Response:
        serializer = UpdateGenreInputSerializer(
            data={
                **request.data,
                "id": pk,
            }
        )
        serializer.is_valid(raise_exception=True)
        input = UpdateGenre.Input(**serializer.validated_data)
        use_case = UpdateGenre(
            repository=DjangoORMGenreRepository(),
            category_repository=DjangoORMCategoryRepository(),
        )
        try:
            use_case.execute(input=input)
        except RelatedCategoriesNotFound:
            return Response(
                status=HTTP_400_BAD_REQUEST,
                data={"error": "Categories with provided IDs not found"},
            )
        except GenreNotFound:
            return Response(status=HTTP_404_NOT_FOUND)

        return Response(status=HTTP_204_NO_CONTENT)
