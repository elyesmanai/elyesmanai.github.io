import re 
from bs4 import BeautifulSoup

with open('../index.html', 'r', encoding='utf-8') as file :
    filedata = file.read()
    header = re.search("(?is)<header[^>]*>(.*?)<\/header>", filedata)
    menu = re.search("(?is)<table[^>]*>(.*?)<\/table>", filedata)


pages = ['talks','awards','research','teaching','career', 'content']

for page in pages:
	for tag in [["header",header], ['table',menu]]:

		with open('../'+page+".html", 'r',encoding='utf-8') as file :
			current_page = file.read()

		with open('../'+page+".html", 'w',encoding='utf-8') as file :
			injected_list=re.sub(f"(?is)<{tag[0]}[^>]*>(.*?)<\/{tag[0]}>", tag[1].group(0), current_page)
			file.write(injected_list)