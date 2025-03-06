import pytest
from store.models import Product, Category
from contextlib import nullcontext as does_not_raise
from django.db.utils import IntegrityError


class TestCategories:
    @pytest.mark.django_db
    def test_categories_creation(self):
        with does_not_raise():
            category = Category(category_slug='test_category_slug', name='Test Category Name')
            assert category.category_slug == 'test_category_slug'
            assert category.name == 'Test Category Name'
            category.save()

        with does_not_raise():
            category2 = Category(category_slug='test_category_slug2', name='test_second_category_name')
            assert category2.category_slug == 'test_category_slug2'
            assert category2.name == 'test_second_category_name'
            category2.save()

        with does_not_raise():
            category3 = Category(category_slug='test_category_slug3', name='test_second_category_name')
            assert category3.category_slug == 'test_category_slug3'
            assert category3.name == 'test_second_category_name'
            category3.save()

        with pytest.raises(IntegrityError):
            wrong_category = Category(category_slug='test_category_slug3', name='lalala')
            wrong_category.save()


class TestProducts:
    @pytest.fixture(scope='class', autouse=False)
    def category(self):
        return Category(category_slug='test_category_slug', name='Test Category Name')

    @pytest.mark.django_db
    def test_product_creation(self, category):
        basic_product = Product(name='Test product 1', product_slug='test_product_slug_1',
                                category=category, price=418.99)
        product = Product(name='Test product 2', product_slug='test_product_slug_2',
                          category=category, price=200, description='test description',
                          quantity=38, discount=15)

        assert basic_product.name == 'Test product 1'
        assert basic_product.product_slug == 'test_product_slug_1'
        assert basic_product.category == category
        assert basic_product.price == 418.99

        assert product.name == 'Test product 2'
        assert product.product_slug == 'test_product_slug_2'
        assert product.category == category
        assert product.price == 200
        assert product.description == 'test description'
        assert product.quantity == 38
        assert product.discount == 15
        assert product.get_price() == round(product.price / 100 * (100 - product.discount), 2)
