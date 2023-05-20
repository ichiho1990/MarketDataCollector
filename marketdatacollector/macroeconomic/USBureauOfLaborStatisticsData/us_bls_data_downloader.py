import json
import calendar
import datetime
from abc import ABC, abstractmethod
import requests
import pandas as pd
from marketdatacollector import enums
from marketdatacollector.macroeconomic.USBureauOfLaborStatisticsData import us_bls_series_id_generator


class USBLSDataDownloader(ABC):
    """
    Abstract class for downloading US Bureau of Labor Statistics indicator data based on the given series id
    """

    def __init__(self,
                 registration_key: str):
        """create the constructor based on the given registration_key

        Args:
            registration_key: string of registration_key.
            Can be obtained from https://data.bls.gov/registrationEngine/
        """

        self.registration_key = registration_key
        self.series_id_list = None
        self.output_data = None
        self.product = self.get_us_bls_indicator()

    @abstractmethod
    def get_us_bls_indicator(self) -> us_bls_series_id_generator.USBLSSeriesID:
        """method to get the parent class of the chosen indicator

        Returns: USBLSSeriesID child class

        """

    def print_components(self):
        """ Method to present the current values of each component.

        """
        self.product.view_id_components()

    def get_mapping_components_table(self, mapping_component_name: str) -> pd.DataFrame:
        """get mapping table dataframe to find the corresponding code of the series id to be generated
           based on the economic description

        Args:
            mapping_component_name: string of mapping_component_name

        Returns: mapping_table (pd.DataFrame): a dataframe with rows of possible series code and the description for the code

        """

        return self.product.mapping_table[mapping_component_name]

    def specify_data_indicator(self, indicator: dict):
        """generate and format series id components based on the input dictionary

        Args:
            indicator (dict): dictionary with keys of component name and values of the
                             series id code for the series id.

        """

        self.product.generate_series_id_components(**indicator)

        self.series_id_list = self.product.get_series_id_format()

    def get_bls_data(self,
                     start_year: str,
                     end_year: str,
                     calculations: bool = True,
                     catalog: bool = True,
                     aspects: bool = False,
                     annual_average: bool = False
                     ):
        """Download bls data

        Args:
            start_year (str): string of start year from which the data to be downloaded
            end_year (str): string of end year until which the data to be downloaded
            calculations (bool): specify whether percentage changes are calculated. Default to True
            catalog (bool): specify whether catalog is downloaded. Default to True
            aspects (bool): specify whether aspects is downloaded. Default to False
            annual_average (bool): specify whether annual_average is downloaded. Default to False

        """

        headers = {'Content-type': 'application/json'}

        data = json.dumps(
            {"seriesid": self.series_id_list,
             "startyear": start_year,
             "endyear": end_year,
             'calculations': calculations,
             "aspects": aspects,
             'registrationkey': self.registration_key,
             "catalog": catalog,
             "annualaverage": annual_average}
        )

        post = requests.post('https://api.bls.gov/publicAPI/v2/timeseries/data/', data=data, headers=headers, timeout=2)

        if post.status_code == 200:
            json_data = json.loads(post.text)

            self.output_data = json_data['Results']['series']

    def format_bls_data(self) -> list:
        """Format the raw data downloaded from BLS

        Returns: output_data_list (list): list of dictionary with keys of data title and values of data

        """

        output_data_list = []

        bls_cpi_data_series = [series for series in self.output_data if
                               bool(series[enums.USBLSDownloadedDataGeneralTitle.DATA.value])]

        for series in bls_cpi_data_series:

            out_dict = {catalog_item[0]: catalog_item[1] for
                        catalog_item in series[enums.USBLSDownloadedDataGeneralTitle.CATALOG.value].items()}

            data = {}

            date = [datetime.date(year=int(raw_series_data[enums.USBLSDownloadedDataTitle.YEAR.value]),
                                  month=int(raw_series_data[enums.USBLSDownloadedDataTitle.PERIOD.value][1:]),
                                  day=calendar.monthrange(int(raw_series_data[enums.USBLSDownloadedDataTitle.YEAR.value]),
                                                          int(raw_series_data[enums.USBLSDownloadedDataTitle.PERIOD.value][1:]))[1]) for
                    raw_series_data in series[enums.USBLSDownloadedDataGeneralTitle.DATA.value]]

            value = [float(raw_series_data[enums.USBLSDownloadedDataTitle.VALUE.value]) for raw_series_data in
                     series[enums.USBLSDownloadedDataGeneralTitle.DATA.value]]

            pct_changes = [raw_series_data[enums.USBLSDownloadedDataTitle.CALCULATIONS.value][
                               enums.USBLSDownloadedDataCalculationsTitle.PCT_CHANGES.value] for raw_series_data in
                           series[enums.USBLSDownloadedDataGeneralTitle.DATA.value] if
                           enums.USBLSDownloadedDataTitle.CALCULATIONS.value in raw_series_data.keys()]

            rename_columns = {title.value: title.name.lower() for title in
                              enums.USBLSDownloadedDataCalculationsPctChangesTitle}

            pct_changes_dict = pd.DataFrame(pct_changes).rename(columns=rename_columns).to_dict('List')

            data['date'] = date
            data['value'] = value
            data.update(pct_changes_dict)

            footnotes_list = []

            for raw_series_data in series[enums.USBLSDownloadedDataGeneralTitle.DATA.value]:

                footnotes = ""

                for footnote in raw_series_data[enums.USBLSDownloadedDataTitle.FOOTNOTES.value]:
                    if footnote:
                        footnotes = footnotes + footnote['text']

                footnotes_list.append(footnotes)

            data[enums.USBLSDownloadedDataTitle.FOOTNOTES.value] = footnotes_list

            out_dict[enums.USBLSDownloadedDataGeneralTitle.DATA.value] = pd.DataFrame(data).to_dict('records')

            output_data_list.append(out_dict)

        return output_data_list


class USBLSCPIDownloader(USBLSDataDownloader):
    """Download US Bureau of Labor Statistics indicator data for
       Consumer Price Index - All Urban Consumers.

    """

    def __init__(self, registration_key):
        super().__init__(registration_key=registration_key)

    def get_us_bls_indicator(self) -> us_bls_series_id_generator.USBLSSeriesID:

        return us_bls_series_id_generator.USBLSSeriesIdCPI()


class USBLSPPIDownloader(USBLSDataDownloader):
    """Download US Bureau of Labor Statistics indicator data for
       Producer Price Index Industry Data.

    """

    def __init__(self, registration_key):
        super().__init__(registration_key=registration_key)

    def get_us_bls_indicator(self) -> us_bls_series_id_generator.USBLSSeriesID:

        return us_bls_series_id_generator.USBLSSeriesIdPPI()
