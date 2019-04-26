from django import forms
import urllib


class SearchForm(forms.Form):
    search_text = forms.CharField(label='', max_length=100, show_hidden_initial=False)

    def as_url_args(self):
        return urllib.parse.urlencode(self.cleaned_data)
