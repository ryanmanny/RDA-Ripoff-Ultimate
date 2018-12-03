from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.urls import reverse

from django.contrib.auth.decorators import login_required

from .models import SiteUser
from .models import Product
from .forms import RipoffForm


def homepage(request):
    return render(request, 'homepage.html', {"ripoff_link": reverse('add_ripoff')})


@login_required
def add_ripoff(request):
    if request.method == "POST":
        form = RipoffForm(request.POST)
        if form.is_valid():
            ripoff = form.save(commit=False)

            user = SiteUser.users.get(username="RIPOFF_RICK")  # TODO: How to associate with user?
            ripoff.user = user

            product_name = form.cleaned_data['product_name']
            product, _ = Product.products.get_or_create(name=product_name)
            ripoff.product = product

            ripoff.save()

            return JsonResponse({
                "ripoff_amount": ripoff.ripoff_amount,
            })
    else:
        form = RipoffForm()

    return render(request, 'add_ripoff.html', {'form': form, 'errors': form.errors})
