from unittest.mock import create_autospec

from src.core.category.domain.category_repository import CategoryRepository
from src.core.category.application.use_cases.update_category import (
    UpdateCategory,
    UpdateCategoryRequest,
)
from src.core.category.domain.category import Category


class TestUpdateCategory:
    def test_update_category_name(self):
        category = Category(
            name="Filme",
            description="Categoria para filmes",
            is_active=True,
        )
        repository_mock = create_autospec(CategoryRepository)
        repository_mock.get_by_id.return_value = category

        use_case = UpdateCategory(repository=repository_mock)
        request = UpdateCategoryRequest(
            id=category.id,
            name="Série",
        )

        use_case.execute(request)

        assert category.name == "Série"
        assert category.description == "Categoria para filmes"
        repository_mock.update.assert_called_once_with(category)

    def test_update_category_description(self):
        category = Category(
            name="Filme",
            description="Categoria para filmes",
            is_active=True,
        )
        repository_mock = create_autospec(CategoryRepository)
        repository_mock.get_by_id.return_value = category

        use_case = UpdateCategory(repository=repository_mock)
        request = UpdateCategoryRequest(
            id=category.id,
            description="Categoria para séries",
        )

        use_case.execute(request)

        assert category.name == "Filme"
        assert category.description == "Categoria para séries"
        repository_mock.update.assert_called_once_with(category)

    def test_can_deactivate_category(self):
        category = Category(
            name="Série",
            description="Categoria para séries",
            is_active=True,
        )
        repository_mock = create_autospec(CategoryRepository)
        repository_mock.get_by_id.return_value = category

        use_case = UpdateCategory(repository=repository_mock)
        request = UpdateCategoryRequest(
            id=category.id,
            is_active=False,
        )

        use_case.execute(request)

        assert category.is_active is False
        assert category.name == "Série"
        assert category.description == "Categoria para séries"
        repository_mock.update.assert_called_once_with(category)

    def test_can_activate_category(self):
        category = Category(
            name="Série",
            description="Categoria para séries",
            is_active=False,
        )
        repository_mock = create_autospec(CategoryRepository)
        repository_mock.get_by_id.return_value = category

        use_case = UpdateCategory(repository=repository_mock)
        request = UpdateCategoryRequest(
            id=category.id,
            is_active=True,
        )

        use_case.execute(request)

        assert category.is_active is True
        assert category.name == "Série"
        assert category.description == "Categoria para séries"
        repository_mock.update.assert_called_once_with(category)
