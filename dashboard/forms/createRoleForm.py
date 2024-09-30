from django import forms
from core.models import Role, Permission


class CreateRoleForm(forms.ModelForm):
    permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.all(),
        widget=forms.CheckboxSelectMultiple(),
        required=False
    )

    class Meta:
        model = Role
        fields = ['name','all_access', 'permissions']
        labels = {
            'name': 'Nombre del rol',
            'permissions': 'Permisos',
            'all_access': 'Todos los accesos'
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'input input-bordered input-primary w-full rounded', 'placeholder': 'Nombre'}),
        }

    def __init__(self, *args, **kwargs):
        super(CreateRoleForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['permissions'].initial = self.instance.permissions.all()

    def save(self, commit=True):
        role = super().save(commit=False)
        if commit:
            role.save()
            self.save_m2m()
        return role
