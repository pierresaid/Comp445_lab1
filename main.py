import logging

from src.Core import Core
from src.http import Http

logging.basicConfig(format='httpc: %(message)s', level=logging.DEBUG)

core = Core()
try:
    core.run()
except Exception as e:
    logging.error(e)
exit(0)

# req = Http("http://www.google.fr")
req = Http("http://httpbin.org/get?course=networking&assignment=1")
# req = Http("http://httpbin.org/status/418")
# req = Http("http://example.com/")

# req = Http("http://www.google.fr/")

res = req.get(['azd : zfe:'])
# res = req.post('name=admin&shoesize=12')
# print(str(res.body, encoding='utf-8'), end='')
print("Status : " + res.status)
print("Code : " + res.code)
print("Headers : ", end='')
print(res.headers)
print("Body : " + str(res.body, encoding='utf-8'))
# req.get("http://httbin.org/get")

# TODO command line interpreter
# TODO parse status body header etc...
# TODO Handle port
