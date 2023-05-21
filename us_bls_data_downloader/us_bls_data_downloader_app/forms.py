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


class DataNameForm(forms.ModelForm):
    class Meta:
        model = models.USBLSDataName
        fields = ('data_category',)


