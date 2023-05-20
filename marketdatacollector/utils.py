import requests
import pandas as pd


def get_bls_series_id_component_url(indicator: str,
                                    component: str) -> str:

    """get bls series id component url for checking the code id based on the given indicator and component

    Args:
        indicator (str): string of the indicator prefix symbol. For example, CPI is 'CU'
        component (str): string of the component name, for example, area component of CPI is 'area'

    Returns: url (str): bls series id component url

    """

    root_url = 'https://download.bls.gov/pub/time.series/'

    url = root_url + str(indicator) + '/' + str(indicator) + '.' + str(component)

    return url


def get_bls_series_id_component_mapping_table(bls_series_id_component_url: str) -> pd.DataFrame:
    """ get bls series id component mapping table from bls website

    Args:
        bls_series_id_component_url (str): url of bls series id component

    Returns: dataframe of data from bls_series_id_component_url

    """

    headers = {
        'User-agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582'
    }

    response = requests.get(bls_series_id_component_url, headers=headers)

    content_text = response.text

    content_text_lines = [line.split('\t') for line in content_text.splitlines()]

    columns = content_text_lines[0]

    data = content_text_lines[1:]

    return pd.DataFrame(data, columns=columns)



