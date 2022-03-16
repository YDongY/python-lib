import json
import logging
import hashlib
from datetime import datetime

import requests

_LOGGER = logging.getLogger(__name__)


def do_get(url, params, key):
    _add_sign(params, key)
    resp = requests.get(url, params, timeout=5)
    return _decode_response(url, params, resp)


def do_post(url, params, key):
    _add_sign(params, key)
    resp = requests.post(url, data=json.dumps(params), headers={'Content-Type': 'application/json'}, timeout=5)
    return _decode_response(url, params, resp)


def do_delete(url, params, key):
    _add_sign(params, key)
    resp = requests.delete(url, data=json.dumps(params), timeout=5)
    return _decode_response(url, params, resp)


def _decode_response(url, params, resp):
    _LOGGER.info('request url: {}, params: {}, get resp: {} - {}'.format(url, params, resp.status_code, resp.text))

    try:
        resp_json = resp.json()
    except ValueError:
        resp_json = dict()
    if 'status' not in resp_json:
        raise ValueError('open api response is not valid')
    return resp_json


def _add_sign(params, key):
    params['timestamp'] = int(datetime.now().timestamp())
    s = ''
    for k in sorted(params.keys()):
        if params[k] is not None:
            s += '%s=%s&' % (k, params[k])
    s += 'key=%s' % key
    m = hashlib.md5()
    m.update(s.encode('utf8'))
    sign = m.hexdigest().upper()
    params['sign'] = sign
