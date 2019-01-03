

'''Делаю парсинг книжного магазина-песочницы http://books.toscrape.com/ 
с сохранением результатов в csv-файл и дальнейшим анализом данных'''

from urllib.request import urlopen
from urllib.error import HTTPError
from datetime import datetime

from bs4 import BeautifulSoup
from csvsaver import csv_write_books_data

URL = 'http://books.toscrape.com/'

def get_html(url):
    try:
        html = urlopen(url)
    except HTTPError as e:
        print(e)
        return None
    else:
        return html

def get_soup(html):
    try:
        soup = BeautifulSoup(html.read(), 'lxml')
    except Exception as e:
        print(e)
        return None
    return soup



def get_page_data(soup):
    
    def get_rate_of_book(item):
        rate_words = {'One' : 1, 
                      'Two' : 2, 
                      'Three' : 3,
                      'Four' : 4,
                      'Five' : 5}
        rate_word = item.find('p').get('class')[1]
        rate = rate_words[rate_word]
        return rate
    
    def get_genre(item):
        link = item.find('a').get('href')
        book_page = get_soup(get_html(URL + 'catalogue/' + link))
        path = book_page.find('ul', {'class' : 'breadcrumb'}).find_all('a')
        genre = path[-1].text
        return genre

    if soup is not None:
        body = soup.find('body')
        row = body.find('ol', {'class' : 'row'})
        books_infos = []
        row_items = row.find_all('li')
        for item in row_items:
            genre = get_genre(item)
            title = item.find('h3').find('a').get('title')
            price = item.find('div', {'class' : 'product_price'}).find('p', 'price_color').text
            rate = get_rate_of_book(item)
            book_info = {
                'title' : title,
                'price' : price,
                'genre' : genre,
                'rate' : rate
            }
            books_infos.append(book_info)

    return books_infos

def get_pages_count(soup):
    if soup is not None:
        pages_count = soup.find('ul', {'class' : 'pager'}).find('li', {'class' : 'current'}).text.split()[-1]
        return pages_count

def main():
    start = datetime.now()
    all_books_data = []
    count = get_pages_count(get_soup(get_html(URL)))
    for i in range(1, int(count) + 1):
        books_from_one_page = get_page_data(get_soup(get_html(URL + 'catalogue/page-' + str(i) + '.html')))
        for book in books_from_one_page:
            all_books_data.append(book)
    csv_write_books_data(all_books_data)
    end = datetime.now()
    elapsed = end - start
    print('elapsed time {}'.format(elapsed))

if __name__ == '__main__':
    main()
