import requests
import json
import pprint

pp = pprint.PrettyPrinter(indent=4)

api_url = 'https://en.wikipedia.org/w/api.php'


def get_links(page_title):
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

    return links


# links = get_links('Chinese Center on Long Island')
# print('num_links:', links)
