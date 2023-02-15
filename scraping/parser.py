import requests
from bs4 import BeautifulSoup as BS
from random import randint

__all__ = ('work', 'rabota', 'dou', 'djinni')

headers = [
    {'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:47.0) Gecko/20100101 Firefox/47.0',
     'Accept': 'text/html, application/xhtml+xml,aplication/xml;q=0.9,*/*;q=0.8'},
    {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0',
     'Accept': 'text/html, application/xhtml+xml,aplication/xml;q=0.9,*/*;q=0.8'},
    {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X x.y; rv:42.0) Gecko/20100101 Firefox/42.0',
     'Accept': 'text/html, application/xhtml+xml,aplication/xml;q=0.9,*/*;q=0.8'}
]


def work(url: str, city: str = None, language: str = None):
    domain = 'https://www.work.ua'
    resp = requests.get(url, headers=headers[randint(0, 2)])

    jobs = []
    errors = []
    if url:
        if resp.status_code == 200:
            soup = BS(resp.content, 'html.parser')
            main_div = soup.find('div', id='pjax-job-list')
            div_list = main_div.find_all('div', attrs={'class': 'job-link'})
            if main_div:
                for div in div_list:
                    title = div.find('h2')
                    href = title.a['href']
                    description = div.p.text
                    company = div.find('div', attrs={'class': 'add-top-xs'}).find('span').b.text
                    jobs.append({'title': title.text,
                                 'url': domain + href,
                                 'description': description,
                                 'company': company,
                                 'city_id': city,
                                 'language_id': language
                                 })
            else:
                errors.append({'url': url, 'title': 'Div does not exist'})
        else:
            errors.append({'url': url, 'title': 'Page do not response'})

    return jobs, errors


def rabota(url: str, city: str = None, language: str = None):
    domain = 'https://rabota.ua/'
    resp = requests.get(url, headers=headers[randint(0, 2)])

    jobs = []
    errors = []
    if url:
        if resp.status_code == 200:
            data = resp.json()
            if data:
                for d in data['documents']:
                    full_url = None
                    if d.get('notebookId') and d.get('id'):
                        full_url = f"{domain}company{d['notebookId']}/vacancy{d['id']}"

                    jobs.append({
                        'title': d.get('name'),
                        'company': d.get('companyName'),
                        'url': full_url,
                        'description': d.get('description'),
                        'city_id': city,
                        'language_id': language
                    })
            else:
                errors.append({'url': url, 'title': 'Data does not exist'})
        else:
            errors.append({'url': url, 'title': 'Page do not response'})

    return jobs, errors


def dou(url: str, city: str = None, language: str = None):
    resp = requests.get(url, headers=headers[randint(0, 2)])

    jobs = []
    errors = []
    if url:
        if resp.status_code == 200:
            soup = BS(resp.content, 'html.parser')
            main_div = soup.find('div', id='vacancyListId')

            if main_div:
                li_list = main_div.find_all('li', attrs={'class': 'l-vacancy'})
                for li in li_list:
                    _title = li.find('div', attrs={'class': 'title'}).a
                    title = _title.text
                    href = _title['href']
                    company = li.find('a', attrs={'class': 'company'}).text  # .strip()
                    description = li.find('div', attrs={'class': 'sh-info'}).text  # .strip()

                    jobs.append({'title': title,
                                 'url': href,
                                 'description': description,
                                 'company': company,
                                 'city_id': city,
                                 'language_id': language
                                 })
            else:
                errors.append({'url': url, 'title': 'Div does not exist'})
        else:
            errors.append({'url': url, 'title': 'Page do not response'})

    return jobs, errors


def djinni(url: str, city: str = None, language: str = None):
    domain = 'https://djinni.co'
    resp = requests.get(url, headers=headers[randint(0, 2)])

    jobs = []
    errors = []
    if url:
        if resp.status_code == 200:
            soup = BS(resp.content, 'html.parser')
            main_ul = soup.find('ul', attrs={'class': 'list-jobs'})
            li_list = main_ul.find_all('li', attrs={'class': 'list-jobs__item'})
            if main_ul:
                for li in li_list:
                    link = li.find('div', attrs={'class': 'list-jobs__title'})
                    title = link
                    href = link.a['href']
                    description = li.find('div', attrs={'class': 'truncated mw-100 fz-16 mb-0 js-show-more'})
                    company = li.find('div', attrs={'class': 'list-jobs__details__info'}).a

                    jobs.append({'title': title.text,
                                 'url': domain + href,
                                 'description': description.text,
                                 'company': company.text,
                                 'city_id': city,
                                 'language_id': language
                                 })
            else:
                errors.append({'url': url, 'title': 'Div does not exist'})
        else:
            errors.append({'url': url, 'title': 'Page do not response'})

    return jobs, errors
