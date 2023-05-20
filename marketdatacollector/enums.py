from enum import Enum, IntEnum


class USBLSSeriesIDIndicator(Enum):
    CU = 'Consumer Price Index - All Urban Consumers'
    PC = 'Producer Price Index Industry Data'


class USBLSSeriesIdCPIComponents(Enum):
    PREFIX = 'prefix'
    SEASONAL = 'seasonal_adjustment'
    PERIOD = 'periodicity'
    AREA = 'area'
    ITEM = 'item'


class USBLSSeriesIdPPIComponents(Enum):
    PREFIX = 'prefix'
    SEASONAL = 'seasonal_adjustment'
    INDUSTRY = 'industry'
    PRODUCT = 'product'


class USBLSDownloadedDataGeneralTitle(Enum):
    SERIES = 'seriesID'
    CATALOG = 'catalog'
    DATA = 'data'


class USBLSDownloadedCatalogTitle(Enum):
    TITLE = 'series_title'
    ID = 'series_id'
    SEASONALITY = 'seasonality'
    SURVEY_NAME = 'survey_name'
    SURVEY_ABB = 'survey_abbreviation'
    MEASURE_DATA_TYPE = 'measure_data_type'
    AREA = 'area'
    ITEM = 'item'


class USBLSDownloadedDataTitle(Enum):
    YEAR = "year"
    PERIOD = "period"
    PERIOD_NAME = "periodName"
    VALUE = "value"
    FOOTNOTES = "footnotes"
    CALCULATIONS = "calculations"


class USBLSDownloadedDataCalculationsTitle(Enum):
    NET_CHANGES = "net_changes"
    PCT_CHANGES = "pct_changes"


class USBLSDownloadedDataCalculationsPctChangesTitle(Enum):
    MONTH_PCT_CHANGES = '1'
    QUARTER_PCT_CHANGES = '3'
    SEMI_ANNUAL_PCT_CHANGES = '6'
    ANNUAL_PCT_CHANGES = '12'


class USBLSSeriesIdPeriodCode(Enum):
    """
    frequency of observation
    """
    R = 'monthly'
    S = 'semi-annual'


class USBLSSeriesIdSeasonallyAdjustedCode(Enum):
    """
    adjustment of data to eliminate the effect of intra-year variations
    """
    U = 'Unadjusted'
    S = 'Seasonally Adjusted'






