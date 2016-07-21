from django import forms


form_controls = {
    'class': 'form-input'
}


class SubmissionForm(forms.Form):
    artist_name = forms.CharField(label='Artist Name', max_length=100,
        widget=forms.TextInput(attrs=form_controls))
    song_name = forms.CharField(label='Song Name', max_length=100,
        widget=forms.TextInput(attrs=form_controls))

    def __init__(self, *args, **kwargs):
        super(SubmissionForm, self).__init__(*args, **kwargs)
        for field in ['artist_name', 'song_name']:
            self.fields[field].widget.attrs['style'] = 'margin-bottom: 25px;'
