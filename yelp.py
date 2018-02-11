# -*- coding: utf-8 -*-
'''
TL;DR of overall workings of yelp.py
query_api() is called first from start(), then query_api() calls the search(), then search() calls request(), and then request() returns a json object.
the query_api() then sees if businesses are in json oject and prints the first businuss.
'''
from __future__ import print_function

import argparse
import json
import pprint
import requests
import sys
import urllib
import coffeeshop

# This client code can run on Python 2.x or 3.x.  Your imports can be
# simpler if you only need one of those.
try:
    # For Python 3.0 and later
    from urllib.error import HTTPError
    from urllib.parse import quote
    from urllib.parse import urlencode
except ImportError:
    # Fall back to Python 2's urllib2 and urllib
    from urllib2 import HTTPError
    from urllib import quote
    from urllib import urlencode


# Yelp Fusion no longer uses OAuth as of December 7, 2017.
# You no longer need to provide Client ID to fetch Data
# It now uses private keys to authenticate requests (API Key)
# You can find it on
# https://www.yelp.com/developers/v3/manage_app
API_KEY= '1t54qajbOLK-eXDY2rtywLC9aefjxfsZM6T12Vf2aeoTQuWvwt3B6clW_2ORAavpZY9T4GrrNvJWwly37Sp-iRrSfHN8NX6xjW-ysVzzENi91CC8ZCtE4IKnrk17WnYx'


# API constants, you shouldn't have to change these.
API_HOST = 'https://api.yelp.com'
SEARCH_PATH = '/v3/businesses/search'
BUSINESS_PATH = '/v3/businesses/'  # Business ID will come after slash.


# Defaults for our simple example.
DEFAULT_TERM = 'coffee'
DEFAULT_LOCATION = 'Austin, TX'
SEARCH_LIMIT = 3


def request(host, path, api_key, url_params=None):
    """Given your API_KEY, send a GET request to the API.
    Args:
        host (str): The domain host of the API.
        path (str): The path of the API after the domain.
        API_KEY (str): Your API Key.
        url_params (dict): An optional set of query parameters in the request.
    Returns:
        dict: The JSON response from the request.
    Raises:
        HTTPError: An error occurs from the HTTP request.
    """
    url_params = url_params or {}
    url = '{0}{1}'.format(host, quote(path.encode('utf8')))
    headers = {
        'Authorization': 'Bearer %s' % api_key,
    }

    print(u'Querying {0} ...'.format(url))

    response = requests.request('GET', url, headers=headers, params=url_params)

    return response.json()


def search(api_key, term, location):
    """Query the Search API by a search term and location.
    Args:
        term (str): The search term passed to the API.
        location (str): The search location passed to the API.
    Returns:
        dict: The JSON response from the request.
    """

    url_params = {
        'term': term.replace(' ', '+'),
        'location': location.replace(' ', '+'),
        'limit': SEARCH_LIMIT
    }
    return request(API_HOST, SEARCH_PATH, api_key, url_params=url_params)


def get_business(api_key, business_id):
    """Query the Business API by a business ID.
    Args:
        business_id (str): The ID of the business to query.
    Returns:
        dict: The JSON response from the request.
    """
    business_path = BUSINESS_PATH + business_id

    return request(API_HOST, business_path, api_key)

def coffee_shop_results(response):
    '''
    Parse JSON Object, iterate through results and create coffeeshop object for each
    coffeeshop in JSOM object
    return the list of coffee shops
    '''
    list_shops = []

    for obj in response["businesses"] :
        print (obj, "next \n\n")
        #coffeeshop =  CoffeeShop()
        #coffeeshop.name(obj["name"])
        #coffeeshop.id(obj["id"])
        #coffeeshop.location(obj["location"])
        #coffeeshop.price(obj["price"])
        #coffeeshop.review(obj["review"])
        #coffeeshop.review(obj["imageUrl"])
        #print("********************COFFEE RES*****"+coffeeshop)



def query_api(term, location):
    """Queries the API by the input values from the user.
    Args:
        term (str): The search term to query.
        location (str): The location of the business to query.
    """
    response = search(API_KEY, term, location)

    businesses = response.get('businesses')
    pprint.pprint(response, indent=2)
    if not businesses:
        print(u'No businesses for {0} in {1} found.'.format(term, location))
        return
    coffee_shop_results(response)

def start():
    parser = argparse.ArgumentParser()

    parser.add_argument('-q', '--term', dest='term', default=DEFAULT_TERM,
                        type=str, help='Search term (default: %(default)s)')
    parser.add_argument('-l', '--location', dest='location',
                        default=DEFAULT_LOCATION, type=str,
                        help='Search location (default: %(default)s)')

    input_values = parser.parse_args()

    try:
        query_api(input_values.term, input_values.location)
    except HTTPError as error:
        sys.exit(
            'Encountered HTTP error {0} on {1}:\n {2}\nAbort program.'.format(
                error.code,
                error.url,
                error.read(),
            )
        )


if __name__ == '__main__':
    main()