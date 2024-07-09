from django import forms
from core.models import Stock, Product


class CreateStockForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(CreateStockForm, self).__init__(*args, **kwargs)
        self.fields['product'].queryset = Product.objects.all()

    class Meta:
        model = Stock
        fields = ['code', 'quantity', 'product']
        labels = {
            'code': 'Código',
            'quantity': 'Cantidad',
            'product': 'Producto Relacionado',
        }
        widgets = {
            'code': forms.TextInput(attrs={'class': 'input input-bordered input-primary w-full rounded', 'placeholder': 'Código'}),
            'quantity': forms.TextInput(attrs={'class': 'input input-bordered input-primary w-full rounded', 'placeholder': 'Cantidad'}),
            'product': forms.Select(attrs={'class': 'input input-bordered input-primary w-full rounded', 'placeholder': 'Producto Relacionado'}),
        }
