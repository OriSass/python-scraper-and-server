from bs4 import BeautifulSoup
import requests
from datetime import datetime, timedelta
import mydb as db

def when_to_time(when_sentence):
    sentence_arr =  when_sentence.split()
    count, day_or_hour = int(sentence_arr[0]), sentence_arr[1] 
    if 'Hour' in day_or_hour: 
        time = datetime.now() - timedelta(hours = count)
    else: time = datetime.now() - timedelta(days = count)
    return time.strftime("%Y-%m-%d %H:%M:%S")

def scrape_data(path):
    proxies = {
        'http': 'socks5://127.0.0.1:9050',
        'https': 'socks5://127.0.0.1:9050'
    }
    raw_data = requests.get(path, proxies=proxies).text
    txt_html = BeautifulSoup(raw_data, 'html.parser')
    posts = []
    rows = txt_html.find_all('tr')
    for row in rows:
        if not row.th:
            children = tuple(row.children)
            # clean new lines
            children = tuple(filter(lambda child: child != '\n', children))
            # get rid of HTML tags
            children = tuple([child.text for child in children])
            # adding time in UTC
            children += (when_to_time(children[3]),) 
            # removing the when sentence
            children = children[:3] + children[4:]
            posts.append(children)
    db.migrate()
    filtered_posts = db.reduce_duplicates(posts)
    if len(filtered_posts) > 0:
        db.insert_data(filtered_posts)
    else: print("Old news man..")
def run():
    try:
        #path = "http://nzxj65x32vh2fkhk.onion/all"
        path = "https://paste.scratchbook.ch/lists"
        scrape_data(path)
    except Exception as err:
        print(err)
