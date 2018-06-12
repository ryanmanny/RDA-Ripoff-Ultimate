from django.contrib import admin

from RipoffServer.models import SiteUser, Product, Location, DiscountPlan, Ripoff

admin.site.register(SiteUser)
admin.site.register(Product)
admin.site.register(Location)
admin.site.register(DiscountPlan)
admin.site.register(Ripoff)
