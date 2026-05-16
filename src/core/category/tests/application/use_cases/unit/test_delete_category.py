import uuid
from unittest.mock import create_autospec

import pytest

from core.category.domain.category_repository import CategoryRepository
from src.core.category.application.use_cases.delete_category import (
    DeleteCategory,
    DeleteCategoryRequest,
)
from src.core.category.application.use_cases.exceptions import CategoryNotFound
from src.core.category.domain.category import Category


class TestDeleteCategory:
    def test_delete_category_from_repository(self):
        category = Category(
            name="Filme",
            description="Categoria de filmes",
        )
        repository_mock = create_autospec(CategoryRepository)
        repository_mock.get_by_id.return_value = category

        use_case = DeleteCategory(repository_mock)
        use_case.execute(DeleteCategoryRequest(id=category.id))

        repository_mock.delete.assert_called_once_with(category.id)

    def test_when_category_not_found_then_raise_exception(self):
        repository_mock = create_autospec(CategoryRepository)
        repository_mock.get_by_id.return_value = None
        use_case = DeleteCategory(repository=repository_mock)
        request = DeleteCategoryRequest(id=uuid.uuid4())
        with pytest.raises(CategoryNotFound):
            use_case.execute(request)

        repository_mock.delete.assert_not_called()
