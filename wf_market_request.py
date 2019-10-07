from urllib import request
import json

# https://docs.google.com/document/d/1121cjBNN4BeZdMBGil6Qbuqse-sWpEXPpitQH5fb_Fo/edit

ITEMS_URL = 'https://api.warframe.market/v1/items/{}/orders?include=item'.format
INVENTORY_URL = 'https://api.warframe.market/v1/profile/{}/orders?include=profile'.format
PROFILE_URL = 'https://www.warframe.market/profile/{}/'.format


def api_get_request(url):
    request_instance = request.Request(url)
    try:
        with request.urlopen(request_instance) as response:
            http_response = response.read().decode("utf-8")
            json_object = json.loads(str(http_response))

            return json_object
    except UnicodeEncodeError:
        print('Not ascii encodable!')


def webservice_get_request(url):
    with open('cookie.txt', 'r') as reader:
        cookie = reader.read().encode('utf-8')

    request_instance = request.Request(url)
    # request_instance.add_header('authority', 'warframe.market')
    request_instance.add_header('User-Agent', '')
    request_instance.add_header('Cookie', str(cookie))
    with request.urlopen(request_instance) as response:
        http_response = response.read().decode("utf-8")

        return http_response


def request_item_prices(request_item_name):
    items = api_get_request(ITEMS_URL(request_item_name))['payload']['orders']
    avg_price = -1
    length = len(items)
    for item in items:
        avg_price += item['platinum']

    return 'avg price for {} over {} sets is {}.'.format(request_item_name, length, avg_price / length)


def request_inventory(request_account_name):
    items = api_get_request(INVENTORY_URL(request_account_name))['payload']['sell_orders']

    avg_price = -1
    length = len(items)
    for item in items:
        avg_price += item['platinum'] * item['quantity']

    return 'avg price for {}s inventory over {} sets is {} and has a total value of {}.'.format(request_account_name,
                                                                                                length,
                                                                                                avg_price / length,
                                                                                                avg_price)


def get_settings(request_profile_name):
    profile = webservice_get_request(PROFILE_URL(request_profile_name))
    print(profile)


# item_name = 'burston_prime_receiver'
# account_name = 'Knicklichtjedi'
# print(request_item_prices(item_name))
# request_inventory(account_name)
# get_settings(account_name)

# data = requests.get('https://warframe.market')
# print(data.text)
