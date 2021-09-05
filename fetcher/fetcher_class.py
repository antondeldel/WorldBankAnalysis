from . import url_links
from . import connection_string

import requests
import json
from collections import defaultdict
import pandas as pd
import zipfile
import os

class CountryFetcher:
    def __init__(self) -> None:

        
        self.detailed_country_data = pd.DataFrame(columns=url_links.keys)
        self.total_countries = 0
        self.detailed_country_data = pd.DataFrame(columns=url_links.gdp_keys)
        self.raw_gbp = pd.DataFrame(columns=url_links.gdp_keys)

        pass

    def refresh_country_list(self):
        '''
        Queries the country listing API to get full list of countries
        '''
        a = requests.get(url_links.country_listing)
        a = json.loads(a.content)
        #TODO add checks
        self.total_countries = int(a[0]['total'])
        df = pd.read_json(json.dumps(a[1]), orient='records')
        
        for k in ['adminregion','lendingType','region','incomeLevel']:
            df[k] =  df[k].str['value']

        for col in url_links.keys:
            if col not in df.columns:
                df[col] = ''
        
        self.data = df.loc[:,url_links.keys]
                    
        pass
    
    
    def refresh_detailed_data(self):
        '''
        Wrapper function for the country-level query

        '''
        url = url_links.movement_gdp
        r = requests.get(url, stream=True)
        save_path = (os.path.join(os.getcwd(),'data','data.zip'))
        print('Downloading files')
        with open(save_path, 'wb') as fd:
            for chunk in r.iter_content(chunk_size=1024):
                fd.write(chunk)
        

        zf = zipfile.ZipFile(save_path)
        dfs = [pd.read_csv(zf.open(f), sep=",",header=0) for f in zf.namelist()][0]

        dfs2 = pd.melt(dfs
            ,id_vars=['Country Name', 'Country Code', 'Indicator Name', 'Indicator Code']
            ,var_name='Year'
            ,value_name='Change')
        dfs2 = dfs2.loc[(-dfs2['Year'].str.contains('Un')) & (-dfs2.Change.isna())]
        for key in url_links.gdp_keys:
            if key not in dfs2.columns:
                dfs2[key] = ''
        self.detailed_country_data = dfs2
        
        pass

    def save_output(self):
        self.data.to_sql('base'
                ,con=connection_string.engine
                ,if_exists = 'replace')
        self.detailed_country_data.to_sql('gdp'
                ,con=connection_string.engine
                ,if_exists='replace')
        pass

    def answer_sql_questions(self):
        import os
        files = sorted(['sql/'+x for x in os.listdir('sql')])
        for index, q in enumerate(files):
            df = pd.read_sql(q, con = connection_string.engine)
            print('The answer to Question',index+1,'is')
            print(df)