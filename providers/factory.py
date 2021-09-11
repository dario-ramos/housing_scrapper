from .argenprop import Argenprop
from .bertoia import Bertoia
from .bonifacio import Bonifacio
from .ienco import Ienco
from .inmobusqueda import Inmobusqueda
from .mercadolibre import Mercadolibre
from .properati import Properati
from .remax import Remax
from .rogliano import Rogliano
from .urquiza import Urquiza
from .zonaprop import Zonaprop


def get_instance(provider_name, provider_data):
    if provider_name == 'argenprop':
        return Argenprop(provider_name, provider_data)
    elif provider_name == 'bertoia':
        return Bertoia(provider_name, provider_data)
    elif provider_name == 'bonifacio':
        return Bonifacio(provider_name, provider_data)
    elif provider_name == 'ienco':
        return Ienco(provider_name, provider_data)
    elif provider_name == 'inmobusqueda':
        return Inmobusqueda(provider_name, provider_data)
    elif provider_name == 'mercadolibre':
        return Mercadolibre(provider_name, provider_data)
    elif provider_name == 'properati':
        return Properati(provider_name, provider_data)
    elif provider_name == 'remax':
        return Remax(provider_name, provider_data)
    elif provider_name == 'rogliano':
        return Rogliano(provider_name, provider_data)
    elif provider_name == 'urquiza':
        return Urquiza(provider_name, provider_data)
    elif provider_name == 'zonaprop':
        return Zonaprop(provider_name, provider_data)
    else:
        raise Exception('Unrecognized provider')
