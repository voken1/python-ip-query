# Python: IP Query

[![PyPi Version](http://img.shields.io/pypi/v/ip-query.svg)](https://pypi.python.org/pypi/ip-query/)

IP Query, allow proxy.


## Installation

``` console
$ pip3 install ip-query
```


## Usage

``` python
from ip_query import ip_query

ip = ip_query()
```

you will get the result like this:

``` text
{
    'ip': '112.118.6.224',
    'country': 'Hong Kong',
    'country_code': 'HK',
    'asn': 4760,
    'aso': 'HKT Limited'
}
```

Behind a socks5 proxy? use like this:

``` python
from ip_query import ip_query

ip = ip_query(
    requests_proxies={
        'http': 'socks5://127.0.0.1:1080',
        'https': 'socks5://127.0.0.1:1080',
    },
)
```


## Thanks

We've chosen `GeoLite2 Country` and `GeoLite2 ASN` from [GeoLite2 Free Downloadable Databases](https://dev.maxmind.com/geoip/geoip2/geolite2/)..

Latest Version: `20190312`.

Many thanks to [MaxMind](https://github.com/MaxMind).

