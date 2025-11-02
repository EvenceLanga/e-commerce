# inventory/forms.py
from django import forms

class AuxRelayInventoryForm(forms.Form):
    material = forms.CharField(max_length=255)
    alternative_mat = forms.CharField(max_length=255, required=False)
    mat_group = forms.CharField(max_length=255, required=False)
    basic_data_text = forms.CharField(widget=forms.Textarea, required=False)
    material_description = forms.CharField(widget=forms.Textarea, required=False)
    image = forms.ImageField(required=False)  # for image upload

    standard_price = forms.IntegerField(required=False, min_value=0)
    total_stock = forms.IntegerField(required=False, min_value=0)
    per = forms.IntegerField(required=False, min_value=0)