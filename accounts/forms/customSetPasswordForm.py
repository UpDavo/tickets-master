from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import SetPasswordForm


class CustomSetPasswordForm(SetPasswordForm):
	error_messages = {
		'password_mismatch': "Las contraseñas no coinciden",
		'required': 'Este campo es requerido'
	}

	new_password1 = forms.CharField(
		label="Nueva Contraseña",
		widget=forms.PasswordInput(attrs={'class': 'form-control rounded-0'}),
		strip=False,
		help_text=password_validation.password_validators_help_text_html(),
		error_messages=error_messages,
	)
	new_password2 = forms.CharField(
		label="Confirmar Contraseña",
		strip=False,
		widget=forms.PasswordInput(attrs={'class': 'form-control rounded-0'}),
		error_messages=error_messages
	)