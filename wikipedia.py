import requests
import json
import pprint
import pickle
import os

pp = pprint.PrettyPrinter(indent=4)

api_url = 'https://en.wikipedia.org/w/api.php'

dump_file = 'neighbors_dump.pl'
memo = None


def get_links(page_title):
    global memo
    if memo == None and os.path.isfile(dump_file):
        memo = pickle.load(open(dump_file, "rb"))
    elif memo == None:
        memo = {}

    if page_title in memo:
        return memo[page_title]

    params = {
        'action': 'query',
        'prop': 'links',
        'titles': page_title,
        'format': 'json',
        'pllimit': 500
    }

    links = []
    res = requests.get(api_url, params=params)

    res_dict = json.loads(res.content)
    if ('-1' in res_dict['query']['pages']):
        return []

    link_list = [el['title']
                 for el in list(res_dict['query']['pages'].values())[0]['links']]
    links.extend(link_list)
    while 'continue' in res_dict and len(res_dict['continue']['plcontinue']) > 2:
        plcontinue = res_dict['continue']['plcontinue']
        params.update({'plcontinue': plcontinue})
        res = requests.get(api_url, params=params)
        res_dict = json.loads(res.content)
        link_list = [el['title'] for el in list(
            res_dict['query']['pages'].values())[0]['links']]

        links.extend(link_list)

    memo[page_title] = links
    pickle.dump(memo, open(dump_file, "wb"))

    return links


def get_random_title():
    params = {
        'action': 'query',
        'format': 'json',
        'list': 'random',
        'rnfilterredir': 'nonredirects',
        'rnnamespace': 0,
        'rnlimit': 1
    }
    res = json.loads(requests.get(api_url, params=params).text)[
        'query']['random'][0]['title']
    return res
