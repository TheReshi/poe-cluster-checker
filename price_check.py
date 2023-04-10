import requests
import resources as res
import time

LEAGUE = "Crucible"
SESSION_ID = []
CURRENCY_DATA = {}
non_added = []

def read_sess_ids():
    with open("sessid.txt", 'r') as sessidfile:
        for sessid in sessidfile:
            SESSION_ID.append(sessid.strip())

def get_currency_data():
    for currency in res.CURRENCY_ID.keys():
        params = {
            'league': LEAGUE,
            'type': 'Currency',
            'currencyId': res.CURRENCY_ID[currency],
        }

        response = requests.get('https://poe.ninja/api/data/currencyhistory', params=params)
        # print(response.content)

        CURRENCY_DATA[currency] = round(int(response.json()["receiveCurrencyGraphData"][-1]["value"]))


def get_divine_price():
    params = {
        'league': LEAGUE,
        'type': 'Currency',
        'currencyId': '3',
    }

    response = requests.get('https://poe.ninja/api/data/currencyhistory', params=params)
    return round(int(response.json()["receiveCurrencyGraphData"][-1]["value"]))

get_currency_data()

# DIVINE_PRICE = get_divine_price()

def get_item_prices(cluster_id, combs):
    item_data = None

    while not item_data:
        for sess_id in SESSION_ID:
            item_data = get_item_data(sess_id, cluster_id, combs)
            while item_data == -1:
                print("Trade site probably dead!")
                time.sleep(300)
                item_data = get_item_data(sess_id, cluster_id, combs)
            if item_data and item_data != -1:
                break
        if not item_data:
            time.sleep(60)

    found_items = []
    for found_item in item_data.json()["result"]:
        found_items.append(found_item)

    if len(found_items) > 5:
        found_items = found_items[0:5]

    prices = []

    response = ""

    if len(found_items) > 0:
        while 'result' not in response:
            for sess_id in SESSION_ID:
                res.debug(f"Starting to fetch items with SESSID: {sess_id}")
                while response == -1 or response == "":
                    if response == -1:
                        time.sleep(300)
                    response = fetch_items(found_items, sess_id)
                if 'error' in response.json():
                    res.debug(f"Continue with SESSID: {sess_id}")
                    continue
                if 'result' in response.json():
                    res.debug(f"Break with SESSID: {sess_id}")
                    break
            
            if 'error' in response.json():
                res.debug(f"Sleeping with SESSID: {sess_id}")
                time.sleep(60)
            elif 'result' in response.json():
                for result in response.json()['result']:

                    if result['listing']['price']['currency'] == "chaos" or result['listing']['price']['currency'] in CURRENCY_DATA.keys():
                        for currency in CURRENCY_DATA.keys():
                            if result['listing']['price']['currency'] == currency:
                                prices.append(int(float(result['listing']['price']['amount']) * CURRENCY_DATA[currency]))
                            elif result['listing']['price']['currency'] == "chaos":
                                prices.append(int(result['listing']['price']['amount']))
                    else:
                        non_added.append(result['listing']['price']['currency'])
                        # print(f"NON-ADDED CURRENCY: {result['listing']['price']['currency']}")
                        prices.append(f"{result['listing']['price']['amount']} OTHER_CURRENCY: {result['listing']['price']['currency']}")

                    # if result['listing']['price']['currency'] == "divine":
                    #     prices.append(int(float(result['listing']['price']['amount']) * DIVINE_PRICE))
                    # elif result['listing']['price']['currency'] == "chaos":
                    #     prices.append(int(result['listing']['price']['amount']))
                    # else:
                    #     prices.append(f"{result['listing']['price']['amount']} {result['listing']['price']['currency']}")
                break

    return prices

