import requests
from bs4 import BeautifulSoup as BS
from random import randint

headers = [
    {'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:47.0) Gecko/20100101 Firefox/47.0',
     'Accept': 'text/html, application/xhtml+xml,aplication/xml;q=0.9,*/*;q=0.8'},
    {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0',
     'Accept': 'text/html, application/xhtml+xml,aplication/xml;q=0.9,*/*;q=0.8'},
    {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X x.y; rv:42.0) Gecko/20100101 Firefox/42.0',
     'Accept': 'text/html, application/xhtml+xml,aplication/xml;q=0.9,*/*;q=0.8'}
]


def work(url: str):
    domain = 'https://www.work.ua/'
    resp = requests.get(url, headers=headers[randint(0, 2)])

    jobs = []
    errors = []

    if resp.status_code == 200:
        soup = BS(resp.content, 'html.parser')
        main_div = soup.find('div', id='pjax-job-list')
        div_list = main_div.find_all('div', attrs={'class': 'job-link'})
        if main_div:
            for div in div_list:
                title = div.find('h2')
                href = title.a['href']
                description = div.p.text
                company = 'No name'
                logo = div.find('img')
                if logo:
                    company = logo['alt']
                jobs.append({'title': title.text,
                             'url': domain + href,
                             'descriptions': description,
                             'company': company
                             })
        else:
            errors.append({'url': url, 'title': 'Div does not exist'})
    else:
        errors.append({'url': url, 'title': 'Page do not response'})

    return jobs, errors
