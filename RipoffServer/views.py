from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

import json

from RipoffServer.models import Product, Location, PaymentType, Ripoff


@login_required
def add_ripoff(request):
    errors = []

    product_name = request.POST['product_name']
    product_name = " ".join([word.strip().capitalize() for word in product_name.split().lower()])

    product, created = Product.objects.get_or_create(name=product_name)
    location = Location.objects.get(name=request.POST['location_name'])
    payment_type = PaymentType[request.POST['payment_type_name']]

    cost = request.POST['cost']

    if cost > 99.99:
        errors.append("Item price cannot be higher than $99.99")

    if not errors:
        ripoff = Ripoff(product=product, location=location, payment_type=payment_type, cost=cost)
        ripoff.save()

    return HttpResponse(json.dumps({'errors': errors}))
