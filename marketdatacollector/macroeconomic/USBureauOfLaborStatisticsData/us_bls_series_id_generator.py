from typing import Union
from abc import ABC, abstractmethod
from marketdatacollector import enums, utils


class USBLSSeriesID(ABC):
    """
    Abstract class for generating US Bureau of Labor Statistics indicator series id
    """

    def __init__(self):
        self.indicator = ''
        self.mapping_components_name = []
        self.mapping_table = {}
        self.id_components = {}

    @abstractmethod
    def get_default_id_components(self) -> dict:
        """get default id components that the series id consists with.

        Returns: dictionary with keys of component names and values of default series id for
                            the corresponding component.

        """

    @abstractmethod
    def get_series_id_format(self) -> list:
        """Generate series id of the indicator to be downloaded with for each of the items in
           the code list

        Returns:
            series_id_list (list): list of series ids each is the combination of the same values
                                   of the other components and each of items in list of the values
                                   for the last component.

        """

    def view_id_components(self):
        """ Method to present the current values of each component.

        """
        for component_item in self.id_components.items():

            print(f'component name: "{component_item[0]}", '
                  f'current value: "{component_item[1]}"')

            if component_item[0] in self.mapping_components_name:
                print(
                    f'code name of component "{component_item[0]}" '
                    f'can be found by using get_us_bls_series_id_mapping_table method')

    def generate_series_id_components(self,
                                      **kwargs: dict):
        """generate series id components based on the input dictionary

        Args:
            **kwargs (dict): dictionary with keys of component name and values of the
                             series id code for the series id.

        Returns:

        """

        for component_item in kwargs.items():
            self.id_components[component_item[0]] = component_item[1]

    @staticmethod
    def get_us_bls_series_id_mapping_table(indicator: str,
                                           mapping_components: Union[list, str]) -> dict:
        """get mapping table to find the corresponding code of the series id to be generated
           based on the economic description

        Args:
            indicator (str): string of the indicator symbol.
                             For example, Consumer Price Index - All Urban Consumers is 'CU'
            mapping_components (Union[list, str]): string or list of string, each string is the name of
                                                   the component that the mapping table is generated for.

        Returns:
            mapping_table (dict): dictionary with keys of component name and values of a dataframe
                                  with rows of possible series code and the description for the code

        """

        if isinstance(mapping_components, str):
            mapping_components = [mapping_components]

        url_dict = {component: utils.get_bls_series_id_component_url(indicator=indicator,
                                                                     component=component) for component in
                    mapping_components}

        mapping_table_dict = {component: utils.get_bls_series_id_component_mapping_table(url_dict[component]) for
                              component in url_dict}

        return mapping_table_dict


class USBLSSeriesIdCPI(USBLSSeriesID):
    """Generate US Bureau of Labor Statistics indicator series id for
       Consumer Price Index - All Urban Consumers.

       The series id consists with:
       1. Prefix:
          'CU' is the prefix of Consumer Price Index - All Urban Consumers
       2. Seasonal Adjustment Code:
          details can be found in USBLSSeriesIdSeasonallyAdjustedCode in enums.py
       3. Periodicity Code:
          details can be found in USBLSSeriesIdPeriodCode in enums.py
       4. Area Code:
          Indicates the area for which indexes are available.
       6. Item Code:
          Indicates the commodity, service, or special grouping for which indexes are available.

       Further details can be found in https://www.bls.gov/help/def/cu.htm
    """

    def __init__(self):
        super().__init__()

        self.indicator = enums.USBLSSeriesIDIndicator.CU.name.lower()
        self.mapping_components_name = [enums.USBLSSeriesIdCPIComponents.AREA.value,
                                        enums.USBLSSeriesIdCPIComponents.ITEM.value]

        self.mapping_table = self.get_us_bls_series_id_mapping_table(self.indicator, self.mapping_components_name)

        self.id_components = self.get_default_id_components()

    def get_default_id_components(self) -> dict:
        """get the default values for each id components that the series id of
           Consumer Price Index - All Urban Consumers consists with.
        1. Prefix is 'CU'
        2. Seasonal Adjustment Code is 'S', which is applying seasonal adjustment
        3. Periodicity Code is 'R', which is monthly
        4. Area Code is '0000', which is 'U.S. city average'
        5. Item Code is list of one item - 'SA0', which is 'All items'

        Returns: id_components (dict): dictionary with keys of component names and
                                       values of default series id for the corresponding component.

        """

        area_mapping_table = self.mapping_table[
            enums.USBLSSeriesIdCPIComponents.AREA.value]

        item_mapping_table = self.mapping_table[enums.USBLSSeriesIdCPIComponents.ITEM.value]

        area_code = area_mapping_table.loc[area_mapping_table['area_name'] == 'U.S. city average', 'area_code'].values[
            0]
        item_code_list = item_mapping_table.loc[item_mapping_table['item_name'] == 'All items', 'item_code'].tolist()

        id_components = {enums.USBLSSeriesIdCPIComponents.PREFIX.value: enums.USBLSSeriesIDIndicator.CU.name,
                         enums.USBLSSeriesIdCPIComponents.SEASONAL.value: enums.USBLSSeriesIdSeasonallyAdjustedCode.S.name,
                         enums.USBLSSeriesIdCPIComponents.PERIOD.value: enums.USBLSSeriesIdPeriodCode.R.name,
                         enums.USBLSSeriesIdCPIComponents.AREA.value: area_code,
                         enums.USBLSSeriesIdCPIComponents.ITEM.value: item_code_list
                         }

        return id_components

    def get_series_id_format(self) -> list:
        """Generate series id of the indicator to be downloaded with for each of the Item Code in
           the code list

        Returns:
            series_id_list (list): list of series ids each is the combination of the same values
                                   of the other components and each of items in code_list

        """

        series_id = [component_item[1] for component_item in self.id_components.items() if
                     component_item[0] != enums.USBLSSeriesIdCPIComponents.ITEM.value]

        series_id_list = [''.join(series_id) + code for code in
                          self.id_components[enums.USBLSSeriesIdCPIComponents.ITEM.value]]

        return series_id_list


