from django.contrib import admin
from.models import category,subcategory,product,cart,cartitem

# Register your models here.
admin.site.register(category)
admin.site.register(subcategory)
admin.site.register(product)
admin.site.register(cart)
admin.site.register(cartitem)

