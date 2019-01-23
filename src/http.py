import socket
from urllib.parse import urlparse, ParseResult, parse_qs
import re
from uu import encode


class Http:

    def __init__(self, url):
        parsed_url = urlparse(url)
        self.socket = None
        if parsed_url.path == url:
            url = "http://" + url
            parsed_url = urlparse(url)
        if parsed_url.hostname is None or parsed_url.path is None:
            raise Exception('<url> malformed')
        self.hostname = parsed_url.hostname
        self.path = parsed_url.path
        if parsed_url.query is not '':
            self.path += "?" + parsed_url.query
        if self.path == '':
            self.path = '/'
        # print(self.path)
        # print(self.hostname)

    def get(self, headers=None):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket = s
        s.connect((self.hostname, 80))
        query = "GET {0} HTTP/1.1\r\nHost: {1}\r\n".format(self.path, self.hostname)
        if headers is not None:
            for h in headers:
                if re.search("(.+):(.+)", h):
                    query += h + "\r\n"
        query += "\r\n\r\n"
        # print(query)
        s.sendall(str.encode(query))
        result = self.read_result()
        # print(str(result, encoding='utf-8'), end='')
        s.close()
        return str(result, encoding='utf-8')

    def post(self, data=None, headers=None):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket = s
        s.connect((self.hostname, 80))

        query = "POST {0} HTTP/1.1\r\nHost: {1}\r\n".format(self.path, self.hostname)
        if headers is not None:
            for h in headers:
                if re.search("(.+):(.+)", h):
                    query += h + "\r\n"
        if data is not None:
            query += "Content-Length: {0}\r\n".format(len(data))

        query += "\r\n"
        s.sendall(str.encode(query))
        if data is not None and len(data) > 0:
            s.sendall(data.encode())

        result = self.read_result()
        # print(str(result, encoding='utf-8'), end='')
        s.close()
        return str(result, encoding='utf-8')

    def read_result(self):
        result = b''
        new_res = None
        # while not re.search("Content-Length:.(.*?)\\r\\n", str(result, encoding='utf-8')):
        while result.find(b'\r\n\r\n') == -1 and (new_res is None or len(new_res) != 0):
            new_res = self.socket.recv(1)
            result += new_res
        begin_length_idx = result.find(b'Content-Length: ') + len('Content-Length: ')
        end_lenght_idx = result[begin_length_idx:].find(b'\r\n')
        content_length = int(str(result[begin_length_idx:][:end_lenght_idx], encoding='utf-8'))
        result = self.socket.recv(content_length)
        return result
