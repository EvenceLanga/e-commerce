# inventory/admin.py
from django.contrib import admin
from .models import AuxRelayInventory

@admin.register(AuxRelayInventory)
class AuxRelayInventoryAdmin(admin.ModelAdmin):
    list_display = ("material", "standard_price", "total_stock", "created_by", "last_updated_by", "created_at", "updated_at")
    
    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.created_by = request.user  # first time creation
        obj.last_updated_by = request.user  # always set to the current user
        super().save_model(request, obj, form, change)
