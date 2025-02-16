from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import SetPasswordForm

class UsernamePasswordResetForm(forms.Form):
    username = forms.CharField(max_length=150, required=True)

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not User.objects.filter(username=username).exists():
            raise forms.ValidationError("User does not exist.")
        return username
