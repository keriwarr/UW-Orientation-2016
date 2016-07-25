from django import forms

from users.models import CustomUser
from users.programs import PROGRAMS


class CustomUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'team', 'position', 'photo']

    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-input', 'readonly': True}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-input', 'readonly': True}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-input', 'readonly': True}))


class RegistrationForm(forms.Form):
    username = forms.CharField(label='Quest ID', max_length=100, widget=forms.TextInput(attrs={'class': 'form-input'}))
    first_name = forms.CharField(label='First Name', max_length=120, widget=forms.TextInput(attrs={'class': 'form-input'}))
    last_name = forms.CharField(label='Last Name', max_length=120, widget=forms.TextInput(attrs={'class': 'form-input'}))
    school = forms.CharField(label='School', max_length=120, widget=forms.TextInput(attrs={'class': 'form-input'}))
    program = forms.ChoiceField(label='Program', choices=PROGRAMS, widget=forms.Select(attrs={'class': 'form-input'}))
