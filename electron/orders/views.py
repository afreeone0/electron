from django.contrib import messages
from django.db import transaction
from django.db.models import Prefetch
from django.shortcuts import redirect
from .forms import CreateOrderForm
from cart.models import Cart
from .models import Order, OrderItem
from django.forms import ValidationError
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, FormView
from django.urls import reverse_lazy


class MakeOrderView(LoginRequiredMixin, FormView):
    template_name = 'orders/make_order.html'
    form_class = CreateOrderForm
    success_url = reverse_lazy('orders_archive')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Оформление заказа'
        return context

    def get_initial(self):
        initial = super().get_initial()
        initial['first_name'] = self.request.user.first_name
        initial['last_name'] = self.request.user.last_name
        return initial

    def form_valid(self, form):
        request = self.request
        try:
            with transaction.atomic():
                user = request.user
                cart_items = Cart.objects.filter(user=user)

                if cart_items.exists():
                    # Создать заказ
                    order = Order.objects.create(
                        user=user,
                        phone_number=form.cleaned_data['phone_number'],
                        requires_delivery=form.cleaned_data['requires_delivery'],
                        delivery_address=form.cleaned_data['delivery_address'],
                        payment_on_get=form.cleaned_data['payment_on_get'],
                    )
                    # Создать заказанные товары
                    for cart_item in cart_items:
                        product = cart_item.product
                        name = cart_item.product.name
                        price = cart_item.product.get_price()
                        quantity = cart_item.quantity

                        if product.quantity < quantity:
                            raise ValidationError(f'Недостаточное количество {name}, в наличии {product.quantity}')

                        OrderItem.objects.create(
                            order=order,
                            product=product,
                            name=name,
                            price=price,
                            quantity=quantity,
                        )
                        product.quantity -= quantity
                        product.save()

                    # Очистить корзину пользователя после создания заказа
                    cart_items.delete()

                    messages.success(request, 'Заказ оформлен!')
                    return redirect('orders_archive')
        except ValidationError as e:
            messages.error(request, str(e))
            return redirect('make_order')

    def form_invalid(self, form):
        messages.error(self.request, 'Что-то пошло не так')
        return redirect(reverse_lazy('make_order'))


class OrdersArchiveView(LoginRequiredMixin, ListView):
    template_name = 'orders/orders_archive.html'
    paginate_by = 15
    context_object_name = 'orders'

    def get_queryset(self):
        q_set = (
            Order.objects.filter(user=self.request.user).prefetch_related(
                Prefetch(
                    'orderItems',
                    queryset=OrderItem.objects.select_related('product'),
                )
            ).order_by('-id')
        )
        return q_set

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['title'] = 'Мои заказы'
        return context