def get_item_data(session_id, cluster_id, combs):
    # res.debug(f"cluster_id, prefix1, prefix2, suffix, session_id: {cluster_id}, {prefix1}, {prefix2}, {suffix}, {session_id}")
    res.debug(f"Getting items with SESSID: {session_id}")

    cookies = {
        'cf_clearance': 'Nwu_B8Zv44Uswuv7K9Qkp71S6LepExU26lRuorRYDOQ-1670605370-0-150',
        'POESESSID': session_id,
    }

    headers = {
        'authority': 'www.pathofexile.com',
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9,hu;q=0.8',
        'content-type': 'application/json',
        'origin': 'https://www.pathofexile.com',
        'referer': 'https://www.pathofexile.com/trade/search',
        'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
    }

    if cluster_id <= 17:
        json_data = {
            'query': {
                'status': {
                    'option': 'any',
                },
                'type': 'Large Cluster Jewel',
                'stats': [
                    {
                        'type': 'and',
                        'filters': [
                            {
                                'id': 'enchant.stat_3086156145',
                                'disabled': False,
                                'value': {
                                    'max': 8,
                                },
                            },
                            {
                                'id': 'enchant.stat_3948993189',
                                'disabled': False,
                                'value': {
                                    'option': cluster_id,
                                },
                            },
                            {
                                'id': combs[0]["notableId"],
                                'disabled': False,
                            },
                            {
                                'id': combs[1]["notableId"],
                                'disabled': False,
                            },
                            {
                                'id': combs[2]["notableId"],
                                'disabled': False,
                            },
                        ],
                        'disabled': False,
                    },
                ],
                'filters': {
                    'misc_filters': {
                        'filters': {
                            'mirrored': {
                                'option': 'false',
                            },
                            'corrupted': {
                                'option': 'false',
                            },
                        },
                        'disabled': False,
                    },
                    'type_filters': {
                        'filters': {
                            'rarity': {
                                'option': 'nonunique',
                            },
                        },
                        'disabled': False,
                    },
                    'trade_filters': {
                        'filters': {
                            'indexed': {
                                'option': '3days',
                            },
                            'price': {
                                'min': 1,
                            },
                        },
                        'disabled': False,
                    },
                },
            },
            'sort': {
                'price': 'asc',
            },
        }
    elif cluster_id <= 38:
        json_data = {
            'query': {
                'status': {
                    'option': 'any',
                },
                'type': 'Medium Cluster Jewel',
                'stats': [
                    {
                        'type': 'and',
                        'filters': [],
                    },
                    {
                        'filters': [
                            {
                                'id': 'enchant.stat_3086156145',
                                'value': {
                                    'max': 5,
                                },
                                'disabled': False,
                            },
                            {
                                'id': 'enchant.stat_3948993189',
                                'value': {},
                                'disabled': False,
                            },
                            {
                                'id': combs[0]["notableId"],
                            },
                            {
                                'id': combs[1]["notableId"],
                            },
                        ],
                        'type': 'and',
                    },
                ],
                'filters': {
                    'type_filters': {
                        'filters': {
                            'rarity': {
                                'option': 'nonunique',
                            },
                        },
                        'disabled': False,
                    },
                    'misc_filters': {
                        'filters': {
                            'fractured_item': {
                                'option': 'false',
                            },
                            'mirrored': {
                                'option': 'false',
                            },
                            'split': {
                                'option': 'false',
                            },
                            'corrupted': {
                                'option': 'false',
                            },
                        },
                    },
                    'trade_filters': {
                        'filters': {
                            'price': {
                                'min': 1,
                            },
                            'indexed': {
                                'option': '3days',
                            },
                        },
                    },
                },
            },
            'sort': {
                'price': 'asc',
            },
        }

    #data = '{"query":{"status":{"option":"any"},"type":"Large Cluster Jewel","stats":[{"type":"and","filters":[]},{"filters":[{"id":"enchant.stat_3086156145","value":{"max":8},"disabled":false},{"id":"enchant.stat_3948993189","value":{"option":1},"disabled":false},{"id":"explicit.stat_567971948"},{"id":"explicit.stat_3599340381"},{"id":"explicit.stat_1152182658"}],"type":"and"}],"filters":{"type_filters":{"disabled":false,"filters":{"rarity":{"option":"nonunique"}}},"misc_filters":{"filters":{"mirrored":{"option":"false"},"corrupted":{"option":"false"}}},"trade_filters":{"filters":{"indexed":{"option":"3days"},"price":{"min":1}}}}},"sort":{"price":"asc"}}'

    # url = 'https://www.pathofexile.com/api/trade/search/' + LEAGUE + '&'.join([f'{key}={value}' for key, value in json_data.items()])
    # print(url)
    
    found_items_response = requests.post('https://www.pathofexile.com/api/trade/search/' + LEAGUE, cookies=cookies, headers=headers, json=json_data)

    try:

        res.debug(f"Headers from trade: {found_items_response.headers}")

        if 'error' in found_items_response.json():
            res.debug(f"Error while getting items with SESSID: {session_id} | Error: {found_items_response.json()}")

        return found_items_response
    
    except:

        return -1

def fetch_items(found_items, sess_id):
    res.debug(f"Fetching items with SESSID: {sess_id}")

    cookies = {
        'cf_clearance': 'Nwu_B8Zv44Uswuv7K9Qkp71S6LepExU26lRuorRYDOQ-1670605370-0-150',
        'POESESSID': sess_id,
    }

    headers = {
        'authority': 'www.pathofexile.com',
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9,hu;q=0.8',
        'referer': 'https://www.pathofexile.com/trade/search/' + LEAGUE,
        'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
    }

    # print(found_items)

    response = requests.get(
        f'https://www.pathofexile.com/api/trade/fetch/{",".join(found_items)}',
        cookies=cookies,
        headers=headers,
    )

    try:
        res.debug(f"Headers from fetch: {response.headers}")

        if 'error' in response.json():
            res.debug(f"Error while fetching items with SESSID: {sess_id} | Error: {response.json()}")

        return response

    except:
        return -1


read_sess_ids()