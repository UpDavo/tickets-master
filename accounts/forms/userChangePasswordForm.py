from django import forms
from django.contrib.auth import password_validation


class UserChangePasswordForm(forms.Form):
    error_messages = {
        'password_mismatch': "Las contraseñas no coinciden.",
        'password_incorrect': "La actual contraseña fue introducida incorrectamente.",
    }

    old_password = forms.CharField(
        label="Contraseña Actual",
        strip=False,
        widget=forms.PasswordInput(
            attrs={'autofocus': True, 'class': 'form-control'}),
    )

    new_password1 = forms.CharField(
        label='Nueva Contraseña',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )

    new_password2 = forms.CharField(
        label='Confirmar Nueva Contraseña',
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )

    field_order = ['old_password', 'new_password1', 'new_password2']

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean_old_password(self):
        old_password = self.cleaned_data["old_password"]
        if not self.user.check_password(old_password):
            raise forms.ValidationError(
                self.error_messages['password_incorrect'],
                code='password_incorrect',
            )
        return old_password

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(
                    self.error_messages['password_mismatch'],
                    code='password_mismatch',
                )
        password_validation.validate_password(password2, self.user)
        return password2

    def save(self, commit=True):
        password = self.cleaned_data["new_password1"]
        self.user.set_password(password)
        if commit:
            self.user.save()
        return self.user
