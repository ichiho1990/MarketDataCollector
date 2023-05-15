import requests
import json
import calendar
import datetime
import numpy as np
import pandas as pd
from marketdatacollector.macroeconomic import us_bls_series_id as bls_id
from abc import ABC, abstractmethod


class USBLSDataDownloader(ABC):

    def __init__(self,
                 registration_key: str = None):

        self.registration_key = registration_key
        self.series_id_list = None
        self.output_data = None
        self.product = self.get_us_bls_indicator()

    @abstractmethod
    def get_us_bls_indicator(self) -> bls_id.USBLSSeriesID:

        pass

    def print_components(self):
        self.product.view_id_components()

    def get_mapping_components_table(self, mapping_component_name):

        return self.product.mapping_table[mapping_component_name]

    def specify_data_indicator(self, indicator, code_list=None):

        self.product.generate_series_id_components(**indicator)

        self.series_id_list = self.product.get_series_id_format(code_list)

        pass

    def get_bls_data(self,
                     start_year: str,
                     end_year: str,
                     calculations: bool = True,
                     catalog: bool = True,
                     aspects: bool = False,
                     annual_average: bool = False
                     ):

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

        post = requests.post('https://api.bls.gov/publicAPI/v2/timeseries/data/', data=data, headers=headers)

        if post.status_code == 200:
            json_data = json.loads(post.text)

            self.output_data = json_data['Results']['series']

    def format_bls_data(self):

        output_data_list = []

        bls_cpi_data_series = [series for series in self.output_data if bool(series['data'])]

        for series in bls_cpi_data_series:

            out_dict = {key: series['catalog'][key] for key in series['catalog']}

            series_data_list = []

            for raw_series_data in series['data']:
                data = {}

                year = int(raw_series_data['year'])
                month = int(raw_series_data['period'][1:])
                day = calendar.monthrange(year, month)[1]
                date = datetime.date(year, month, day)
                value = float(raw_series_data['value'])

                month_pct_chg = np.nan
                quarter_pct_chg = np.nan
                semi_annual_pct_chg = np.nan
                annual_pct_chg = np.nan

                if 'calculations' in raw_series_data.keys():
                    calculations = raw_series_data['calculations']
                    pct_changes = calculations['pct_changes']

                    if '1' in pct_changes.keys():
                        month_pct_chg = float(pct_changes['1'])
                    if '3' in pct_changes.keys():
                        quarter_pct_chg = float(pct_changes['3'])
                    if '6' in pct_changes.keys():
                        semi_annual_pct_chg = float(pct_changes['6'])
                    if '12' in pct_changes.keys():
                        annual_pct_chg = float(pct_changes['12'])

                footnotes = ""

                for footnote in raw_series_data['footnotes']:
                    if footnote:
                        footnotes = footnotes + footnote['text']

                data['date'] = date
                data['value'] = value
                data['month_pct_chg'] = month_pct_chg
                data['quarter_pct_chg'] = quarter_pct_chg
                data['semi_annual_pct_chg'] = semi_annual_pct_chg
                data['annual_pct_chg'] = annual_pct_chg
                data['footnotes'] = footnotes

                series_data_list.append(data)

            out_dict['data'] = series_data_list

            output_data_list.append(out_dict)

        return output_data_list


class USBLSCPIDownloader(USBLSDataDownloader):

    def __init__(self, registration_key):
        super(self.__class__, self).__init__(registration_key = registration_key)

    def get_us_bls_indicator(self) -> bls_id.USBLSSeriesID:

        return bls_id.USBLSSeriesIdCPI()


class USBLSPPIDownloader(USBLSDataDownloader):

    def __init__(self, registration_key):
        super(self.__class__, self).__init__(registration_key = registration_key)

    def get_us_bls_indicator(self) -> bls_id.USBLSSeriesID:

        return bls_id.USBLSSeriesIdPPI()
