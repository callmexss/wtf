import os
import pickle

import click
import requests
import bs4

from prettytable import PrettyTable


URL = "https://www.abbreviations.com/serp.php?st={}&p={}"
CACHE_FILE = "wtf.pkl"
CACHE = {}


def init():
    if not os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "wb") as f:
            pass
    else:
        with open(CACHE_FILE, "rb") as f:
            global CACHE
            CACHE = pickle.load(f)


def get_content(key, page):
    """Get content from abbreviations.com.

    key, abbreviation
    page, show how many pages of results, 99999 for all
    """
    url = URL.format(key, page)
    response = requests.get(url)
    return response.text


def parse_content(content):
    soup = bs4.BeautifulSoup(content, "lxml")
    term = soup.select_one("td.tal.tm.fsl > a")
    definitions = soup.select("td.tal.dx.fsl > p.desc")
    ratings = soup.select("#abbr-rate")

    info = []

    for definition, rating in zip(definitions, ratings):
        rating = len(rating.select("#abbr-rate > span.sf"))

        data = {
            'term': term.get_text(),
            'definition': definition.get_text(),
            'rating': rating,
        }

        info.append(data)

    info.sort(key=lambda x: x['rating'], reverse=True)
    return info


def show_content(content):
    flag = False
    for piece in content:
        if not flag:
            for k in piece.keys():
                print(k.center(10), end="\t\t")
            print()
            flag = True

        for v in piece.values():
            print(str(v).center(10), end="\t\t")
        print()


def show_content_as_table(content):
    if not content:
        print("Query does not found.")
        return

    flag = False

    for piece in content:
        if not flag:
            pt = PrettyTable(piece.keys())
            flag = True
        pt.add_row(piece.values())

    print(pt)


def test():
    content = get_content("KPI", 1)
    content = parse_content(content)
    show_content_as_table(content)


@click.command()
@click.option('--page', default=1, help="how many pages of results to show")
@click.argument('key', default="NBA")
def wtf(key, page):
    if not 0 <= page <= 99999:
        return "Invalid Page."

    init()

    if (key, page) in CACHE:
        content = CACHE[(key, page)]
    else:
        content = get_content(key, page)
        content = parse_content(content)
        CACHE[(key, page)] = content

        with open(CACHE_FILE, "wb") as f:
            pickle.dump(CACHE, f)

    show_content_as_table(content)


if __name__ == '__main__':
    wtf()
