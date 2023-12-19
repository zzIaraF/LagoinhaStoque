from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm



class UserForm(UserCreationForm): 
    opc = forms.ChoiceField(choices=[('1', 'Vendedor'), ('0', 'Gerente')], widget=forms.Select(), required=False)
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 
                  'username', 'password1', 'password2']

    
def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Usuário já cadastrado')
        return username

class UserEditForm(forms.ModelForm):
    novasenha = forms.CharField(widget=forms.PasswordInput(), label='Nova Senha', required=False)
    confirmarsenha = forms.CharField(widget=forms.PasswordInput(), label='Confirmar Nova Senha', required=False)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'novasenha', 'confirmarsenha']

    def clean_confirmarsenha(self):
        novasenha = self.cleaned_data.get('novasenha')
        confirmarsenha = self.cleaned_data.get('confirmarsenha')

        if novasenha and novasenha != confirmarsenha:
            raise forms.ValidationError('As senhas não coincidem')

        return confirmarsenha

    def save(self, commit=True):
        user = super().save(commit=False)

        novasenha = self.cleaned_data.get('novasenha')
        if novasenha:
            user.set_password(novasenha)

        if commit:
            user.save()

        return user