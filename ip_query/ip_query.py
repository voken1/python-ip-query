#!/usr/bin/env python
# encoding: utf-8

import os
import requests
import geoip2.database
import cli_print as cp

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
    ip = ipsb(requests_proxies=requests_proxies, timeout=timeout)

    if not ip:
        ip = myip(requests_proxies=requests_proxies, timeout=timeout)

    if not ip:
        ip = ipify(requests_proxies=requests_proxies, timeout=timeout)

    if ip:
        # with GEO
        if with_geo and geo_missed(ip):
            data = geoip(ip['ip'])
            if data:
                return data

        # no geo
        return ip

    # no ip
    return None


def geo_missed(ip: dict):
    """
    Return True, if missed any item of geo.

    :param ip: ip dict
    :return: bool
    """
    if ip['country'] is None:
        return True
    if ip['country_code'] is None:
        return True
    if ip['asn'] is None:
        return True
    if ip['aso'] is None:
        return True
    return False


def ipsb(requests_proxies: dict = None, timeout: int = TIMEOUT):
    """
    https://api.ip.sb/geoip

    :param requests_proxies: ...
    :param timeout: ...
    :return: dict or None
    """
    data = requests_get_json(url='https://api.ip.sb/geoip',
                             requests_proxies=requests_proxies,
                             timeout=timeout)
    if data:
        result = IP_DICT.copy()
        result['ip'] = data['ip']
        result['country'] = data['country']
        result['country_code'] = data['country_code']
        result['asn'] = data['asn']
        result['aso'] = data['organization']
        return result
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
            cp.error('[ip_query] requests.status_code: {}'.format(resp.status_code))
            return None

    except Exception as e:
        cp.error('[ip_query] {}'.format(e))
        return None


def geoip(ip_address, country_mmdb: str = None, asn_mmdb: str = None):
    """
    GeoLite2
    https://dev.maxmind.com/geoip/geoip2/geolite2/

    :param ip_address:
    :param country_mmdb:
    :param asn_mmdb:
    :return: dict or None
    """

    data = IP_DICT.copy()
    data['ip'] = ip_address

    try:
        mmdb_dir = os.path.dirname(os.path.abspath(__file__))

        # country
        if country_mmdb and os.path.exists(country_mmdb):
            path_to_country_mmdb = country_mmdb
        else:
            path_to_country_mmdb = os.path.join(mmdb_dir, 'GeoLite2-Country.py')
        with geoip2.database.Reader(path_to_country_mmdb) as reader:
            resp = reader.country(ip_address)
            data['country'] = resp.country.name
            data['country_code'] = resp.country.iso_code

        # asn
        if asn_mmdb and os.path.exists(asn_mmdb):
            path_to_asn_mmdb = asn_mmdb
        else:
            path_to_asn_mmdb = os.path.join(mmdb_dir, 'GeoLite2-ASN.py')
        with geoip2.database.Reader(path_to_asn_mmdb) as reader:
            resp = reader.asn(ip_address)
            data['asn'] = resp.autonomous_system_number
            data['aso'] = resp.autonomous_system_organization

        return data

    except Exception as e:
        cp.error('[ip_query] geoip: {}'.format(e))
        return None
