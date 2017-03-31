import json

from six.moves.urllib.parse import urlencode
from redlib.api.http import HttpRequest, RequestOptions, GlobalOptions

from .base import Completer
from ... import const


class GoogleSuggest(Completer):

    def __init__(self):
        self._g_opt = GlobalOptions(cache_dir=const.autocomp_cache_dir, timeout=3, cache_timeout='15s')


    def complete(self, term):
        r_opt = RequestOptions(headers = {'User-Agent' : 'Mozilla 51.0' })
        http = HttpRequest(self._g_opt)

        url="http://suggestqueries.google.com/complete/search?client=firefox&" + urlencode({'q' : term})
        j = http.get(url, r_opt)
        js = json.loads(j)

        return [i.encode('ascii', 'ignore') for i in js[1]]

