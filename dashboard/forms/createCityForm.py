from django import forms
from core.models import City

class CreateCityForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(CreateCityForm, self).__init__(*args, **kwargs)

    class Meta:
        model = City
        fields = ['name']
        labels = {
            'name': 'Nombre de la Ciudad',
        }
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'input input-bordered input-primary w-full rounded', 
                'placeholder': 'Nombre de la Ciudad'
            }),
        }