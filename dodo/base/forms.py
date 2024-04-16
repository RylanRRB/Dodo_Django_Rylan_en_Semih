from django import forms
from .models import Profile

class NameForm(forms.Form):
    your_name = forms.CharField(label='Your name', max_length=100)

class UserForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ("grade", "city", "date_of_birth")
        widgets = {
            "date_of_birth": forms.DateInput(attrs={"type": "date"})
        }