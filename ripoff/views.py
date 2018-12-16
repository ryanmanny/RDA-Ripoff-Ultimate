from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.urls import reverse

from django.contrib.auth.decorators import login_required

from .models import Product
from .forms import RipoffForm


# TODO: Subclass from some Abstract Index Class that renders links to other pages
# TODO: Figure out if this template should go in the global templates folder...
def homepage(request):
    return render(request, 'ripoff/homepage.html', {"ripoff_link": reverse('add_ripoff')})


# TODO: Replace with class-based views?
@login_required
def add_ripoff(request):
    if request.method == "POST":
        form = RipoffForm(request.POST)
        if form.is_valid():
            ripoff = form.save(commit=False)

            ripoff.user = request.user

            product_name = form.cleaned_data['product_name']
            product, _ = Product.products.get_or_create(name=product_name)
            ripoff.product = product

            ripoff.save()

            return JsonResponse({
                "ripoff_amount": ripoff.ripoff_amount,
            })
    else:
        form = RipoffForm()

    return render(request, 'ripoff/add_ripoff.html', {'form': form, 'errors': form.errors})
