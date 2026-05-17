from src.core.category.domain.category import Category
from src.core.category.infra.in_memory_category import InMemoryCategoryRepository
from src.core.genre.application.use_cases.list_genre import GenreOutput, ListGenre
from src.core.genre.domain.genre import Genre
from src.core.genre.infra.in_memory_genre import InMemoryGenreRepository


class TestListGenre:
    def test_list_genre_with_associated_categories(self):
        movie_category = Category(name="Movie", description="Movie category")
        documentary_category = Category(
            name="Documentary", description="Documentary movie category"
        )
        InMemoryCategoryRepository(categories=[movie_category, documentary_category])

        genre = Genre(
            name="Drama", categories={movie_category.id, documentary_category.id}
        )
        genre_repository = InMemoryGenreRepository(genres=[genre])

        use_case = ListGenre(repository=genre_repository)
        output = use_case.execute(input=ListGenre.Input())

        assert len(output.data) == 1

        assert output == ListGenre.Output(
            data=[
                GenreOutput(
                    id=genre.id,
                    name=genre.name,
                    is_active=True,
                    categories={movie_category.id, documentary_category.id},
                )
            ]
        )

    def test_list_genre_with_no_genres(self):
        genre_repository = InMemoryGenreRepository(genres=[])
        use_case = ListGenre(repository=genre_repository)
        output = use_case.execute(input=ListGenre.Input())

        assert len(output.data) == 0
        assert output == ListGenre.Output(data=[])
