# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
import json
from datetime import datetime
import re
from bs4 import BeautifulSoup
import requests

# %% [markdown]
# # Task 1 Get the link of each Vikings Season

# %%
base_url = 'https://en.wikipedia.org/'
main_page_url = 'wiki/Vikings_(2013_TV_series)#Season_1'


def get_links(url):
    r = requests.get(url)
    webpage = BeautifulSoup(r.content)
    url_list = []
    links = webpage.find_all('div', class_='hatnote')
    for link in links:
        url = link.find('a')
        url_list.append(base_url + url['href'])
    return url_list[2:-3]


links = get_links(base_url + main_page_url)
links

# %% [markdown]
# # Task 2 Get the information of the info box on each page

# %%


def get_content(row):
    data = row.find('td')
    if data.find('li') is not None:
        return [li.get_text() for li in data.find_all('li')]
    else:
        return data.get_text().replace('\xa0', ' ')


def get_info_box(url):
    r = requests.get(url)
    page = BeautifulSoup(r.content)
    info_box = page.find('table', class_='infobox vevent')
    dicts = {}
    for index, row in enumerate(info_box.select('tr')[:-2]):
        if index == 0:
            dicts['title'] = row.get_text()
        elif index == 1:
            dicts['season'] = row.get_text()
        elif index == 2:
            continue
        elif row.get_text() == 'Release':
            continue
        else:
            key = row.find('th', class_='infobox-label')
            if key is not None:
                dicts[key.get_text()] = get_content(row)

    return dicts


# %%
list_info = [get_info_box(link) for link in links]
list_info


# %%
# Change season and n. of epidode to int
for index, movie in enumerate(list_info):
    movie['season'] = index + 1
    movie['No. of episodes'] = int(movie['No. of episodes'])
    if len(movie['Original release']) == 2:
        movie['Original release'] = movie['Original release'][0]
    elif len(movie['Original release']) == 4:
        movie['Original release'] = movie['Original release'][::2]


# %%
list_info[-1]['Original release'] = list_info[-1]['Original release'][::2]


# %%
movie_info = list_info.copy()


# %%


def convert_to_datetime(input_date):
    fmt = '%Y-%m-%d'
    if len(input_date) == 2:
        dicts = {}
        for i, s in enumerate(input_date):
            date = s.strip()[1:-1]
            dicts[f"part {i+1}"] = datetime.strptime(date, fmt)
        return dicts
    elif isinstance(input_date, str):
        date = item.strip()[1:-1]
        return datetime.strptime(date, fmt)


movie_info


# %%

json.dump(movie_info, open('vikings.json', 'w'), default=str)


# %%
