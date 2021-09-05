from fetcher import fetcher_class

if __name__ == '__main__':
    #Downlaod data from API
    runner = fetcher_class.CountryFetcher()
    runner.refresh_country_list()
    runner.refresh_detailed_data()
    
    #Save information to Postgress database
    runner.save_output()
    #Execute SQL queries
    runner.answer_sql_questions()
    #Generate visualisation