from django.contrib import admin

from .models import SiteUser, Product, Location, DiscountPlan, Ripoff, RDAPlan


admin.site.register(SiteUser)

admin.site.register(RDAPlan)
admin.site.register(Product)
admin.site.register(Location)
admin.site.register(DiscountPlan)


class RipoffAdmin(admin.ModelAdmin):
    readonly_fields = ('ripoff_amount',)


admin.site.register(Ripoff, RipoffAdmin)