from django.db import models
from django.utils import timezone


class RegistrationAPIKeys(models.Model):

    api_key = models.CharField(max_length=256)

    def __str__(self):
        return self.api_key


class USBLSDownloadedData(models.Model):

    series_title = models.CharField(max_length=256)
    date = models.CharField(max_length=256)
    value = models.CharField(max_length=256)
    month_pct_changes = models.CharField(max_length=256)
    quarter_pct_changes = models.CharField(max_length=256)
    semi_annual_pct_changes = models.CharField(max_length=256)
    annual_pct_changes = models.CharField(max_length=256)
    footnotes = models.CharField(max_length=256, default='na')

    def __str__(self):

        return self.series_title

class CPISeriesIDComponents(models.Model):

    api_key = models.ForeignKey(RegistrationAPIKeys, on_delete=models.CASCADE)
    seasonal = models.CharField(max_length=1, default='S')
    period = models.CharField(max_length=1, default='R')
    area = models.CharField(max_length=10, default='0000')
    item = models.CharField(max_length=256, default='SA0E')
    start = models.CharField(max_length=4)
    end = models.CharField(max_length=4)

    def __str__(self):

        return self.api_key


class CPISeriesIDAreaComponentsTable(models.Model):

    # api_key = models.ForeignKey(RegistrationAPIKeys, on_delete=models.CASCADE)
    created_date = models.DateField(default=timezone.now)
    area_code = models.CharField(max_length=256)
    area_name = models.CharField(max_length=256)
    display_level = models.CharField(max_length=256)
    selectable = models.CharField(max_length=256)
    sort_sequence = models.CharField(max_length=256)

    def __str__(self):
        return str(self.created_date)


class CPISeriesIDItemComponentsTable(models.Model):

    # api_key = models.ForeignKey(RegistrationAPIKeys, on_delete=models.CASCADE)
    created_date = models.DateField(default=timezone.now)
    item_code = models.CharField(max_length=256)
    item_name = models.CharField(max_length=256)
    display_level = models.CharField(max_length=256)
    selectable = models.CharField(max_length=256)
    sort_sequence = models.CharField(max_length=256)

    def __str__(self):
        return str(self.created_date)


class PPISeriesIDComponents(models.Model):

    api_key = models.ForeignKey(RegistrationAPIKeys, on_delete=models.CASCADE)
    seasonal = models.CharField(max_length=1, default='U')
    industry = models.CharField(max_length=10, default='211111')
    product = models.CharField(max_length=256, default='211111P')
    start = models.CharField(max_length=4)
    end = models.CharField(max_length=4)

    def __str__(self):

        return self.api_key


class PPISeriesIDIndustryComponentsTable(models.Model):

    # api_key = models.ForeignKey(RegistrationAPIKeys, on_delete=models.CASCADE)
    created_date = models.DateField(default=timezone.now)
    industry_code = models.CharField(max_length=256)
    industry_name = models.CharField(max_length=256)

    def __str__(self):
        return str(self.created_date)


class PPISeriesIDProductComponentsTable(models.Model):

    # api_key = models.ForeignKey(RegistrationAPIKeys, on_delete=models.CASCADE)
    created_date = models.DateField(default=timezone.now)
    industry_code = models.CharField(max_length=256)
    product_code = models.CharField(max_length=256)
    product_name = models.CharField(max_length=256)

    def __str__(self):
        return str(self.created_date)
