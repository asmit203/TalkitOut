from django import forms
from .models import announcements

class announcement_form(forms.ModelForm):

    class Meta:
        model=announcements
        fields=['title', 'description']


