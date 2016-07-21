from django import forms

from teams.models import TeamProfile, TeamCheer


class TeamProfileForm(forms.ModelForm):
    class Meta:
        model = TeamProfile
        fields = ['welcome_message', 'description', 'team_video']

    team_video = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-input'}), required=False)
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-textarea'}), required=False)
    welcome_message = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-textarea'}), required=False)

class TeamCheerForm(forms.ModelForm):
    class Meta:
        model = TeamCheer
        fields = ['name', 'text']

    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-input'}))
    text = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-textarea'}))
