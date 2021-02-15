import requests
import pandas as pd
import brotli


def get_api_data(apiurl):
    r = requests.get(apiurl, headers={'Accept-Encoding': 'br'})
    return r

if __name__ == '__main__':
    apiurl = 'https://BioPortal.salud.gov.pr/api/administration/reports/cases/grouped-by-collected-date'
    data = get_api_data(apiurl)