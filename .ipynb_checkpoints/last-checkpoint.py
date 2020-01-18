import asyncio
import concurrent.futures
import requests

import requests as rq
import bs4 as bs
import json
import traceback
import re
import numpy as np
import json
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
import glob, os

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'}

urls = []
def get_urls():
    with open("./news_all_lingala.txt") as f:
        for line in f :
            if line != '\n':
                urls.append(line[:-1]) 

get_urls()

final_data = []

def do_req(url):
    return requests.get(url, headers=headers)

async def main():

    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        loop = asyncio.get_event_loop()
        futures = [
            loop.run_in_executor(
                executor, 
                do_req,
                url
            )
            for url in urls
        ]
        for response in await asyncio.gather(*futures):
            soup = bs.BeautifulSoup(response.text, 'html.parser')
            # get title
            title = soup.select_one('div.col-title h1')
            description = soup.select_one('div.media-pholder--video  div.intro')
            if not description:
                description = soup.select_one('div#article-content .wsw')
                
            # news_body = news_body.text if news_body else ''
            final_data.append({'title' : title.text, 'description' : description.text})


loop = asyncio.get_event_loop()
loop.run_until_complete(main())

def save_data(data):
    with open('data_lig_full.json', 'w') as fout:
        json.dump(data, fout)
# print(final_data)
save_data(final_data)