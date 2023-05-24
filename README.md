# MarketDataCollector: A tool for collecting various market data 
MarketDataCollector is developed to enable the collection of various market data for financial analysis and flexible for further extension.

Currently, Consumer Price Index and Producer Price Index Industry Data from U.S. Bureau of Labor Statistics are developed.

# I. Python Implementation

The main Python implementation can be found in marketdatacollector/macroeconomic/USBureauOfLaborStatisticsData

It contains two main modules:
- us_bls_series_id_generator
  - This module generates the id deries based on the datatype indicated
  
- us_bls_data_downloader
  - This module downloads the data from U.S. Bureau of Labor Statistics Database for the id deries generated
 
# I.I Application

# I.I.I create instance
Create an instance for the data to be downloaded with parameter registration_key.
For example, if CPI, then generate an instance of USBLSCPIDownloader in us_bls_data_downloader module
The registration key can be applied here for free: https://data.bls.gov/registrationEngine/

# I.I.II Indicate the details of the data to be downloaded
The data to be downloaded may vary for the same data type.

For example, for CPI, the data could be seasonal adjusted or not.

Therefore, in order to see what are the details and indicate the details, you can use print_components method

It will show:
```{python}
component name: "prefix", current value: "CU"
component name: "seasonal_adjustment", current value: "S"
component name: "periodicity", current value: "R"
component name: "area", current value: "0000"
code name of component "area" can be found by using get_us_bls_series_id_mapping_table method
component name: "item", current value: "['SA0']"
code name of component "item" can be found by using get_us_bls_series_id_mapping_table method
```

The component name are the component that you can choose, except for prefix
If you see code name of component "xxxx" can be found by using get_us_bls_series_id_mapping_table method
It means there are various choices and you can find the details of the choices by using get_mapping_components_table method.

For example, if you want to find which area you can choose for CPI,
You can call get_mapping_components_table('area')
It will show:
```{figure} /figures/area_mapping_table.png
:height: 300px
:name: area_mapping_table

Area Mapping Table for CPI
```
The area_code of the corresponding area_name will be what to be indicated to download the data of the corresponding area

The way to indicate the details is to first create a dictionary with key of component name and value of the code.

For example, to indicate not seasonal adjusted, you create a dictionary as:

{"seasonal_adjustment": "U}

And call specify_data_indicator method with this parameter.

# I.I.III Download and format data

Finally, you specify the start year and end year of the period of the data to be downloaded by using .get_bls_data(start_year, end_year) method.

And then use .format_bls_data() to format the downloaded data.

The output of format_bls_data method is a list of dictionary.

To view the downloaded data in dataframe in time series, you can run pd.DataFrame(output[0]['data']),
The dataframe will be like:
```{figure} /figures/downloaded_data.png
:height: 300px
:name: area_mapping_table

Downloaded Data
```

A code example of usage can be also found in marketdatacollector/macroeconomic/USBureauOfLaborStatisticsData/us_bls_data_main.py

