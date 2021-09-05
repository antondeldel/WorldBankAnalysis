country_listing = 'https://api.worldbank.org/v2/country?format=json'

individual_url = 'http://api.worldbank.org/v2/country/{}?format=json'

movement_gdp = 'https://databank.worldbank.org/data/download/GEP_CSV.zip'

raw_gbp = 'https://databank.worldbank.org/data/download/GDP.csv'

keys = ['id', 'iso2Code', 'name', 'region', 'adminregion', 'incomeLevel', 'lendingType', 'capitalCity', 'longitude', 'latitude']

gdp_keys = ['Country Name', 'Country Code', 'Indicator Name', 'Indicator Code',
       'Year', 'Change']

raw_gdp = ['iso2Code', 'Ranking','Unnamed1','Name','GDP','Unnamed1']