from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import password_validation
from core.models import User, Role
from core.services.users_service import UsersService


class CreateUserForm(UserCreationForm):

    names = forms.CharField(
        label='Nombres',
        max_length=45,
        widget=forms.TextInput(attrs={
            'class': 'input input-bordered input-primary w-full rounded', 'placeholder': 'Nombres'}),
    )
    ci = forms.IntegerField(
        label='Cédula',
        widget=forms.TextInput(attrs={
            'class': 'input input-bordered input-primary w-full rounded', 'placeholder': 'Cédula'}),
    )
    role = forms.ModelChoiceField(
        label='Rol',
        queryset=Role.objects.all(),
        widget=forms.Select(
            attrs={'class': 'select select-bordered select-primary w-full rounded'}),
    )

    def __init__(self, *args, **kwargs):
        super(CreateUserForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update(
            {'class': 'input input-bordered input-primary w-full rounded', 'placeholder': 'Correo Electrónico'})
        self.fields['username'].widget.attrs.update(
            {'class': 'input input-bordered input-primary w-full rounded', 'placeholder': 'Nombre de usuario'})
        self.fields['password1'].widget.attrs.update(
            {'class': 'input input-bordered input-primary w-full rounded', 'placeholder': 'Contraseña'})
        self.fields['password2'].widget.attrs.update(
            {'class': 'input input-bordered input-primary w-full rounded', 'placeholder': 'Confirmar contraseña'})

    def clean_username(self):
        username = self.cleaned_data['username']
        userService = UsersService()
        if userService.checkExists(username):
            raise forms.ValidationError(
                "Este nombre de usuario ya está en uso.")
        return username

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Las contraseñas no coinciden.")
        password_validation.validate_password(password2, self.instance)
        return password2

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'password1', 'password2', 'email', 'names', 'ci',
                  'role']
