import logging
import sqlite3

from providers.argenprop import Argenprop
from providers.bonifacio import Bonifacio
from providers.ienco import Ienco
from providers.inmobusqueda import Inmobusqueda
from providers.mercadolibre import Mercadolibre
from providers.properati import Properati
from providers.remax import Remax
from providers.rogliano import Rogliano
from providers.urquiza import Urquiza
from providers.zonaprop import Zonaprop


def register_property(conn, prop):
    stmt = 'INSERT INTO properties (internal_id, provider, url) VALUES (:internal_id, :provider, :url)'
    try:
        conn.execute(stmt, prop)
    except Exception as e:
        print(e)


def process_properties(provider_name, provider_data):
    provider = get_instance(provider_name, provider_data)

    new_properties = []

    # db connection
    conn = sqlite3.connect('properties.db')

    # Check to see if we know it
    stmt = 'SELECT * FROM properties WHERE internal_id=:internal_id AND provider=:provider'

    prop_count = 0
    with conn:
        for prop in provider.next_prop():
            cur = conn.cursor()
            logging.info(f"Processing property {prop['internal_id']}")
            cur.execute(
                stmt, {'internal_id': prop['internal_id'], 'provider': prop['provider']})
            result = cur.fetchone()
            cur.close()
            if result == None:
                # Insert and save for notification
                logging.info('It is a new one')
                prop_count += 1
                register_property(conn, prop)
                new_properties.append(prop)

    return new_properties


def get_instance(provider_name, provider_data):
    if provider_name == 'argenprop':
        return Argenprop(provider_name, provider_data)
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
