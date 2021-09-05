from fetcher import fetcher_class

if __name__ == '__main__':
    #Downlaod data from API
    runner = fetcher_class.CountryFetcher()
    runner.refresh_country_list()
    runner.refresh_detailed_data()
    runner.save_output()
    #Save information to Postgress database

    #Execute SQL queries

    #Generate visualisation