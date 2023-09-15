from django.contrib import admin
from .models import merchant,merchant_service_details,customer
# Register your models here.
admin.site.register(merchant)
admin.site.register(customer)
admin.site.register(merchant_service_details)