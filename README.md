# BioPortal APIs

<!--- These are examples. See https://shields.io for others or to customize this set of shields. You might want to include dependencies, project status and licence info here --->
[![Twitter](https://img.shields.io/twitter/follow/SMICRCPR.svg?style=social&label=@SMICRCPR)](https://twitter.com/SMICRCPR)

BioPortal APIs es un paquete de Python que permite accesar las bases de datos públicas del BioPortal del Departamento de Salud de Puerto Rico.

Este paquete le permite a uno descargar y guardar datos públicos del BioPortal a cualquier momento. Presenta un formato sencillo para facilitar su uso a cualquiera que lo desee.

## Prerequisitos

Antes de comenzar, asegúrese de haber cumplido los siguientes requisitos:
<!--- These are just example requirements. Add, duplicate or remove as required --->
* Tienes instalado una versión de Python >= 3.6
* Estas utilizando una computadora con Windows, Mac, o Linux.

## Instalando BioPortal APIs

Para instalar BioPortal APIs, abre una ventana del Command Line o Terminal y corra:

```bash
pip install bioportal
```

## Usando BioPortal APIs

Siga estos pasos en un programa de Python para descargar datos de APIs públicos:

```python
from bioportal import BioPortalClient

cliente = BioPortalClient()

casos_por_coleccion = cliente.descargar_dataset('Casos por fecha de coleccion')
casos_por_coleccion.to_csv('Casos_por_fecha_coleccion.csv')
```
El resultado será un archivo conteniendo una tabla en formato csv.
Además, puede ver cuales APIs estan disponibles usando:

```python
cliente.datasets_disponibles()
```
```
Bases de datos disponibles:
  1   'Pruebas unicas con informacion minima'
  2   'Pruebas unicas con ID de paciente y fechas en tiempo local de Puerto Rico'
  3   'Pruebas unicas con ID de paciente y fechas en tiempo internacional UTC'
  4   'Pruebas por fecha de coleccion'
  5   'Pruebas por fecha de reporte'
  6   'Pruebas por fecha de coleccion y entidad'
  7   'Total de TDF por fecha reportada de llegada'
  8   'Casos por fecha de coleccion'
  9   'Casos por fecha de creacion en sistema'
 10   'Casos por grupo de edad'
 11   'Casos por ciudad'
 12   'Casos por region'
 13   'Resumen de Escuelas Publicas y Privadas'
```

## Contribuyendo a desarrollar este programa
<!--- If your README is long or you have some specific process or steps you want contributors to follow, consider creating a separate CONTRIBUTING.md file--->
Para contribuir al crecimiento de BioPortal APIs, sigue estos pasos:

1. Bifurca este repositorio.
2. Crea una rama: `git checkout -b <nombre_rama>`.
3. Haga sus cambios y guardelos usando un commit: `git commit -m '<commit_message>'`
4. Empujalos a la rama original: `git push origin bioportal-apis/<localizacion>`
5. Crea un pull request.

Alternativamente, puede rebuscar la documentación de GitHub para [crear un pull request](https://help.github.com/en/github/collaborating-with-issues-and-pull-requests/creating-a-pull-request).

## Contribuyentes

## Contacto

En caso de alguna pregunta, puede contactarnos a través de <jose.zavala@salud.pr.gov>.

## Licencia
<!--- If you're not sure which open license to use see https://choosealicense.com/--->

Este proyecto esta licenciado bajo los terminos de la [Licencia MIT](LICENSE).
