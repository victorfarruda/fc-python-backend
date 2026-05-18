import pytest

from src.core.genre.domain.genre import Genre
from src.django_project.category_app.models import Category
from src.django_project.category_app.repository import DjangoORMCategoryRepository
from src.django_project.genre_app.repository import DjangoORMGenreRepository
from src.django_project.genre_app.models import GenreModel


@pytest.mark.django_db
class TestSave:
    def test_saves_genre_in_database(self):
        genre = Genre(name="Action")
        genre_repository = DjangoORMGenreRepository()

        assert GenreModel.objects.count() == 0
        genre_repository.save(genre)

        assert GenreModel.objects.count() == 1
        genre_model = GenreModel.objects.first()
        assert genre_model.id == genre.id
        assert genre_model.name == genre.name
        assert genre_model.is_active is True

    def test_saves_genre_with_categories(self):
        category_repository = DjangoORMCategoryRepository()
        category1 = Category(name="Movie", description="Description Movie")
        category_repository.save(category1)

        genre_repository = DjangoORMGenreRepository()
        genre = Genre(name="Romance", categories=[category1.id])
        
        assert GenreModel.objects.count() == 0
        genre_repository.save(genre)
        
        assert GenreModel.objects.count() == 1
        genre_model = GenreModel.objects.first()
        assert genre_model.categories.count() == 1
        related_category = genre_model.categories.get()
        assert related_category.id == category1.id
        assert related_category.name == "Movie"