from django.shortcuts import redirect, reverse
from django.urls import reverse_lazy
from .forms import UserLoginForm, UserProfileForm, UserRegistrationForm
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from cart.models import Cart
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin


class UserLoginView(LoginView):
    template_name = 'users/login.html'
    form_class = UserLoginForm
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        user = form.get_user()

        session_key = self.request.session.session_key

        if user:
            auth.login(self.request, user)
            messages.success(self.request, 'Logged in successfully!')

            if session_key:
                for cart_not_auth in Cart.objects.filter(session_key=session_key):
                    cart_auth = Cart.objects.filter(user=user, product=cart_not_auth.product).first()
                    if cart_auth:
                        cart_auth.quantity += cart_not_auth.quantity
                        cart_auth.save()
                        cart_not_auth.delete()
                    else:
                        cart_not_auth.user = user
                        cart_not_auth.session_key = None
                        cart_not_auth.save()

            return redirect(reverse('index'), permanent=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Войти'
        return context


class UserProfileView(LoginRequiredMixin, UpdateView):
    template_name = 'users/profile.html'
    form_class = UserProfileForm
    success_url = reverse_lazy('profile')

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, 'Профиль обновлён')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Профиль'
        return context


class UserRegistrationView(CreateView):
    template_name = 'users/registration.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        session_key = self.request.session.session_key

        form.save()
        messages.success(self.request, 'Вы успешно зарегестрировались')
        auth.login(self.request, form.instance)

        if session_key:
            Cart.objects.filter(session_key=session_key).update(user=form.instance)

        return redirect(reverse('index'), permanent=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Регистрация'
        return context


@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    url = reverse('index')
    return redirect(url)
