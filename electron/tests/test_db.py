import pytest
from cart.models import Cart
from store.models import Product, Category
from users.models import User
from orders.models import Order, OrderItem


@pytest.mark.django_db
def test_category_and_product_and_cart_models(db):
    category = Category.objects.create(category_slug='test_category', name='Test Category')
    assert category.category_slug == 'test_category'
    assert category.name == 'Test Category'
    assert Category.objects.count() == 1

    product = Product.objects.create(category=category, name='Test Product',
                                     product_slug='test_product_slug', price=100,
                                     description='test description abcd efgh',
                                     quantity=10, discount=10)
    assert product.category == category
    assert product.price == 100
    assert product.discount == 10
    assert product.get_price() == round(90, 2)
    assert Product.objects.count() == 1

    cart1 = Cart.objects.create(product=product, quantity=2)
    assert cart1.product == product
    assert cart1.quantity == 2
    assert cart1.get_price_for_product() == 90 * 2
    cart2 = Cart.objects.create(product=product, quantity=4)
    assert cart2.product == product
    assert cart2.quantity == 4
    assert cart2.get_price_for_product() == 90 * 4
    assert Cart.objects.get_total_quantity() == 6
    assert Cart.objects.get_total_price_for_user() == 4*90 + 2*90
    assert Cart.objects.count() == 2


@pytest.mark.django_db
def test_users_and_orders_models(db):
    user = User.objects.create(username='test_username', password='test_password123',
                               first_name='Test', last_name='Testson',
                               email='test_email@gmail.com', phone_number='+79008003020')
    assert user.username == 'test_username'
    assert user.email == 'test_email@gmail.com'
    assert user.phone_number == '+79008003020'

    order = Order.objects.create(user=user, phone_number=user.phone_number[1:])
    assert order.user == user
    assert order.phone_number == '79008003020'
    assert not order.requires_delivery
    assert not order.payment_on_get
    assert not order.is_paid
    assert order.status == 'В обработке'
    assert Order.objects.count() == 1

    category = Category.objects.create(category_slug='test_category', name='Test Category')
    product = Product.objects.create(category=category, name='Test Product',
                                     product_slug='test_product_slug', price=100,
                                     description='test description abcd efgh',
                                     quantity=10, discount=10)
    order_item1 = OrderItem.objects.create(order=order, product=product,
                                           name='Test Product', price=90, quantity=5)
    assert order_item1.order == order
    assert order_item1.price == 90
    assert order_item1.quantity == 5
    assert order_item1.products_price() == 90 * 5
    order_item2 = OrderItem.objects.create(order=order, product=product,
                                           name='Test Product', price=90, quantity=3)
    assert order_item2.order == order
    assert order_item2.price == 90
    assert order_item2.quantity == 3
    assert order_item2.products_price() == 90 * 3
    assert OrderItem.objects.total_price() == 90*3 + 90*5
    assert OrderItem.objects.total_quantity() == 8
    assert OrderItem.objects.count() == 2
