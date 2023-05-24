from django.contrib import admin
from us_bls_data_downloader_app.models import *

admin.site.register(RegistrationAPIKeys)
admin.site.register(USBLSDownloadedData)
admin.site.register(CPISeriesIDComponents)
admin.site.register(CPISeriesIDAreaComponentsTable)
admin.site.register(CPISeriesIDItemComponentsTable)
admin.site.register(PPISeriesIDComponents)
admin.site.register(PPISeriesIDIndustryComponentsTable)
admin.site.register(PPISeriesIDProductComponentsTable)

