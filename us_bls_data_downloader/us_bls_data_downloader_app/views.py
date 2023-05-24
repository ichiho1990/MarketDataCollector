from django.shortcuts import render, redirect
from django.views.generic import CreateView, UpdateView, TemplateView, View, ListView, DetailView
from django.urls import reverse_lazy
from django.http import response
import pandas as pd
import pickle
from us_bls_data_downloader_app import forms, models
from marketdatacollector import enums
from marketdatacollector.macroeconomic.USBureauOfLaborStatisticsData import us_bls_data_downloader


def registration_api_key_view(request):
    form = forms.APIKeysForm()

    if request.method == 'POST':
        form = forms.APIKeysForm(request.POST)
        if form.is_valid():
            form.save(commit=True)

            return redirect('/index/')

        else:
            print('ERROR FORM INVALID')

    return render(request, 'base.html', {'form': form})


def us_bls_index_view(request):

    return render(request, 'index.html')


def cpi_series_id_components_view(request):
    form = forms.CPISeriesIDComponentsForm()

    model = models.USBLSDownloadedData

    if request.method == 'POST':
        # registration_key = request.POST.get('id_api_key')
        form = forms.CPISeriesIDComponentsForm(request.POST)

        if form.is_valid():
            form.save(commit=True)

            try:

                downloader = us_bls_data_downloader.USBLSCPIDownloader(registration_key=form.cleaned_data['api_key'].api_key)

                components = {enums.USBLSSeriesIdCPIComponents.SEASONAL.value: form.cleaned_data['seasonal'],
                              enums.USBLSSeriesIdCPIComponents.PERIOD.value: form.cleaned_data['period'],
                              enums.USBLSSeriesIdCPIComponents.AREA.value: form.cleaned_data['area'],
                              enums.USBLSSeriesIdCPIComponents.ITEM.value: form.cleaned_data['item'],}

                downloader.specify_data_indicator(components)

                downloader.get_bls_data(start_year=form.cleaned_data['start'], end_year=form.cleaned_data['end'])

                downloaded_data = downloader.format_bls_data()

                for o in downloaded_data:

                    data = o['data']
                    series_title = o['series_title']

                    for d in data:
                        d['series_title'] = series_title

                    model.objects.bulk_create(
                    model(**vals) for vals in pd.DataFrame(data).to_dict('records')
                    )

                # date_dict = {'assess_records': model.objects.order_by('series_title')}

                print(f'key: {pd.DataFrame(data)}')
                print(data)

                with open('out_data.pkl', 'wb') as f:
                    pickle.dump(downloaded_data, f)

                # After the operation was successful,
                # redirect to some other page
                return redirect('/out/')  # 4

            except Exception as e:
                print(e)
                print(form.cleaned_data['api_key'].api_key)


        else:
            print('ERROR FORM INVALID')

    return render(request, 'cpi_series_id_components.html', {'form': form})


def cpi_series_id_components_area_view(request):

    downloader = us_bls_data_downloader.USBLSCPIDownloader()

    mapping_table = downloader.get_mapping_components_table('area')

    model = models.CPISeriesIDAreaComponentsTable

    model.objects.bulk_create(
        model(**vals) for vals in mapping_table.to_dict('records')
    )

    date_dict = {'cpi_area_table': model.objects.order_by('created_date')}

    return render(request, 'cpi_area_mapping_table.html', context=date_dict)


def cpi_series_id_components_item_view(request):

    downloader = us_bls_data_downloader.USBLSCPIDownloader()

    mapping_table = downloader.get_mapping_components_table('item')

    model = models.CPISeriesIDItemComponentsTable

    model.objects.bulk_create(
        model(**vals) for vals in mapping_table.to_dict('records')
    )

    date_dict = {'cpi_item_table': model.objects.order_by('created_date')}

    return render(request, 'cpi_item_mapping_table.html', context=date_dict)


def ppi_series_id_components_view(request):
    form = forms.PPISeriesIDComponentsForm()

    model = models.USBLSDownloadedData

    if request.method == 'POST':
        # registration_key = request.POST.get('id_api_key')
        form = forms.PPISeriesIDComponentsForm(request.POST)

        if form.is_valid():
            form.save(commit=True)

            try:

                downloader = us_bls_data_downloader.USBLSPPIDownloader(registration_key=form.cleaned_data['api_key'].api_key)

                components = {enums.USBLSSeriesIdPPIComponents.SEASONAL.value: form.cleaned_data['seasonal'],
                              enums.USBLSSeriesIdPPIComponents.INDUSTRY.value: form.cleaned_data['industry'],
                              enums.USBLSSeriesIdPPIComponents.PRODUCT.value: form.cleaned_data['product'],}

                downloader.specify_data_indicator(components)

                downloader.get_bls_data(start_year=form.cleaned_data['start'], end_year=form.cleaned_data['end'])

                downloaded_data = downloader.format_bls_data()

                for o in downloaded_data:

                    data = o['data']
                    series_title = o['series_title']

                    for d in data:
                        d['series_title'] = series_title

                    model.objects.bulk_create(
                    model(**vals) for vals in pd.DataFrame(data).to_dict('records')
                    )

                # date_dict = {'assess_records': model.objects.order_by('series_title')}

                print(f'key: {pd.DataFrame(data)}')
                print(data)

                with open('out_data.pkl', 'wb') as f:
                    pickle.dump(downloaded_data, f)

                # After the operation was successful,
                # redirect to some other page
                return redirect('/out/')  # 4

            except Exception as e:
                print(e)
                print(form.cleaned_data['api_key'].api_key)


        else:
            print('ERROR FORM INVALID')

    return render(request, 'ppi_series_id_components.html', {'form': form})


def ppi_series_id_components_industry_view(request):

    downloader = us_bls_data_downloader.USBLSPPIDownloader()

    mapping_table = downloader.get_mapping_components_table('industry')

    model = models.PPISeriesIDIndustryComponentsTable

    model.objects.bulk_create(
        model(**vals) for vals in mapping_table.to_dict('records')
    )

    date_dict = {'ppi_industry_table': model.objects.order_by('created_date')}

    return render(request, 'ppi_industry_mapping_table.html', context=date_dict)


def ppi_series_id_components_product_view(request):

    downloader = us_bls_data_downloader.USBLSPPIDownloader()

    mapping_table = downloader.get_mapping_components_table('product')

    model = models.PPISeriesIDProductComponentsTable

    model.objects.bulk_create(
        model(**vals) for vals in mapping_table.to_dict('records')
    )

    date_dict = {'ppi_product_table': model.objects.order_by('created_date')}

    return render(request, 'ppi_product_mapping_table.html', context=date_dict)


def output_view(request):

    model = models.USBLSDownloadedData

    date_dict = {'downloaded_data': model.objects.order_by('series_title')}

    return render(request, 'out_put.html', context=date_dict)