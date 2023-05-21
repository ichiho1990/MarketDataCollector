from django.shortcuts import render, redirect
from django.views.generic import CreateView, UpdateView, TemplateView, View, ListView, DetailView
from django.urls import reverse_lazy
import pandas as pd
import pickle
from us_bls_data_downloader_app import forms, models
from marketdatacollector import enums
from marketdatacollector.macroeconomic.USBureauOfLaborStatisticsData import us_bls_data_downloader

# Create your views here.

def input_form_view(request):
    form = forms.FormInputName()

    if request.method == 'POST':
        form = forms.FormInputName(request.POST)

        if form.is_valid():
            api_key = form.cleaned_data['api_key']
            data_category = form.cleaned_data['data_category']

            if data_category.upper() == 'CPI':
                downloader = us_bls_data_downloader.USBLSCPIDownloader(api_key)
                data_indicator_components = ['seasonal_adjustment', 'periodicity', 'area', 'item']
                data_indicator_components_dict = {component: form.cleaned_data[component] for component in
                                                  data_indicator_components}
                data_indicator_components_dict['item'] = data_indicator_components_dict['item'].split(',')
            elif data_category.upper() == 'PPI':
                downloader = us_bls_data_downloader.USBLSPPIDownloader(api_key)
                data_indicator_components = ['seasonal_adjustment', 'industry', 'product']
                data_indicator_components_dict = {component: form.cleaned_data[component] for component in
                                                  data_indicator_components}
                data_indicator_components_dict['product'] = data_indicator_components_dict['product'].split(',')



            downloader.print_components()
            downloader.specify_data_indicator(data_indicator_components_dict)
            # define the data time series period and then download data

            downloader.get_bls_data(start_year = form.cleaned_data['start'], end_year = form.cleaned_data['end'])

            # format data and return output
            out = downloader.format_bls_data()
            for series in out:
                print(f'series {series["series_title"]}')
                print(pd.DataFrame(series['data']))

            with open('out_data.pkl', 'wb') as f:
                pickle.dump(out, f)

    return render(request, 'input_form.html', {'form': form})


class USBLSDataNameListView(ListView):
    model = models.USBLSDataName
    context_object_name = 'data_name'


def showlist(request):
    results=models.USBLSDataName.objects.all
    return render(request, "data_name_form.html", {"showcity":results})
#
# def index(request):
#     return render(request, 'index.html')
#
# class IndexView(TemplateView):
#     template_name = "index.html"
#     # form = forms.FormInputName()
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['injectme'] = 'Basic'
#         return context
#
# class SchoolListView(ListView):
#     model = models.School
#
# class SchoolDetailView(DetailView):
#     model = models.School
#     template_name = "us_bls_data_downloader_app/school_detail.html"


def input_form_view_new(request):
    form = forms.FormInputName()

    input_data_attribute_list = [item for item in models.USBLSDataName().__dict__]

    if request.method == 'POST':
        form = forms.FormInputName(request.POST)
        input_api_key = request.POST.get('input_api_key')
        input_data_category = request.POST.get('input_data_category')
        input_start = request.POST.get('input_start')
        input_end = request.POST.get('input_end')
        input_seasonal_adjustment = request.POST.get('input_seasonal_adjustment')
        input_periodicity = request.POST.get('input_periodicity')
        input_area = request.POST.get('input_area')
        input_item = request.POST.get('input_item')
        input_industry = request.POST.get('input_industry')
        input_product = request.POST.get('input_product')

        if input_seasonal_adjustment:
            print('save seasonal adjustment')
            usblsmodel = models.USBLSDataName()
            for item in usblsmodel.__dict__:
                input_name = 'input_' + item

                usblsmodel.__setattr__(item, request.POST.get(input_name))

            usblsmodel.save()
            return redirect('/success/')

        elif input_data_category.upper() == 'CPI':
            context = {'seasonal_adjustment': [code.name for code in enums.USBLSSeriesIdSeasonallyAdjustedCode],
                       'period': [code.name for code in enums.USBLSSeriesIdPeriodCode]}

            for attribute in input_data_attribute_list:
                if not attribute in context.keys():
                    key = 'input_' + attribute
                    context[key] = request.POST.get(key)

            return render(request, 'input_form_new.html', context)


        elif input_data_category.upper() == 'PPI':
            context = {'seasonal_adjustment': [code.name for code in enums.USBLSSeriesIdSeasonallyAdjustedCode],
                       'period': 'NA'}

            for attribute in input_data_attribute_list:
                if not attribute in context.keys():
                    key = 'input_' + attribute
                    context[key] = request.POST.get(key)

            return render(request, 'input_form_new.html', context)



