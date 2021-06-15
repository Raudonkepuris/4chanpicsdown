#!/usr/bin/python

import sys
import requests
from bs4 import BeautifulSoup
import urllib
import os
import yaml
from tqdm import tqdm

#path of conf file
CONFIG_PATH = "/home/liut/.config/4chanpicsdown.yaml" 

def main(argv):
    #turns argv to str
    url = ''.join(argv)

    #gets page
    html_page = requests.get(url)
    soup = BeautifulSoup(html_page.content, 'html.parser')
    #checks if page is up
    if html_page.status_code > 400:
        print("Page returned " + html_page.status_code + ", exiting")
        exit()

    #opens conf file
    with open(CONFIG_PATH) as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
        #sets picture path to one in config file
        pic_path = data['default-path']

    
    split_url = url.split('/')
    #this rough check exists because when spliiting by '/' it creates list containing:
    #'https', '', *4chanlink*, *board name*, 'thread', *thread num*
    #and this scripts uses the board name and thread num to create dirs
    if len(split_url) != 6:
        print("Doesn't conform with standart 4chan link, exiting")
        exit()

    pic_path += '/' + split_url[3] + '/' + split_url[5]

    imgs = soup.findAll('a', {'class': 'fileThumb'})

    os.makedirs(pic_path)
    
    #downloads imgs
    for img in tqdm(imgs):
        img_url = "https:" + img['href']

        split_img_url = img_url.split('/')

        img_down = requests.get(img_url)
        file = open(pic_path + '/' + split_img_url[-1], "wb")
        file.write(img_down.content)
        file.close()    

if __name__=="__main__":
    main(sys.argv[1:2])