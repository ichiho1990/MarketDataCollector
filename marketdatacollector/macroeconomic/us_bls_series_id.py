from typing import List, Union
from marketdatacollector import enums, utils
from abc import ABC, abstractmethod


class USBLSSeriesID(ABC):

    def __init__(self):
        self.indicator = ''
        self.mapping_components_name = []
        self.mapping_table = {}

    @abstractmethod
    def get_default_id_components(self):
        pass

    @abstractmethod
    def view_id_components(self):
        pass

    @abstractmethod
    def get_series_id_format(self, code_list):
        pass

    @abstractmethod
    def generate_series_id_components(self, **kwargs):
        pass

    @staticmethod
    def get_us_bls_series_id_mapping_table(indicator: str,
                                           mapping_components: Union[List, str]) -> dict:

        if isinstance(mapping_components, str):
            mapping_components = [mapping_components]

        url_dict = {component: utils.get_bls_series_id_component_url(indicator=indicator,
                                                                     component=component) for component in mapping_components}

        mapping_table_dict = {component: utils.get_bls_series_id_component_mapping_table(url_dict[component]) for component in url_dict}

        return mapping_table_dict


class USBLSSeriesIdCPI(USBLSSeriesID):

    def __init__(self):
        super(self.__class__, self).__init__()

        self.indicator = enums.USBLSSeriesIDIndicator.CU.name.lower()
        self.mapping_components_name = [enums.USBLSSeriesIdCPIComponents.AREA.value,
                                        enums.USBLSSeriesIdCPIComponents.ITEM.value]

        self.mapping_table = self.get_us_bls_series_id_mapping_table(self.indicator, self.mapping_components_name)

        self.id_components = self.get_default_id_components()

    def get_default_id_components(self):

        area_mapping_table = self.mapping_table[
            enums.USBLSSeriesIdCPIComponents.AREA.value]

        area_code = area_mapping_table.loc[area_mapping_table['area_name'] == 'U.S. city average', 'area_code'].values[0]

        id_components = {enums.USBLSSeriesIdCPIComponents.PREFIX.value: enums.USBLSSeriesIDIndicator.CU.name,
                         enums.USBLSSeriesIdCPIComponents.SEASONAL.value: enums.USBLSSeriesIdSeasonallyAdjustedCode.S.name,
                         enums.USBLSSeriesIdCPIComponents.PERIOD.value: enums.USBLSSeriesIdPeriodCode.R.name,
                         enums.USBLSSeriesIdCPIComponents.AREA.value: area_code,
                         enums.USBLSSeriesIdCPIComponents.ITEM.value: ''
                         }

        return id_components

    def view_id_components(self):

        for component in self.id_components:

            print(f'component name: "{component}", current value: "{self.id_components[component]}"')

            if component in self.mapping_components_name:
                print(
                    f'code name of component "{component}" can be found by using get_us_bls_series_id_mapping_table method')

    def generate_series_id_components(self,
                                      **kwargs):

        for i in kwargs:
            self.id_components[i] = kwargs[i]

    def get_series_id_format(self,
                             code_list: Union[List, str] = None):

        if isinstance(code_list, str):
            code_list = [code_list]

        if not code_list:
            item_mapping_table = self.mapping_table[enums.USBLSSeriesIdCPIComponents.ITEM.value]

            code_list = item_mapping_table.loc[item_mapping_table['item_name'] == 'All items', 'item_code'].tolist()

        series_id = [self.id_components[component] for component in self.id_components]

        series_id_list = [''.join(series_id) + code for code in code_list]

        return series_id_list


class USBLSSeriesIdPPI(USBLSSeriesID):

    def __init__(self):
        super(self.__class__, self).__init__()

        self.indicator = enums.USBLSSeriesIDIndicator.PC.name.lower()
        self.mapping_components_name = [enums.USBLSSeriesIdPPIComponents.INDUSTRY.value,
                                        enums.USBLSSeriesIdPPIComponents.PRODUCT.value]

        self.mapping_table = self.get_us_bls_series_id_mapping_table(self.indicator, self.mapping_components_name)

        self.id_components = self.get_default_id_components()

    def get_default_id_components(self):

        industry_mapping_table = self.mapping_table[
            enums.USBLSSeriesIdPPIComponents.INDUSTRY.value]

        industry_code = industry_mapping_table.loc[industry_mapping_table['industry_name'] == 'Crude petroleum and natural gas extraction', 'industry_code'].values[0]

        id_components = {enums.USBLSSeriesIdPPIComponents.PREFIX.value: enums.USBLSSeriesIDIndicator.PC.name,
                         enums.USBLSSeriesIdPPIComponents.SEASONAL.value: enums.USBLSSeriesIdSeasonallyAdjustedCode.S.name,
                         enums.USBLSSeriesIdPPIComponents.INDUSTRY.value: industry_code,
                         enums.USBLSSeriesIdPPIComponents.PRODUCT.value: ''
                         }

        return id_components

    def view_id_components(self):

        for component in self.id_components:

            print(f'component name: "{component}", current value: "{self.id_components[component]}"')

            if component in self.mapping_components_name:
                print(
                    f'code name of component "{component}" can be found by using get_us_bls_series_id_mapping_table method')

    def generate_series_id_components(self,
                                      **kwargs):

        for i in kwargs:
            self.id_components[i] = kwargs[i]

    def get_series_id_format(self,
                             code_list: Union[List, str] = None):

        if isinstance(code_list, str):
            code_list = [code_list]

        if not code_list:
            product_mapping_table = self.mapping_table[enums.USBLSSeriesIdPPIComponents.PRODUCT.value]

            code_list = product_mapping_table.loc[product_mapping_table['product_name'] == 'Primary products', 'product_code'].tolist()

        series_id = [self.id_components[component] for component in self.id_components]

        series_id_list = [''.join(series_id) + code for code in code_list]

        return series_id_list

