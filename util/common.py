import numpy as np
import pandas as pd
import six
import zipfile
from six.moves.urllib.parse import urlparse
import requests

class URLFetch:

    def __init__(self, url, method='get', json=False, session=None,
                 headers=None, proxy=None):
        self.url = url
        self.method = method
        self.json = json

        if not session:
            self.session = requests.Session()
        else:
            self.session = session

        if headers:
            self.session.headers.update(headers)
        if proxy:
            self.update_proxy(proxy)
        else:
            self.update_proxy('')

    def set_session(self, session):
        self.session = session
        return self

    def get_session(self, session):
        self.session = session
        return self

    def __call__(self, *args, **kwargs):
        u = urlparse(self.url)
        self.session.headers.update({'Host': u.hostname})
        url = self.url % (args)
        if self.method == 'get':
            return self.session.get(url, params=kwargs, proxies=self.proxy)
        elif self.method == 'post':
            if self.json:
                return self.session.post(url, json=kwargs, proxies=self.proxy)
            else:
                return self.session.post(url, data=kwargs, proxies=self.proxy)

    def update_proxy(self, proxy):
        self.proxy = proxy
        self.session.proxies.update(self.proxy)

    def update_headers(self, headers):
        self.session.headers.update(headers)


class ParseTables:
    def __init__(self, *args, **kwargs):
        self.schema = kwargs.get('schema')
        self.bs = kwargs.get('soup')
        self.headers = kwargs.get('headers')
        self.index = kwargs.get('index')
        self._parse()

    def _parse(self):
        trs = self.bs.find_all('tr')
        lists = []
        schema = self.schema
        for tr in trs:
            tds = tr.find_all('td')
            if len(tds) == len(schema):
                lst = []
                for i in range(0, len(tds)):
                    txt = tds[i].text.replace('\n', '').replace(
                        ' ', '').replace(',', '')
                    try:
                        val = schema[i](txt)
                    except:
                        if schema[i] == float or schema[i] == int:
                            val = np.nan
                        else:
                            val = ''
                            #raise ValueError("Error in %d. %s(%s)"%(i, str(schema[i]), txt))
                    lst.append(val)
                lists.append(lst)
        self.lists = lists

    def get_tables(self):
        return self.lists

    def get_df(self):
        if self.index:
            return pd.DataFrame(self.lists, columns=self.headers).set_index(self.index)
        else:
            return pd.DataFrame(self.lists, columns=self.headers)


def unzip_str(zipped_str, file_name=None):
    if isinstance(zipped_str, six.binary_type):
        fp = six.BytesIO(zipped_str)
    else:
        fp = six.BytesIO(six.b(zipped_str))

    zf = zipfile.ZipFile(file=fp)
    if not file_name:
        file_name = zf.namelist()[0]
    return zf.read(file_name).decode('utf-8')
