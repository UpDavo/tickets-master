from django import forms
from core.models import User, Role


class UpdateUserForm(forms.ModelForm):

    names = forms.CharField(
        label='Nombres',
        max_length=45,
        widget=forms.TextInput(attrs={
            'class': 'input input-bordered input-primary w-full rounded', 'placeholder': 'Nombres'}),
    )
    role = forms.ModelChoiceField(
        label='Rol',
        queryset=Role.objects.all(),
        widget=forms.Select(
            attrs={'class': 'select select-bordered select-primary w-full rounded'}),
    )
    ci = forms.IntegerField(
        label='Cédula',
        widget=forms.TextInput(attrs={
            'class': 'input input-bordered input-primary w-full rounded', 'placeholder': 'Cédula'}),
    )

    def __init__(self, *args, **kwargs):
        super(UpdateUserForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update(
            {'class': 'input input-bordered input-primary w-full rounded', 'placeholder': 'Correo Electrónico'})

    def clean_password2(self):
        # Al editar el usuario, no requerimos la validación de contraseñas
        return self.cleaned_data.get("password2")

    class Meta:
        model = User
        fields = ['email', 'names', 'role', 'ci']
