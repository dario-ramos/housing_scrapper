# Providers configuration

For the sake of simplicity I'll include a sample for each of the pre-built providers, which I hope will be good enough.

Notice that:

- All provider keys follow a naming structure: PROVIDER<NUMBER>\_<KEY_NAME>. All keys with the same NUMBER belong to the same provider.
- The NAME key univocally identifies the provider. It must be one of the pre-built ones; see the `get_instance` function in `providers/factory.py` for a list.
- The BASE_URL key is the common part of the url for all listing queries. It's tipically the home page url for the listing site.
- The S1, S2, ... keys are sources. Each of them is a listing query. Each provider can have an arbitrary number of these; they can be set up by city, housing type or any filter that the listing site provides.
- Some providers have a TIMEOUT key. This is a maximum time in seconds to allow for scraping a singular source. This is sometimes necessary because some listing sites can be unreliable or not very amenable to scraping, and cannot be waited on forever.

```
PROVIDER1_NAME = "argenprop"
PROVIDER1_ENABLED = 1
PROVIDER1_BASE_URL = "https://www.argenprop.com"
PROVIDER1_S1 = "/casa-alquiler-localidad-villa-elisa"
PROVIDER1_S2 = "/casa-alquiler-localidad-city-bell"
PROVIDER1_S3 = "/casa-alquiler-localidad-manuel-b-gonnet"
PROVIDER1_S4 = "/casa-alquiler-localidad-arturo-segui"

PROVIDER2_NAME = "bonifacio"
PROVIDER2_ENABLED = 1
PROVIDER2_BASE_URL = "http://bonifaciobienesraices.com"
# Villa Elisa
PROVIDER2_S1 = "/buscar?operacion=ALQUILER&zona_id=4&tipo=CASA"
# City Bell
PROVIDER2_S2 = "/buscar?operacion=ALQUILER&zona_id=1&tipo=CASA"
# Gonnet
PROVIDER2_S3 = "/buscar?operacion=ALQUILER&zona_id=2&tipo=CASA"
PROVIDER2_TIMEOUT = 10

PROVIDER3_NAME = "ienco"
PROVIDER3_ENABLED = 1
PROVIDER3_BASE_URL = "https://iencopropiedades.com/resultado-busqueda"
# Arturo Segui
PROVIDER3_S1 = '/?status%5B%5D=for-rent&type%5B%5D=casa&dormitorios=&location%5B%5D=&areas%5B%5D=arturo-segui&min-price=&max-price='
# City Bell
PROVIDER3_S2 = '/?status%5B%5D=for-rent&type%5B%5D=casa&dormitorios=&location%5B%5D=&areas%5B%5D=city-bell&min-price=&max-price='
# Gonnet
PROVIDER3_S3 = '/?status%5B%5D=for-rent&type%5B%5D=casa&dormitorios=&location%5B%5D=&areas%5B%5D=gonnet&min-price=&max-price='
# Gorina
PROVIDER3_S4 = '/?status%5B%5D=for-rent&type%5B%5D=casa&dormitorios=&location%5B%5D=&areas%5B%5D=gorina&min-price=&max-price='
# Ringuelet
PROVIDER3_S5 = '/?status%5B%5D=for-rent&type%5B%5D=casa&dormitorios=&location%5B%5D=&areas%5B%5D=ringuelet&min-price=&max-price='
# Villa Castels
PROVIDER3_S6 = '/?status%5B%5D=for-rent&type%5B%5D=casa&dormitorios=&location%5B%5D=&areas%5B%5D=villa-castels&min-price=&max-price='
# Villa Elisa
PROVIDER3_S7 = '/?status%5B%5D=for-rent&type%5B%5D=casa&dormitorios=&location%5B%5D=&areas%5B%5D=villa-elisa&min-price=&max-price='

PROVIDER4_NAME = 'inmobusqueda'
PROVIDER4_ENABLED = 1
PROVIDER4_BASE_URL = 'https://www.inmobusqueda.com.ar'
PROVIDER4_S1 = '/casa-alquiler-villa-elisa.html'
PROVIDER4_S2 = '/casa-alquiler-city-bell.html'
PROVIDER4_S3 = '/casa-alquiler-manuel-b-gonnet.html'
PROVIDER4_S4 = '/casa-alquiler-arturo-segui.html'

PROVIDER5_NAME = 'mercadolibre'
PROVIDER5_ENABLED = 1
PROVIDER5_BASE_URL = 'https://inmuebles.mercadolibre.com.ar'
PROVIDER5_S1 = '/casas/alquiler/bsas-gba-sur/la-plata/villa-elisa/'
PROVIDER5_S2 = '/casas/alquiler/bsas-gba-sur/la-plata/city-bell/'
PROVIDER5_S3 = '/casas/alquiler/bsas-gba-sur/la-plata/manuel-b-gonnet/'
PROVIDER5_TIMEOUT = 10

PROVIDER6_NAME = 'properati'
PROVIDER6_ENABLED = 0
PROVIDER6_BASE_URL = 'https://www.properati.com.ar'
# Villa Elisa
PROVIDER6_S1 = '/nf/propiedades/?address=&keywords=&keywords=&operation_id=1&place_ids=%5B1369%5D&point=&seller_id=&type_id=2'
# City Bell
PROVIDER6_S2 = '/nf/propiedades/?address=&keywords=&operation=rent&operation_id=1&place_ids=%5B1379%5D&place_parent_ids=&point=&type_id=2'
# Gonnet
PROVIDER6_S3 = '/nf/propiedades/?address=&keywords=&keywords=&operation_id=1&place_ids=%5B1377%5D&point=&seller_id=&type_id=2'
# Arturo Segui
PROVIDER6_S4 = '/nf/propiedades/?address=&keywords=&keywords=&operation_id=1&place_ids=%5B1370%5D&point=&seller_id=&type_id=2'

PROVIDER7_NAME = 'remax'
PROVIDER7_ENABLED = 0
PROVIDER7_BASE_URL = 'https://www.remax.com.ar'
# Villa Elisa
PROVIDER7_S1 = '/publiclistinglist.aspx?CurrentPage=1&SelectedCountryID=42&CityID=7849957&TransactionType=For%20Rent%2FLease&ComRes=2&PropertyType=1903&IsQuickSearch=1'
# City Bell
PROVIDER7_S2 = '/publiclistinglist.aspx?CurrentPage=1&SelectedCountryID=42&CityID=7849948&TransactionType=For%20Rent%2FLease&ComRes=2&PropertyType=1903&IsQuickSearch=1'
# Gonnet
PROVIDER7_S3 = '/publiclistinglist.aspx?CurrentPage=1&SelectedCountryID=42&CityID=7849952&TransactionType=For%20Rent%2FLease&ComRes=2&PropertyType=1903&IsQuickSearch=1'
# Arturo Segui
PROVIDER7_S4 = '/publiclistinglist.aspx?CurrentPage=1&SelectedCountryID=42&CityID=7881984&TransactionType=For%20Rent%2FLease&ComRes=2&PropertyType=1903&IsQuickSearch=1'
PROVIDER7_TIMEOUT = 10

PROVIDER8_NAME = 'rogliano'
PROVIDER8_ENABLED = 1
PROVIDER8_BASE_URL = 'https://www.rogliano.com.ar'
PROVIDER8_S1 = '/alquileres.php'

PROVIDER9_NAME = 'urquiza'
PROVIDER9_ENABLED = 1
PROVIDER9_BASE_URL = 'https://www.urquiza.com.ar'
# Villa Elisa
PROVIDER9_S1 = '/base.php?tipo=1&pagina=1&operacion=0&dormitorios=cualquiera&ciudad_id=23265-0&aptobanco=2&moneda=0&filtro-precio-desde=&filtro-precio-hasta=&codigo=&q=Buscar'
# City Bell
PROVIDER9_S2 = '/base.php?tipo=1&pagina=1&operacion=0&dormitorios=cualquiera&ciudad_id=23250-0&aptobanco=2&moneda=0&filtro-precio-desde=&filtro-precio-hasta=&codigo=&q=Buscar'
# Gonnet
PROVIDER9_S3 = '/base.php?tipo=1&pagina=1&operacion=0&dormitorios=cualquiera&ciudad_id=23259-0&aptobanco=2&moneda=0&filtro-precio-desde=&filtro-precio-hasta=&codigo=&q=Buscar'
# Arturo Segui
PROVIDER9_S4 = '/base.php?tipo=1&pagina=1&operacion=0&dormitorios=cualquiera&ciudad_id=23247-0&aptobanco=2&moneda=0&filtro-precio-desde=&filtro-precio-hasta=&codigo=&q=Buscar'
# Ringuelet
PROVIDER9_S5 = '/base.php?tipo=1&pagina=1&operacion=0&dormitorios=cualquiera&ciudad_id=24320-0&aptobanco=2&moneda=0&filtro-precio-desde=&filtro-precio-hasta=&codigo=&q=Buscar'
# Tolosa
PROVIDER9_S6 = '/base.php?tipo=1&pagina=1&operacion=0&dormitorios=cualquiera&ciudad_id=23264-0&aptobanco=2&moneda=0&filtro-precio-desde=&filtro-precio-hasta=&codigo=&q=Buscar'

PROVIDER10_NAME = 'zonaprop'
PROVIDER10_ENABLED = 1
PROVIDER10_BASE_URL = 'https://www.zonaprop.com.ar'
PROVIDER10_S1 = '/casas-alquiler-villa-elisa-la-plata.html'
PROVIDER10_S2 = '/casas-alquiler-city-bell.html'
PROVIDER10_S3 = '/casas-alquiler-manuel-b-gonnet.html'
PROVIDER10_S4 = '/casas-alquiler-arturo-segui.html'

PROVIDER11_NAME = 'bertoia'
PROVIDER11_ENABLED = 1
PROVIDER11_BASE_URL = 'https://www.grupo-urbano.com.ar/propiedades/alquileres'
PROVIDER11_S1 = '/city-bell/?orden=0&offset=5&view=1&tp=1&dm=&bn=&m=ARS&vc_minimo=&vc_maximo=&cod='
PROVIDER11_S2 = '/gonnet-manuel-b/?orden=0&offset=5&view=1&tp=1&dm=&bn=&m=ARS&vc_minimo=&vc_maximo=&cod='
PROVIDER11_S3 = '/gorina-joaquin/?orden=0&offset=5&view=1&tp=1&dm=&bn=&m=ARS&vc_minimo=&vc_maximo=&cod='
PROVIDER11_S4 = '/arturo-segui/?orden=0&offset=5&view=1&tp=1&dm=&bn=&m=ARS&vc_minimo=&vc_maximo=&cod='
PROVIDER11_S5 = '/villa-elisa/?orden=0&offset=5&view=1&tp=1&dm=&bn=&m=ARS&vc_minimo=&vc_maximo=&cod='
```
