from django import forms

from product import models

class Productorm(forms.ModelForm):
    class Meta:
        model = models.Product
        fields = ('name', 'item', 'image', 'price_type')

    class Media:
        js = ('js/custom_file_upload.js',)
        css = {
            'all': ('css/custom_file_upload.css',)
        }

