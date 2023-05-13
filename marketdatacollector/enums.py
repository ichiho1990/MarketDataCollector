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






