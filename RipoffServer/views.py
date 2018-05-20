from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

import json

from models import Product, Location, PaymentType, RipOff


@login_required
def add_ripoff(request):
    product_name = request.GET['product_name']
    location_name = request.GET['location_name']
    payment_type_name = request.GET['payment_type_name']
    cost = request.GET['cost']

    product, created = Product.objects.get_or_create(name=product_name)
    location = Location.objects.get(name=location_name)
    payment_type = PaymentType[payment_type_name]

    ripoff = RipOff.objects.create_ripoff(product=product, location=location, payment_type=payment_type, cost=cost)
    return HttpResponse(json.dumps({'success': ripoff is not None}))
