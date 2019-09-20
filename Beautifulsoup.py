import requests
from bs4 import BeautifulSoup    
page_source = requests.get('https://russelljohn.net/journal/2011/01/50-quotable-quotes-under-140-characters/')
s=''
li=[]
#print(soup.find('title').text)
soup = BeautifulSoup(page_source.text,"lxml")
f = open("myfile.txt", "r+")
f.write(soup.find('article').text)
position = f.seek(0, 0);
s=f.read()
#print(s)
li=s.split(".")
o=open("file3.txt","w")
for i in li:
	o.write(i)
	o.write('\n')
