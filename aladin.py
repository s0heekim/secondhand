import requests
from bs4 import BeautifulSoup


def get_soup(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup


def get_last_page(url):
    soup = get_soup(url)
    try:
        last_page = soup.select('div.numbox_last a')[0].get('href').split("'")[-2]
        last_page = int(last_page)
    except:
        last_page = 1
    return last_page


def extract_books(url, last_page):
    books = []
    for page in range(last_page):
        current_page_url = f'{url}&page={page+1}'
        soup = get_soup(current_page_url)
        print(f'Scrapping Aladin: Page {page}')

        book_list = soup.find_all('div', 'ss_book_box')
        for item in book_list:
            title = item.find('a', 'bo3').b.get_text()
            publication_info_group = item.ul.li.next_sibling.next_sibling.get_text().split(' | ')
            author = ''
            publisher = ''
            publish_date = ''

            for publication_info in publication_info_group:
                if '(지은이)' in publication_info:
                    author = publication_info
                elif '년' in publication_info and '|' in publication_info:
                    publish_date = publication_info
                else:
                    publisher = publication_info

            book = {'title': title, 'author': author, 'publisher': publisher, 'publish_date': publish_date}

            store_list = item.select('td:last-child tr:last-child th')
            for store in store_list:
                store = store.get_text().split(' (')[0]
                if store == '새책':
                    book['new_book_price'] = None
                    book['new_book_link'] = None
                elif store == 'eBook':
                    book['ebook_price'] = None
                    book['ebook_link'] = None
                elif store == '알라딘 중고':
                    book['aladin_price'] = None
                    book['aladin_link'] = None
                elif store == '이 광활한 우주점':
                    book['universe_price'] = None
                    book['universe_link'] = None
                elif store == '판매자 중고':
                    book['seller_price'] = None
                    book['seller_link'] = None

            book_keys = list(book.keys())[4:]

            goto_list = item.select('td:last-child tr:last-child td td td')
            for i, td in enumerate(goto_list):
                price = td.get_text().split('-')[0]
                link = td.find('a')
                if link:
                    link = link.get('href')
                else:
                    link = None
                book[f'{book_keys[0]}'] = price
                book[f'{book_keys[1]}'] = link
                book_keys = book_keys[2:]

            books.append(book)
    return books


def get_books(keyword):
    url = f'https://www.aladin.co.kr/search/wsearchresult.aspx?SearchTarget=Used&KeyWord={keyword}&ViewRowCount=50'
    last_page = get_last_page(url)
    books = extract_books(url, last_page)
    return books
