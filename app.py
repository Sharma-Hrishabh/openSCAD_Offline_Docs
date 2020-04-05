import os, sys
import requests
from urllib.parse import urljoin, unquote
from bs4 import BeautifulSoup

def soupfindAllnSave(pagefolder, url, soup, tag2find='img', inner='src'):
    if not os.path.exists(pagefolder):
        os.mkdir(pagefolder)
    for res in soup.findAll(tag2find):  
        try:
            filename = os.path.basename(res[inner])
            filename = unquote(filename)
            fileurl = urljoin(url, res.get(inner))

            filepath = os.path.join(pagefolder, filename)
            res[inner] = filepath
            
            if not os.path.isfile(filepath): # was not downloaded
                with open(filepath, 'wb') as file:
                    filebin = session.get(fileurl)
                    file.write(filebin.content)
        except Exception as exc:      
            print(exc)
    return soup

def savePage(response, pagefilename='page'):    
   url = response.url
   soup = BeautifulSoup(response.text, "lxml")
   pagefolder = pagefilename+'_files' # page contents 
   soup = soupfindAllnSave(pagefolder, url, soup, 'img', inner='src')
   
   soup.find('div', id="contentSub").decompose()
   soup.find('div', id="footer").decompose()
   soup.find('div', id="mw-navigation").decompose()
   for div in soup.find_all(True, {'class':['noprint','metadata plainlinks ambox ambox-notice', 'mw-jump-link']}):
       div.decompose()
      
   with open(pagefilename+'.html', 'w') as file:
      file.write(soup.prettify())
   return soup



session = requests.Session()

response = session.get('https://en.wikibooks.org/w/index.php?title=OpenSCAD_User_Manual/Print_version&printable=yes')
savePage(response, 'openSCAD_Manual')

response = session.get('https://en.wikibooks.org/w/index.php?title=OpenSCAD_User_Manual/The_OpenSCAD_Language&printable=yes')
savePage(response, 'openSCAD_Language')

