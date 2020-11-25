from urllib.parse import urlparse, ParseResult, parse_qs, urlencode, unquote_plus


def set_query_param(url, param_name, param_value, url_encode=True):
    u = urlparse(url)
    params = parse_qs(u.query)
    params[param_name] = param_value
    query_string = urlencode(
        params) if url_encode else unquote_plus(urlencode(params, doseq=True))
    res = ParseResult(scheme=u.scheme, netloc=u.hostname, path=u.path,
                      params=u.params, query=query_string, fragment=u.fragment)
    return res.geturl()
