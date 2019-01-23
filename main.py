from src.http import Http

# req = Http("http://www.google.fr")
req = Http("http://httpbin.org/get?course=networking&assignment=1")
# req = Http("http://example.com/")

# req = Http("http://www.google.fr/")

res = req.get()
# res = req.post('name=admin&shoesize=12')
print(res, end='')

# req.get("http://httbin.org/get")

# TODO command line interpreter
# TODO parse status body header etc...