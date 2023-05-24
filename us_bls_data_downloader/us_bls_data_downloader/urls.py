"""
URL configuration for us_bls_data_downloader project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from us_bls_data_downloader_app import views

urlpatterns = [
    path('', views.registration_api_key_view, name='base'),
    path('index/', views.us_bls_index_view, name='index'),
    path('cpi/', views.cpi_series_id_components_view, name='cpi'),
    path('cpi_area/', views.cpi_series_id_components_area_view, name='cpi_area'),
    path('cpi_item/', views.cpi_series_id_components_item_view, name='cpi_item'),
    path('ppi/', views.ppi_series_id_components_view, name='ppi'),
    path('ppi_industry/', views.ppi_series_id_components_industry_view, name='ppi_industry'),
    path('ppi_product/', views.ppi_series_id_components_product_view, name='ppi_product'),
    path('out/', views.output_view, name='out'),
    path('admin/', admin.site.urls),
]
