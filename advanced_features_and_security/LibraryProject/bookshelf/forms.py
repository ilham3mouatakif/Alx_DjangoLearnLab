from django import forms

class ExampleForm(forms.Form):
    search_query = forms.CharField(max_length=100, required=True)
