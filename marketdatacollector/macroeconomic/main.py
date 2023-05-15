import pandas as pd
from marketdatacollector.macroeconomic import us_bls_data_download

def get_downloader(registration_key, indictator):

    try:

        if indictator == 'cpi':
            return us_bls_data_download.USBLSCPIDownloader(registration_key)

        elif indictator == 'ppi':
            return us_bls_data_download.USBLSPPIDownloader(registration_key)

    except:
        print('not implemented')


if __name__ == "__main__":

    # registration_key can be applied here for free: https://data.bls.gov/registrationEngine/
    registration_key = 'your registration key'

    # choose 'cpi' or 'ppi'
    indictator = 'cpi'

    downloader = get_downloader(registration_key, indictator)

    # check the components setup to for getting specific data
    downloader.print_components()

    # it shows that by default seasonally adjusted is applied, can provide an input dictionary with key of the component name to change it.
    # The possible value can be found in enums.py
    config_input = {'seasonal_adjustment': 'U'}

    # to check the code for the components, can use the mapping table to find out
    downloader.get_mapping_components_table('item')

    # it can be found that the item code of energy is 'SA0E' and commodity is 'SAC'
    # create a list to provide all items to be downloaded
    items_list = ['SA0E', 'SAC']

    downloader.specify_data_indicator(config_input, items_list)

    # define the data time series period and then download data
    start_year = '2020'
    end_year = '2022'

    downloader.get_bls_data(start_year, end_year)

    # format data and return output
    out = downloader.format_bls_data()

    for series in out:
        print(series['series_title'])
        print(pd.DataFrame(series['data']))