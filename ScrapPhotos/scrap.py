from bs4 import BeautifulSoup
from urllib2 import urlopen
import urllib
import urllib2

def make_soup(url):
	hdr = {'User-Agent':'Mozilla/5.0'}
	req = urllib2.Request(url,headers=hdr)
	html = urllib2.urlopen(req).read()
	return BeautifulSoup(html)

def get_images(url):
    soup = make_soup(url)
    i=0
    images = [img for img in soup.findAll('img')]
    print (str(len(images)) + "images found.")
    print 'Downloading images to current working directory.'
    image_links = [each.get('src') for each in images]
    for each in image_links:
        i=i+1
        if i>40:
        	print('exceed limit. Exiting')
        	exit()
        filename=each.split('/')[-1]
        urllib.urlretrieve(each, filename)
    return image_links


get_images('https://www.google.com/search?q=paintings&client=ubuntu&hs=iBH&channel=fs&source=lnms&tbm=isch&sa=X&ved=0ahUKEwj9gKKvopviAhUv7HMBHSgjAxMQ_AUIDigB&biw=1366&bih=668')
