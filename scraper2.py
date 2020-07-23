"""
Scrape web data for url, phone and emails. Leave out duplicates.
Include Href and Img tag urls.
"""


__author__ = 'Haley Collard'


import re
import sys
import argparse
import requests
from html.parser import HTMLParser

tl = []


class URL_Parser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        for attr in attrs:
            if tag == 'href':
                tl.append(attr)
            if tag == 'img':
                if attr[0] == 'src':
                    tl.append(attr[1])


def create_parser():
    parser = argparse.ArgumentParser(
        description="Scrape web for data.")
    parser.add_argument('url', help='website to scrape')
    return parser


def main(args):
    global tl
    parser = create_parser()
    ns = parser.parse_args()
    url = ns.url
    url_parser = URL_Parser()
    html = requests.get(url).text
    url_parser.feed(html)
    url_pattern = r'href=("(https?:\/\/)?(www\.)?\w+\.\S+)"'
    email_pattern = r"([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)"
    phone_pattern = r'[(\d]?\d{3}[-.()]?\d{3}[-.]?\d{4}'
    urls = re.findall(url_pattern, html)
    tl.append(urls)
    unique_urls = set(tl)
    emails = re.findall(email_pattern, html)
    unique_emails = set(emails)
    phone_nums = re.findall(phone_pattern, html)
    unique_phone_nums = set(phone_nums)
    print('URLS:')
    for url in unique_urls:
        print(url[0])
    print('EMAILS:')
    for email in unique_emails:
        print(email)
    print('PHONE NUMBERS:')
    for phone_num in unique_phone_nums:
        print(phone_num)


if __name__ == '__main__':
    main(sys.argv[1:])
