# inventory/models.py
from django.db import models
from django.contrib.auth.models import User

class AuxRelayInventory(models.Model):
    material = models.CharField(max_length=255)
    alternative_mat = models.CharField(max_length=255, blank=True, null=True)
    mat_group = models.CharField(max_length=255, blank=True, null=True)
    basic_data_text = models.TextField(blank=True, null=True)
    material_description = models.TextField(blank=True, null=True)
    standard_price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_stock = models.IntegerField(default=0)
    per = models.CharField(max_length=50, blank=True, null=True)
    total_value = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    image_url = models.URLField(blank=True, null=True)

    created_by = models.ForeignKey(User, related_name="created_inventory", on_delete=models.SET_NULL, null=True, blank=True)
    last_updated_by = models.ForeignKey(User, related_name="updated_inventory", on_delete=models.SET_NULL, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.material