class USBLSSeriesIdPPI(USBLSSeriesID):
    """Generate US Bureau of Labor Statistics indicator series id for Producer Price Index Industry Data.
       The series id consists with:
       1. Prefix:
          'PC' is the prefix of Producer Price Index Industry Data
       2. Seasonal Adjustment Code:
          details can be found in USBLSSeriesIdSeasonallyAdjustedCode in enums.py
       3. Industry Code:
          based on the North American Industry Classification System (NAICS)
       4. Product Code:
          numerical extensions to the industry codes.

       Further details can be found in https://www.bls.gov/help/def/pc.htm
    """

    def __init__(self):
        super().__init__()

        self.indicator = enums.USBLSSeriesIDIndicator.PC.name.lower()
        self.mapping_components_name = [enums.USBLSSeriesIdPPIComponents.INDUSTRY.value,
                                        enums.USBLSSeriesIdPPIComponents.PRODUCT.value]

        self.mapping_table = self.get_us_bls_series_id_mapping_table(self.indicator, self.mapping_components_name)

        self.id_components = self.get_default_id_components()

    def get_default_id_components(self) -> dict:
        """get the default values for each id components that the series id of
           Producer Price Index Industry Data consists with.
        1. Prefix is 'PC'
        2. Seasonal Adjustment Code is 'U', which is not applying seasonal adjustment
        3. Industry Code is '211111', which is 'Crude petroleum and natural gas extraction'
        4. Product Code is list of one item - '211111P', which is 'Primary products'

        Returns: id_components (dict): dictionary with keys of component names and
                                       values of default series id for the corresponding component.

        """

        industry_mapping_table = self.mapping_table[
            enums.USBLSSeriesIdPPIComponents.INDUSTRY.value]

        product_mapping_table = self.mapping_table[enums.USBLSSeriesIdPPIComponents.PRODUCT.value]

        industry_code = industry_mapping_table.loc[industry_mapping_table['industry_name'] == 'Crude petroleum and natural gas extraction', 'industry_code'].values[0]
        product_code_list = product_mapping_table.loc[
            (product_mapping_table['product_name'] == 'Primary products') & (product_mapping_table['industry_code'] == industry_code), 'product_code'].tolist()

        id_components = {enums.USBLSSeriesIdPPIComponents.PREFIX.value: enums.USBLSSeriesIDIndicator.PC.name,
                         enums.USBLSSeriesIdPPIComponents.SEASONAL.value: enums.USBLSSeriesIdSeasonallyAdjustedCode.U.name,
                         enums.USBLSSeriesIdPPIComponents.INDUSTRY.value: industry_code,
                         enums.USBLSSeriesIdPPIComponents.PRODUCT.value: product_code_list
                         }

        return id_components

    def get_series_id_format(self) -> list:
        """Generate series id of the indicator to be downloaded with for each of the Item Code in
           the code list

        Returns:
            series_id_list (list): list of series ids each is the combination of the same values
                                   of the other components and each of items in code_list

        """

        series_id = [component_item[1] for component_item in self.id_components.items() if
                     component_item[0] != enums.USBLSSeriesIdPPIComponents.PRODUCT.value]

        series_id_list = [''.join(series_id) + code for code in
                          self.id_components[enums.USBLSSeriesIdPPIComponents.PRODUCT.value]]

        return series_id_list
