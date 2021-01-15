import re 
from bs4 import BeautifulSoup

with open('../index.html', 'r') as file :
    filedata = file.read()
    header = re.search("(?is)<header[^>]*>(.*?)<\/header>", filedata)
    menu = re.search("(?is)<table[^>]*>(.*?)<\/table>", filedata)


pages = ['talks','awards','research','teaching']

for page in pages:
	for tag in [["header",header], ['menu',menu]]:

		with open('../'+page+".html", 'r') as file :
			current_page = file.read()

		with open('../'+page+".html", 'w') as file :
			injected_list=re.sub(f"(?is)<{tag[0]}[^>]*>(.*?)<\/{tag[0]}>", tag[1].group(0), current_page)
			file.write(injected_list)