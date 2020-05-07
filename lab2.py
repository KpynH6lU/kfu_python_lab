from urllib.request import urlopen
from bs4 import BeautifulSoup as bs
import requests as req
from urllib.parse import quote


url = 'https://allfind.kpfu.ru/Search/Results?lookfor={}&type=AllFields'
query_text = input('Введите запрос для поиска книг:   ')
search_url = url.format(quote(query_text))
resp = urlopen(search_url)
soup = bs(resp, "html.parser")
books = soup.find_all('div', {'class': 'result clearfix'})
for book in books:
    block = book.find('div', {'class': 'record-title'}).find('a')
    response = req.get('https://allfind.kpfu.ru' + block['href'] + '/Holdings#tabnav')
    soup = bs(response.text, 'html.parser')
    title = soup.find('h3').text
    print('Название: ', title)
    authors = soup.find('tr').find('td').text
    print('Авторы: ', authors.strip())
if not books:
    print('По данному запросу ничего не найденно!')
