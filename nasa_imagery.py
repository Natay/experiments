
import datetime
import sys
import os
import requests

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# API KEY set as an environment variable.
API_KEY = os.getenv("API_KEY") or 'DEMO_KEY'

# API url to send data to.

# TODO: imagery API is wonky.
#API_URL = 'https://api.nasa.gov/planetary/earth/assets'
API_URL = 'https://api.nasa.gov/planetary/earth/imagery'

# WORKING APIS
#API_URL = 'https://eonet.sci.gsfc.nasa.gov/api/v2.1/events'
#API_URL = 'https://api.nasa.gov/EPIC/api/natural/images'

# Dictionary of locations
LOCATIONS = {'state college': (40.781581, -77.844243)}

# Default location is State College, PA.
DEFAULT = (38.862234, -77.075634)


"""
GENERATE certificate in current directory for localhost using:

    openssl req -x509 -out localhost.crt -keyout localhost.key \
      -newkey rsa:2048 -nodes -sha256 \
      -subj '/CN=localhost' -extensions EXT -config <( \
       printf "[dn]\nCN=localhost\n[req]\ndistinguished_name = dn\n[EXT]\nsubjectAltName=DNS:localhost\nkeyUsage=digitalSignature\nextendedKeyUsage=serverAuth")

"""

#  Full path to a certificate file
CERT_FILE = os.path.join(BASE_DIR, 'localhost.crt')
CERT_KEY = os.path.join(BASE_DIR, 'localhost.key')


headers_Get = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }


def main():
    if not API_KEY:
        print("API key not set.")
        sys.exit(-1)

    date = datetime.datetime.today() - datetime.timedelta(days=365)

    date = date.isoformat().split(':')[0].split('T')[0]
    # Get a latitude and longitude
    latitude, longitude = DEFAULT

    # Send a GET request
    params = dict(api_key=API_KEY)

    #req_url = f"{API_URL}?api_key={API_KEY}" + '&'.join([f'{key}={value}' for key, value in params.items()])

    # data = urlencode(params)
    # context = SSLContext()
    # context.load_cert_chain(certfile=CERT_FILE, keyfile=CERT_KEY)
    # #request = Request(url=API_URL, data=params)
    # res = HTTPSConnection(host='api.nasa.gov', port=443, context=context)
    #
    # res.request(method='GET', url=API_URL, body=data)
    # res.send(data=bytes(data, encoding='utf-8'))
    #
    # #print(res.request('GET', API_URL), res)
    # print(res.getresponse().read())
    # 1/0
    response = requests.get(API_URL, params=params, allow_redirects=False)

    returned_protocol = response.request.url.split(':')[0]
    given_protocol = API_URL.split(':')[0]
    if returned_protocol != given_protocol:
        print("**** ERROR : Protocol has been changed in request.")
        print(f"GIVEN PROTOCOL : {API_URL.split(':')[0]}")
        print(f"RETURNED URL: {response.request.url}")
        print(f"RETURNED PROTOCOL : {response.request.url.split(':')[0]}")
        print('-'*100)

    print(response.content)
    data = response.json()
    print(data)
    return data


if __name__ == '__main__':
    main()
