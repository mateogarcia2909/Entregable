from django import forms
from django.contrib.auth.models import User
from .models import Perfil

class EditarPerfilForm(forms.ModelForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = Perfil
        fields = ['telefono', 'direccion'] 

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(EditarPerfilForm, self).__init__(*args, **kwargs)
        if self.user:
            self.fields['email'].initial = self.user.email

    def save(self, commit=True):
        perfil = super().save(commit=False)
        if self.user:
            self.user.email = self.cleaned_data['email']
            if commit:
                self.user.save()
        if commit:
            perfil.save()
        return perfil