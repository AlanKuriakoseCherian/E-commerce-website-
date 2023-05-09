from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView

from store.models import Product


@method_decorator(login_required, "dispatch")
class ProfileView(TemplateView):
    template_name = "user-profile.html"


@method_decorator(login_required, "dispatch")
class ProductListView(ListView):
    model = Product
    template_name = "product-list.html"


@method_decorator(login_required, "dispatch")
class ProductCreateView(CreateView):
    model = Product
    fields = ('name', 'quantity')
    template_name = "product-form.html"
    success_url = '/products'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


@method_decorator(login_required, "dispatch")
class ProductUpdateView(UpdateView):
    model = Product
    fields = ('name', 'quantity')
    template_name = "product-form.html"
    success_url = '/products'


@method_decorator(login_required, "dispatch")
class ProductDeleteView(DeleteView):
    model = Product
    success_url = '/products'


