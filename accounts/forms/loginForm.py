from django import forms
from django.contrib.auth.forms import AuthenticationForm, UsernameField


class LoginForm(AuthenticationForm):
    username = UsernameField(
        label='Correo Electrónico',
        max_length=254,
        widget=forms.TextInput(
            attrs={'autofocus': True, 'class': 'input input-bordered input-primary w-full rounded', 'placeholder': 'Correo Electrónico', }),
    )
    password = forms.CharField(
        label='Contraseña',
        strip=False,
        widget=forms.PasswordInput(
            attrs={'class': 'input input-bordered input-primary w-full rounded', 'placeholder': 'Contraseña'}),
    )

    def clean_username(self):
        username = self.cleaned_data['username']

        return str(username).lower()
