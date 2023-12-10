from django import forms
from .models import announcements
from django.contrib.auth.models import User

class CreateGroupForm(forms.Form):
    group_name = forms.CharField(max_length=255, label='Group Name')
    members = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label='Select Members for the Group'
    )

class announcement_form(forms.ModelForm):

    class Meta:
        model=announcements
        fields=['title', 'description']


