from django.db import transaction
from uuid import UUID

from src.core.genre.domain.genre import Genre
from src.core.genre.domain.genre_repository import GenreRepository
from src.django_project.genre_app.models import GenreModel


class DjangoORMGenreRepository(GenreRepository):
    def save(self, genre: Genre):
        with transaction.atomic():
            genre_model = GenreModelMapper.to_model(genre)
            genre_model.save()

    def get_by_id(self, id: UUID) -> Genre | None:
        try:
            genre_model = GenreModel.objects.get(id=id)
            genre = GenreModelMapper.to_entity(genre_model)
            return genre
        except GenreModel.DoesNotExist:
            return None

    def delete(self, id: UUID):
        try:
            genre_model = GenreModel.objects.get(id=id)
            genre_model.delete()
        except GenreModel.DoesNotExist:
            pass

    def update(self, genre: Genre) -> None:
        try:
            genre_model = GenreModel.objects.get(id=genre.id)
            with transaction.atomic():
                genre_model.name = genre.name
                genre_model.is_active = genre.is_active
                genre_model.categories.set(genre.categories)
                genre_model.save()
        except GenreModel.DoesNotExist:
            pass

    def list(self):
        genre_models = GenreModel.objects.all()
        genres = [
            GenreModelMapper.to_entity(genre_model) for genre_model in genre_models
        ]
        return genres


class GenreModelMapper:
    @staticmethod
    def to_model(genre: Genre) -> GenreModel:
        genre_model = GenreModel(
            id=genre.id,
            name=genre.name,
            is_active=genre.is_active,
        )
        genre_model.categories.set(genre.categories)
        return genre_model

    @staticmethod
    def to_entity(genre_model: GenreModel) -> Genre:
        return Genre(
            id=genre_model.id,
            name=genre_model.name,
            is_active=genre_model.is_active,
            categories=set(genre_model.categories.values_list("id", flat=True)),
        )
