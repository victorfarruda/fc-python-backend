from rest_framework.status import HTTP_200_OK
from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response

from src.core.genre.application.use_cases.list_genre import ListGenre
from src.django_project.genre_app.repository import DjangoORMGenreRepository
from src.django_project.genre_app.serializers import ListGenreOutputSerializer


class GenreViewSet(viewsets.ViewSet):
    def list(self, request: Request) -> Response:
        use_case = ListGenre(repository=DjangoORMGenreRepository())
        output: ListGenre.Output = use_case.execute(input=ListGenre.Input())

        serializer = ListGenreOutputSerializer(instance=output)

        return Response(status=HTTP_200_OK, data=serializer.data)
