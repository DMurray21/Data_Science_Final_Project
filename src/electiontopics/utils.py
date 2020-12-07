import json
from collections import defaultdict
import pandas as pd
from urllib.parse import urlparse

def load_data(datapath):
    posts = []
    with open(datapath) as fp:
        for line in fp.readlines():
            post = json.loads(line)
            posts.append(post)

    return posts

def data_to_frame(data):
    # Given data stored as list of dicts, return as pandas dataframe

    columns = data[0].keys()

    dict_for_frame = defaultdict(list)

    for column in columns:
        for datum in data:
            if column in datum.keys():
                dict_for_frame[column].append(datum[column])
            else:
                dict_for_frame[column].append('')

    return pd.DataFrame(dict_for_frame)

def extract_domain(url):
    # Given a url, return the domain name

    parsed_url = urlparse(url)
    return parsed_url.netloc