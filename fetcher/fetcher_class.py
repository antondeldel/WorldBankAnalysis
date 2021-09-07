from . import url_links
from . import connection_string

import requests
import json
from collections import defaultdict
import pandas as pd
pd.options.display.float_format = '{:,.2f}'.format
import zipfile
import os
import plotly.express as px

class CountryFetcher:
    def __init__(self) -> None:

        
        self.detailed_country_data = pd.DataFrame(columns=url_links.keys)
        self.total_countries = 0
        self.detailed_country_data = pd.DataFrame(columns=url_links.gdp_keys)

        pass

    def refresh_country_list(self):
        '''
        Queries the country listing API to get full list of countries
        '''
        q = []
        print('Refreshing master data')
        for i in range(1,100):
            a = requests.get(url_links.country_listing + f'&page={i}')
            a = json.loads(a.content)
            #TODO add checks
            self.total_countries = int(a[0]['total'])
            if a[0]['page'] > a[0]['pages']:break
            df = pd.read_json(json.dumps(a[1]), orient='records')
            q.append(df)
        df = pd.concat(q,ignore_index=True,sort=False).reset_index(drop=True)
        
        
        for k in ['adminregion','lendingType','region','incomeLevel']:
            df[k] =  df[k].str['value']
        
        df = df.drop_duplicates()

        for col in url_links.keys:
            if col not in df.columns:
                df[col] = ''
        
        self.data = df.loc[:,url_links.keys]
                    
        pass
    
    
    def refresh_detailed_data(self):
        '''
        Wrapper function for the country-level query

        '''
        url = url_links.correct_gbp
        print('Downloading files')
        r = requests.get(url, stream=True)
        save_path = (os.path.join(os.getcwd(),'data','data.zip'))
        
        with open(save_path, 'wb') as fd:
            for chunk in r.iter_content(chunk_size=1024):
                fd.write(chunk)
        

        zf = zipfile.ZipFile(save_path)
        f = sorted(zf.namelist())[0]
        dfs = pd.read_csv(zf.open(f), sep=",",header=2)

        dfs2 = pd.melt(dfs
            ,id_vars=['Country Name', 'Country Code', 'Indicator Name', 'Indicator Code']
            ,var_name='Year'
            ,value_name='Value')
        dfs2 = dfs2.loc[(-dfs2['Year'].str.contains('Un')) & (-dfs2.Value.isna())]
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

        files = sorted(['sql/'+x for x in os.listdir('sql')])
        for index, q in enumerate(files):
            with open(q) as a:
                q = a.read()
            df = pd.read_sql(q, con = connection_string.engine)
            df.style.hide_index()
            print('|','-'*40,'|')
            print('|','-'*20,'|')
            print('The answer to Question',index+1,'is')
            print('|','-'*20,'|')
            print(df.to_string(index=False))
            print('|','-'*40,'|')
    
    def save_to_html(self):
        from . import gInterestingFact
        df = pd.read_sql(gInterestingFact.interestingFactSQL
                ,con=connection_string.engine
                )

        # fig =px.scatter(
        #     x=self.data.longitude.replace('',0).apply(float), 

        #     y=self.data.latitude.replace('',0).apply(float))
        fig = px.area(df, 
            x="Year"
            ,y="Value"
            ,color="region"
            ,line_group="region"
            ,groupnorm='percent')
        fig.write_html(os.path.join(os.getcwd(),"graphs.html"))