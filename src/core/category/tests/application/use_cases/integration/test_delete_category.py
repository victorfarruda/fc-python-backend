from src.core.category.application.use_cases.delete_category import (
    DeleteCategory,
    DeleteCategoryRequest,
)
from src.core.category.domain.category import Category
from src.core.category.infra.in_memory_category import InMemoryCategoryRepository


class TestDeleteCategory:
    def test_delete_category_from_repository(self):
        category_filme = Category(name="Filme", description="Categoria para filmes")
        category_serie = Category(name="Série", description="Categoria para series")
        repository = InMemoryCategoryRepository(
            categories=[category_filme, category_serie]
        )
        use_case = DeleteCategory(repository=repository)
        request = DeleteCategoryRequest(id=category_filme.id)

        assert repository.get_by_id(request.id) is not None
        response = use_case.execute(request)

        assert repository.get_by_id(request.id) is None
        assert response is None
