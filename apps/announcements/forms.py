import django.forms as forms

from apps.announcements.models import Announcement


class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ['title', 'text']

    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-input'}), required=True)
    text = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-textarea'}), required=True)
