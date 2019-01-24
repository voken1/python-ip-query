#!/usr/bin/env python
# encoding: utf-8

import os
import requests
import geoip2.database
import terminal_print as tp


# ip dict format
IP_DICT = {
    'ip': None,
    'country': None,
    'country_code': None,
    'asn': None,
    'aso': None,
}

# requests timeout
TIMEOUT = 5


def ip_query(requests_proxies: dict = None, timeout: int = TIMEOUT, with_geo: bool = True):
    """
    Get IP data, include: ip address, country, country_code, asn, aso

    :param requests_proxies: ...
    :param timeout: ...
    :param with_geo: with Geo info?
    :return: dict or None
    """
    ip = myip(requests_proxies=requests_proxies, timeout=timeout)

    if not ip:
        ip = ipify(requests_proxies=requests_proxies, timeout=timeout)

    if ip:
        # with GEO
        if with_geo:
            data = geoip(ip['ip'])
            if data:
                return data

        # no geo
        return ip

    # no ip
    return None


def myip(requests_proxies: dict = None, timeout: int = TIMEOUT):
    """
    https://www.myip.com/api-docs/

    :param requests_proxies: ...
    :param timeout: ...
    :return: dict or None
    """
    data = requests_get_json(url='https://api.myip.com/',
                             requests_proxies=requests_proxies,
                             timeout=timeout)
    if data:
        result = IP_DICT.copy()
        result['ip'] = data['ip']
        result['country'] = data['country']
        result['country_code'] = data['cc']
        return result
    return None


def ipify(requests_proxies: dict = None, timeout: int = TIMEOUT):
    """
    https://www.ipify.org/

    :param requests_proxies: ...
    :param timeout: ...
    :return: dict or None
    """
    data = requests_get_json(url='https://api.ipify.org?format=json',
                             requests_proxies=requests_proxies,
                             timeout=timeout)
    if data:
        result = IP_DICT.copy()
        result['ip'] = data['ip']
        return result
    return None


def requests_get_json(url: str, requests_proxies: dict = None, timeout: int = TIMEOUT):
    """
    Get data and convert to json.

    :param url: URL
    :param requests_proxies: ...
    :param timeout: ...
    :return: json object or None
    """
    try:
        resp = requests.get(url,
                            proxies=requests_proxies,
                            timeout=timeout,
                            )

        if 200 == resp.status_code:
            return resp.json()
        else:
            tp.error('[ip-query] requests.status_code: {}'.format(resp.status_code))
            return None

    except Exception as e:
        tp.error('[ip-query] {}'.format(e))
        return None


def geoip(ip_address):
    """
    GeoLite2
    https://dev.maxmind.com/geoip/geoip2/geolite2/

    :param ip_address: ip
    :return: dict or None
    """
    mmdb_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'mmdb')

    data = IP_DICT.copy()
    data['ip'] = ip_address

    try:
        # country
        with geoip2.database.Reader(os.path.join(mmdb_dir, 'GeoLite2-Country.mmdb')) as reader:
            resp = reader.country(ip_address)
            data['country'] = resp.country.name
            data['country_code'] = resp.country.iso_code

        # asn
        with geoip2.database.Reader(os.path.join(mmdb_dir, 'GeoLite2-ASN.mmdb')) as reader:
            resp = reader.asn(ip_address)
            data['asn'] = resp.autonomous_system_number
            data['aso'] = resp.autonomous_system_organization

        return data

    except Exception as e:
        tp.error('[ip-query] geoip: {}'.format(e))
        return None
