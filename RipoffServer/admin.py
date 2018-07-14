from django.contrib import admin

from RipoffServer.models import SiteUser, Product, Location, DiscountPlan, Ripoff


class RipoffAdmin(admin.ModelAdmin):
    readonly_fields = ('ripoff_amount',)


admin.site.register(SiteUser)
admin.site.register(Product)
admin.site.register(Location)
admin.site.register(DiscountPlan)
admin.site.register(Ripoff, RipoffAdmin)
