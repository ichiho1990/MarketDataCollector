from django import forms
from us_bls_data_downloader_app import models


class FormInputName(forms.Form):
    api_key = forms.CharField()
    data_category = forms.CharField(max_length=3)
    seasonal_adjustment = forms.CharField(max_length=1)
    periodicity = forms.CharField(max_length=1)
    area = forms.CharField(max_length=10)
    item = forms.CharField(max_length=256)
    industry = forms.CharField(max_length=10)
    product = forms.CharField(max_length=256)
    start = forms.CharField(max_length=4)
    end = forms.CharField(max_length=4)


class APIKeysForm(forms.ModelForm):

    class Meta:
        model = models.RegistrationAPIKeys
        fields = ('api_key',)


class CPISeriesIDComponentsForm(forms.ModelForm):

    class Meta:
        model = models.CPISeriesIDComponents

        fields = ('api_key', 'seasonal', 'period', 'area', 'item', 'start', 'end')


class PPISeriesIDComponentsForm(forms.ModelForm):

    class Meta:
        model = models.PPISeriesIDComponents

        fields = ('api_key', 'seasonal', 'industry', 'product', 'start', 'end')


