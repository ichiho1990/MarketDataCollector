from django.db import models
from marketdatacollector import enums


# Create your models here.
class USBLSDataName(models.Model):

    # US_BLS_DATA_CHOICES = ((data.name, data.value) for data in enums.USBLSSeriesIDIndicator)
#
    # data_name = models.CharField(max_length=100, choices=US_BLS_DATA_CHOICES, default=enums.USBLSSeriesIDIndicator.CU.name)
    api_key = models.CharField(max_length=256)
    data_category = models.CharField(max_length=3)
    seasonal_adjustment = models.CharField(max_length=2)
    periodicity = models.CharField(max_length=2)
    area = models.CharField(max_length=10)
    item = models.CharField(max_length=256)
    industry = models.CharField(max_length=10)
    product = models.CharField(max_length=256)
    start = models.CharField(max_length=4)
    end = models.CharField(max_length=4)

    def __str__(self):
        return self.data_category

    # class Meta:
    #     db_table = 'USBLSDataName'
