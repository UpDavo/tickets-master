from django import forms
from core.models import Product


class CreateProductForm(forms.ModelForm):

    class Meta:
        model = Product
        # fields = ['name', 'sku', 'price', 'image', 'is_fisical','starred', 'active']
        fields = ['name', 'sku', 'price', 'image', 'starred', 'active']
        labels = {
            'name': 'Nombre del producto',
            'sku': 'SKU',
            'price': 'Precio del producto',
            'starred': 'Es producto destacado',
            'image': 'Imágen del producto',
            'active': 'Activo?',
            # 'is_fisical': 'Es producto físico',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'input input-bordered input-primary w-full rounded', 'placeholder': 'Nombre del producto'}),
            'sku': forms.TextInput(attrs={'class': 'input input-bordered input-primary w-full rounded', 'placeholder': 'SKU'}),
            'price': forms.TextInput(attrs={'class': 'input input-bordered input-primary w-full rounded', 'placeholder': 'Precio del producto'}),
            'image': forms.FileInput(attrs={'class': 'file-input file-input-primary file-input-bordered w-full rounded', 'placeholder': 'Imágen del producto'}),
            # 'is_fisical': forms.CheckboxInput(attrs={'class': 'toggle toggle-primary'}),
            'active': forms.CheckboxInput(attrs={'class': 'toggle toggle-primary'}),
            'starred': forms.CheckboxInput(attrs={'class': 'toggle toggle-primary'}),
        }
