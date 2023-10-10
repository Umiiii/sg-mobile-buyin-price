import requests
import logging
import datetime
import pandas as pd
from io import StringIO
import os
import csv
from  bs4 import BeautifulSoup
from lxml import etree
now = datetime.datetime.now()
nowstr = now.strftime("%Y%m%d%H%M%S")
timestr = "{}".format(nowstr)
logpath = "logs/{}.log".format(timestr)


def is_local():
    env_dict = os.environ
    return 'GITHUB_TOKEN' not in env_dict

if is_local():
    logging.basicConfig(level=logging.DEBUG,
                    filename=None,
                    datefmt='%Y/%m/%d %H:%M:%S',
                    format='%(asctime)s - %(name)s - %(levelname)s - %(lineno)d - %(module)s - %(message)s')
else:
    logging.basicConfig(level=logging.DEBUG,
                    filename=logpath,
                    datefmt='%Y/%m/%d %H:%M:%S',
                    format='%(asctime)s - %(name)s - %(levelname)s - %(lineno)d - %(module)s - %(message)s')

logger = logging.getLogger(__name__)

def fetch():
    raw_web = requests.get("https://www.mistermobile.com.sg/phone-trade-in-buy-back/")
    if raw_web.status_code == 200:
        return raw_web.text
    else:
        return ""

def parse_html_segment(raw_html_segment):
    parsed_data = []
    soup = BeautifulSoup(raw_html_segment, features="lxml")
    tables = soup.find_all('table')

    for table in tables:
        tbody = table.find('tbody')
        if not tbody:
            continue  # Skip tables without a tbody

        rows = tbody.find_all('tr')
        for row in rows:
            cells = row.find_all('td')
            cell_text = [cell.text.strip() for cell in cells]
            parsed_data.append(cell_text)
    
    return parsed_data

def parse(raw_html):
    split_idx = raw_html.find("Used Phone Trade-In Singapore")

    new_price_html = raw_html[:split_idx]
    used_price_html = raw_html[split_idx + 1:]

    new_price_data = parse_html_segment(new_price_html)
    used_price_data = parse_html_segment(used_price_html)

    return new_price_data, used_price_data

def export_to_csv(data, filename):
    try:
        with open(filename, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(data)
    except Exception as e:
        logger.error(f"An error occurred while writing to {filename}: {e}")

if __name__ == "__main__":
    logger.debug('Crawler start to run')
    raw_html_data = fetch()
    
    new_data, used_data = parse(raw_html_data)
    export_to_csv(new_data, f"{timestr}_new.csv")
    export_to_csv(used_data, f"{timestr}_used.csv")