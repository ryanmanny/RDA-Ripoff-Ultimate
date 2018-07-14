from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

import json

from RipoffServer.models import Product, Location, PaymentType, Ripoff


@login_required
def add_ripoff(request):
    errors = []

    product_name = request.POST['product_name']
    location_name = request.POST['location_name']
    payment_type_name = request.POST['payment_type_name']
    cost = request.POST['cost']

    product_name = " ".join([word.strip().capitalize() for word in product_name.split().lower()])

    product, created = Product.objects.get_or_create(name=product_name)
    location = Location.objects.get(name=location_name)
    payment_type = PaymentType[payment_type_name]

    if not errors:
        ripoff = Ripoff(product=product, location=location, payment_type=payment_type, cost=cost)
        ripoff.save()

    return HttpResponse(json.dumps({'errors': errors}))
