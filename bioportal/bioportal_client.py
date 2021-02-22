import json
import brotli
import requests
import pandas as pd


class BioPortalClient:
    """Cliente para conectarse a y descargar datos directamente del BioPortal.

    Atributos:
        api_urls (dict): API url correspondiendo a cada dataset público.
        apidata (:obj:`pandas.DataFrame`): Datos descargados. None si no se ha descargado nada.

    """
    api_urls = {
      'Cantidades totales de pruebas reportadas': 'https://BioPortal.salud.gov.pr/api/administration/reports/total',
      'Pruebas unicas con informacion minima': 'https://BioPortal.salud.gov.pr/api/administration/reports/minimal-info-unique-tests',
      'Pruebas unicas con ID de paciente y fechas en tiempo local de Puerto Rico': 'https://BioPortal.salud.gov.pr/api/administration/reports/orders/minimal-info',
      'Pruebas unicas con ID de paciente y fechas en tiempo internacional UTC': 'https://BioPortal.salud.gov.pr/api/administration/reports/orders/basic',
      'Pruebas diarias para grafica de dashboard de Salud': 'https://BioPortal.salud.gov.pr/api/administration/orders/dashboard-daily-testing', # HTML enable JS
      'Pruebas por fecha de coleccion': 'https://BioPortal.salud.gov.pr/api/administration/reports/tests-by-collected-date',
      'Pruebas por fecha de reporte': 'https://BioPortal.salud.gov.pr/api/administration/reports/tests-by-reported-date',
      'Pruebas por fecha de coleccion y entidad': 'https://BioPortal.salud.gov.pr/api/administration/reports/tests-by-collected-date-and-entity',
      'Total de TDF por fecha reportada de llegada': 'https://BioPortal.salud.gov.pr/api/administration/reports/travels/total-forms-by-reported-arrival-date',
      'Total de TDF por municipio': 'https://BioPortal.salud.gov.pr/api/administration/travels/total-forms-by-municipalities',   # HTML enable JS
      'Casos por fecha de coleccion': 'https://BioPortal.salud.gov.pr/api/administration/reports/cases/grouped-by-collected-date',
      'Casos por fecha de creacion en sistema': 'https://BioPortal.salud.gov.pr/api/administration/reports/cases/dashboard-daily',
      'Casos por grupo de edad': 'https://BioPortal.salud.gov.pr/api/administration/reports/cases/dashboard-age-group',
      'Casos por ciudad': 'https://BioPortal.salud.gov.pr/api/administration/reports/cases/dashboard-city',
      'Casos por region': 'https://BioPortal.salud.gov.pr/api/administration/reports/cases/dashboard-region',
      'Resumen de Escuelas Publicas y Privadas': 'https://BioPortal.salud.gov.pr/api/administration/reports/education/general-summary',
    }

    def __init__(self):
        """El constructor para el BioPortalClient.
        """
        self.apidata = None
        pass

    def datasets_disponibles(self):
        """Imprime una lista de los nombres de los datasets disponibles para descargar.

        Devuelve:
            None
        """
        print('Bases de datos disponibles:')
        for i,k in enumerate(self.api_urls):
          print(" {}   '{}'".format(str(i+1).rjust(2), k))

    def descargar_dataset(self, nombre_dataset, verbose=True):
        """Descargar un dataset de algun API público del BioPortal.

        Este dataset procesado tambien es guardado en el atributo 'apidata'.

        Parametros:
            nombre_dataset (str): Nombre del dataset para descargar.
            verbose (bool; opcional): Opcion para imprimir detalles a lo largo de la descarga.
        
        Devuelve:
            self.apidata (pandas.DataFrame): Datos descargados y procesados del API indicado.
        """
        if nombre_dataset not in self.api_urls:
          raise ValueError("El dataset '{}' no esta disponible. \
          Usa client.datasets_disponibles() para encontrar cuales lo estan.".format(nombre_dataset))
        aurl = self.api_urls[nombre_dataset]
        if verbose: print('Descargando "{}"...'.format(nombre_dataset))
        apidata, exitoso = self.descargar_dataset_url(aurl, verbose=verbose)
        if exitoso:
          if verbose: print("Descargado.")
          self.apidata = apidata
        else:
          print("Descarga falló.")
        return self.apidata

    def descargar_dataset_url(self, apiurl, verbose=True, dataframe=True):
        """Descargar un dataset usando directamente un API URL provisto.

        Este método es útil para descargar datasets de APIs que aun no esten
        implementados dentro del atributo de 'api_urls'. Tambien funciona
        para bajar la data cruda al escoger False para el parametro de 'dataframe'.

        Parametros:
            apiurl (str): URL completo (e.g. 'https://[...]') de un API público de BioPortal.
            verbose (bool; opcional): Opcion para imprimir detalles a lo largo de la descarga.
            dataframe (bool; opcional): Opcion para procesar datos descargados a DataFrame.
                                            Elija False para devolver data cruda.

        Devuelve:
            apidata (str o pandas.DataFrame): Datos descargados. Crudos (str) si 'dataframe' es False;
                                                si no, procesados a un pandas.DataFrame.
            exitoso (bool): Bandera clarificando si el api pudo descargarse exitosamente.
        """
        self.apidata = None

        try:
          r = requests.get(apiurl, headers={'Accept-Encoding': 'br'}, timeout=(15,None))
        except requests.exceptions.Timeout:
          # Se quedo pegao
          print("Servidor no responde.")
          return (None, False)

        # Status code
        if r.status_code != 200:
          print("Respuesta inesperada del servidor (#{})".format(r.status_code))
          return (None, False)

        apidata_raw = r.content

        if r.encoding.startswith('ISO'):
          if r.content.decode().startswith('<!DOCTYPE html>'):
            print("Servidor no esperaba que bajaras este API (devolvio un documento HTML)")
            return (None, False)

        try:
          apidata_raw = (brotli.decompress(apidata_raw))
        except:
          pass

        if dataframe:
          apidata = pd.json_normalize(  json.loads(apidata_raw),  sep='_')
        else:
          apidata = apidata_raw
        return (apidata, True)


## Ejemplo para descargar un dataset:
if __name__ == '__main__':
    # Crear cliente de BioPortal
    cliente = BioPortalClient()

    # Imprimir la lista de datasets disponibles
    cliente.datasets_disponibles()

    # Descargar e imprimir los datos indicados
    casos_por_coleccion = cliente.descargar_dataset('Casos por fecha de coleccion')
    print(casos_por_coleccion)

    # Guardarlos a un archivo de formato csv
    # casos_por_coleccion.to_csv('Casos_fecha_coleccion.csv')

    # Probando: Intentar descargar todos los APIs
    # for i,k in enumerate(cliente.api_urls):
    #   print(i+1, k)
    #   cliente.descargar_dataset(k)
    #   print()