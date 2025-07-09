import uuid

import pytest

from src.core.category.application.use_cases.exceptions import CategoryNotFound
from src.core.category.application.use_cases.update_category import UpdateCategory, UpdateCategoryRequest
from src.core.category.domain.category import Category
from src.core.category.infra.in_memory_category import InMemoryCategoryRepository


class TestUpdateCategory:
    def test_update_category_name_and_description(self):
        category = Category(
            name='Filme',
            description='Categoria para filmes',
            is_active=True,
        )
        repository = InMemoryCategoryRepository()
        repository.save(category)

        use_case = UpdateCategory(repository=repository)
        request = UpdateCategoryRequest(
            id=category.id,
            name='Série',
            description='Categoria para séries'
        )
        use_case.execute(request)

        updated_category = repository.get_by_id(category.id)
        assert updated_category.name == 'Série'
        assert updated_category.description == 'Categoria para séries'

    def test_can_deactivate_category(self):
        category = Category(
            name='Série',
            description='Categoria para séries',
            is_active=True,
        )
        repository = InMemoryCategoryRepository()
        repository.save(category)

        use_case = UpdateCategory(repository=repository)
        request = UpdateCategoryRequest(
            id=category.id,
            is_active=False,
        )

        use_case.execute(request)

        assert category.is_active is False
        assert category.name == 'Série'
        assert category.description == 'Categoria para séries'

    def test_can_activate_category(self):
        category = Category(
            name='Série',
            description='Categoria para séries',
            is_active=False,
        )
        repository = InMemoryCategoryRepository()
        repository.save(category)

        use_case = UpdateCategory(repository=repository)
        request = UpdateCategoryRequest(
            id=category.id,
            is_active=True,
        )

        use_case.execute(request)

        assert category.is_active is True
        assert category.name == 'Série'
        assert category.description == 'Categoria para séries'

    def test_cannot_update_category_not_found(self):
        category = Category(
            name='Série',
            description='Categoria para séries',
            is_active=False,
        )
        repository = InMemoryCategoryRepository()
        repository.save(category)

        use_case = UpdateCategory(repository=repository)
        request = UpdateCategoryRequest(
            id=uuid.uuid4(),
            is_active=True,
        )

        with pytest.raises(CategoryNotFound) as exc:
            use_case.execute(request)
