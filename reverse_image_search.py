#!/usr/bin/env python
# coding: utf-8

# In[15]:


import requests
import webbrowser
import urllib.request
from urllib.request import Request, urlopen
from http.cookiejar import CookieJar
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import re
import shutil
import glob
import os


# In[21]:


def collect_similar_images():
    try:
        my_dir="E:/Jupyter Lab/Image similarity/videos_frames"
    #     print("hi")
        for filePath in glob.iglob(my_dir+'/*.*'):
            dir_name=os.path.splitext(os.path.basename(filePath))[0]
            print(dir_name)
    #         filePath = "E:\\Jupyter Lab\\Image Similarity upwork assignment\\images_batter\\cv_3.png"
            searchUrl = 'http://www.google.hr/searchbyimage/upload'
            multipart = {'encoded_image': (filePath, open(filePath, 'rb')), 'image_content': ''}
            response = requests.post(searchUrl, files=multipart, allow_redirects=False)
            fetchUrl = response.headers['Location']
            cj=CookieJar()
            opener=urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
            opener.addheaders=[('User-agent', 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17')]
            sourcecode=opener.open(fetchUrl).read()
            soup = BeautifulSoup(sourcecode, "lxml")
            links = []
            for link in soup.findAll('a'):
                links.append(link.get('href'))
            r=[]
            for l in links:
                if str(l).startswith("/search?q=") and str(l).find('=simg')>=0:
                    r.append(l)
            mainurl='http://www.google.hr'
            secUrl=mainurl+r[0]
            sourcecode=opener.open(secUrl).read()
            soup = BeautifulSoup(sourcecode, "lxml")
            links = []
            for link in soup.findAll('img'):
                links.append(link.get('data-src'))
            os.chdir("E:/Jupyter Lab/Image similarity/Similar_images")
            if not os.path.exists(dir_name):
                os.mkdir(dir_name)
            num=1
            for url in links:
                if str(url)!="None":
                    filename1=str(num)+'.jpg'
                    r = requests.get(url, stream = True)
                    # Check if the image was retrieved successfully
                    if r.status_code == 200:
                        # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
                        r.raw.decode_content = True

                        # Open a local file with wb ( write binary ) permission.
                        with open(filename1,'wb') as f:
                            f1=os.path.join(dir_name,filename1)
                            shutil.copyfileobj(r.raw,f)
                        shutil.copy(filename1, f1)

                        print('Image sucessfully Downloaded: ',filename1)
                        num=num+1
                    else:
                        print('Image Couldn\'t be retreived')
    except Exception as e:
        print(e)
        print(e.with_traceback)






