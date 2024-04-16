from django import forms
from .models import Distance, Time

class NameForm(forms.Form):
    your_name = forms.CharField(label="Your name", max_length=100)

class DistanceForm(forms.ModelForm):
    class Meta:
        model=Distance
        fields=("length", "full_name")

class TimeForm(forms.ModelForm):
    class Meta:
        model = Time
        fields = ("distance", "time_in_minutes", "date")
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"})
        }