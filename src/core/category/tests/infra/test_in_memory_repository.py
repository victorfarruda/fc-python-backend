from src.core.category.domain.category import Category
from src.core.category.infra.in_memory_category import InMemoryCategoryRepository


class TestInMemoryCategoryRepository:
    def test_can_save_entity_category(self):
        repository = InMemoryCategoryRepository()
        category = Category(
            name='Filme',
            description='Categoria para Filmes',
        )
        repository.save(category)

        assert len(repository.categories) == 1
        assert repository.categories[0] == category
