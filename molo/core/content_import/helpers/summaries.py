import requests

from molo.core.content_import.errors import SiteResponseError


def get_summaries(url):
    # TODO handle error responses
    # TODO validate json response
    resp = requests.get(url)

    if is_error_response(resp):
        raise SiteResponseError(
            "%s responded with a %s error" % (url, resp.status_code))
    else:
        return parse_repo_summaries_response(resp.json())


def parse_repo_summaries_response(resp):
    return [{
        'name': d['index'],
        'title': d['data']['title']
    } for d in resp]


def is_error_response(resp):
    code = resp.status_code
    return 400 <= code < 500 or 500 <= code < 600