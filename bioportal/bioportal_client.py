import json
import brotli
import requests
import pandas as pd


class BioPortalClient:
  api_urls = {
      # 'Cantidades totales de pruebas reportadas': 'https://BioPortal.salud.gov.pr/api/administration/reports/total', # Decompression error: incomplete compressed string (?)
      'Pruebas unicas con informacion minima': 'https://BioPortal.salud.gov.pr/api/administration/reports/minimal-info-unique-tests',
      'Pruebas unicas con ID de paciente y fechas en tiempo local de Puerto Rico': 'https://BioPortal.salud.gov.pr/api/administration/reports/orders/minimal-info',
      'Pruebas unicas con ID de paciente y fechas en tiempo internacional UTC': 'https://BioPortal.salud.gov.pr/api/administration/reports/orders/basic',
      # 'Pruebas diarias para grafica de dashboard de Salud': 'https://BioPortal.salud.gov.pr/api/administration/orders/dashboard-daily-testing', # HTML enable JS
      'Pruebas por fecha de coleccion': 'https://BioPortal.salud.gov.pr/api/administration/reports/tests-by-collected-date',
      'Pruebas por fecha de reporte': 'https://BioPortal.salud.gov.pr/api/administration/reports/tests-by-reported-date',
      'Pruebas por fecha de coleccion y entidad': 'https://BioPortal.salud.gov.pr/api/administration/reports/tests-by-collected-date-and-entity',
      'Total de TDF por fecha reportada de llegada': 'https://BioPortal.salud.gov.pr/api/administration/reports/travels/total-forms-by-reported-arrival-date',
      # 'Total de TDF por municipio': 'https://BioPortal.salud.gov.pr/api/administration/travels/total-forms-by-municipalities',   # HTML enable JS
      'Casos por fecha de coleccion': 'https://BioPortal.salud.gov.pr/api/administration/reports/cases/grouped-by-collected-date',
      'Casos por fecha de creacion en sistema': 'https://BioPortal.salud.gov.pr/api/administration/reports/cases/dashboard-daily',
      'Casos por grupo de edad': 'https://BioPortal.salud.gov.pr/api/administration/reports/cases/dashboard-age-group',
      'Casos por ciudad': 'https://BioPortal.salud.gov.pr/api/administration/reports/cases/dashboard-city',
      'Casos por region': 'https://BioPortal.salud.gov.pr/api/administration/reports/cases/dashboard-region',
      'Resumen de Escuelas Publicas y Privadas': 'https://BioPortal.salud.gov.pr/api/administration/reports/education/general-summary',
  }
  def __init__(self):
    self.apidata = None
    pass

  def datasets_disponibles(self):
    print('Bases de datos disponibles:')
    for i,k in enumerate(self.api_urls):
      print(" {}   '{}'".format(str(i+1).rjust(2), k))

  def descargar_dataset(self, nombre_dataset, verbose=True):
    if nombre_dataset not in self.api_urls:
      raise ValueError("El dataset '{}' no esta disponible. \
      Usa client.datasets_disponibles() para encontrar cuales lo estan.".format(nombre_dataset))
    aurl = self.api_urls[nombre_dataset]
    if verbose: print('Descargando "{}"...'.format(nombre_dataset))
    apidata = self.descargar_dataset_url(aurl, verbose=verbose)
    self.apidata = apidata
    if verbose: print("Descargado.")
    return self.apidata

  def descargar_dataset_url(self, apiurl, verbose=True, dataframe=True):
    r = requests.get(apiurl, headers={'Accept-Encoding': 'br'})
    apidata_raw = (brotli.decompress(r.content))
    if dataframe:
      apidata = pd.json_normalize(  json.loads(apidata_raw),  sep='_')
    else:
      apidata = apidata_raw
    return apidata

if __name__ == '__main__':
    cliente = BioPortalClient()
    cliente.datasets_disponibles()
    casos_por_coleccion = cliente.descargar_dataset('Casos por fecha de coleccion')
    print(casos_por_coleccion)
    pass