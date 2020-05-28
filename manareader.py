import os
import re
import shutil
import requests 
import threading
import urllib.request
from tqdm import tqdm
from urllib.error import HTTPError
from bs4 import BeautifulSoup as BS

name = "kuroko-no-basket"
start_chapter = 1
end_chapter = 275
base_url = "http://www.mangareader.net/" + name + "/"


def dowload_images(chapter,page_num):
    page = base_url + str(chapter) + '/' + str(page_num)
    html = urllib.request.urlopen(page).read()
    soup = BS(html, features="html5lib")
    for imgtag in soup.find_all('img'):
        f = open(name+"/"+str(chapter)+"/"+str(page_num)+'.jpg','wb') 
        f.write(requests.get(imgtag["src"]).content)
        f.close()


if __name__ == "__main__":
    if not os.path.exists(name):
      os.makedirs(name)

    for chapter in tqdm(range(start_chapter, end_chapter+1)):
        if os.path.exists(name + '/' + str(chapter)):
            shutil.rmtree(name+"/"+str(chapter)+"/")
        os.makedirs(name + '/' + str(chapter))
        first_page = base_url + str(chapter) + '/1'
        html = urllib.request.urlopen(first_page).read()
        soup = BS(html,features="html5lib")
        max_pages = soup.find_all("option")[-1].text
        threads = list()
        for index in range(1,int(max_pages)+1):
            thread = threading.Thread(target=dowload_images, args=(chapter, index))
            threads.append(thread)
            thread.start()
        
        for thread in threads:
            thread.join()