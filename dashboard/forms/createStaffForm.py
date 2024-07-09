from django import forms
from core.models import Staff


class CreateStaffForm(forms.ModelForm):
    class Meta:
        model = Staff
        fields = ['name', 'last_name', 'email',
                  'id_number']
        labels = {
            'name': 'Nombre',
            'last_name': 'Apellido',
            'email': 'Correo electrónico',
            'id_number': 'Número de identificación',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'input input-bordered input-primary w-full rounded', 'placeholder': 'Nombre'}),
            'last_name': forms.TextInput(attrs={'class': 'input input-bordered input-primary w-full rounded', 'placeholder': 'Apellido'}),
            'email': forms.EmailInput(attrs={'class': 'input input-bordered input-primary w-full rounded', 'placeholder': 'Correo electrónico'}),
            'id_number': forms.TextInput(attrs={'class': 'input input-bordered input-primary w-full rounded', 'placeholder': 'Número de identificación'}),
        }
