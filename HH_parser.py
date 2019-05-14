import requests
from bs4 import BeautifulSoup as bs

headers ={'accept': '*/*',
          'user-agent': 'Chrome/71.0.3578.98'}

base_url ='https://novokuznetsk.hh.ru/search/vacancy?clusters=true&enable_snippets=true&text=Python'

def HH_parser(base_url, headers):
    jobs =[]
    session = requests.session()
    request = session.get(base_url, headers=headers)
    if request.status_code == 200:
        soup = bs(request.content,'html.parser')
        divs = soup.find_all('div', attrs={'data-qa':'vacancy-serp__vacancy'})
        for div in divs:
            title = div.find('a', attrs={'data-qa':'vacancy-serp__vacancy-title'}).text
            href = div.find('a', attrs={'data-qa':'vacancy-serp__vacancy-title'}) ['href']
            company = div.find('a', attrs={'data-qa':'vacancy-serp__vacancy-employer'}).text
            text1 = div.find('div', attrs={'data-qa':'vacancy-serp__vacancy_snippet_responsibility'}).text
            text2 = div.find('div', attrs={'data-qa':'vacancy-serp__vacancy_snippet_requirement'}).text
            content =text1 + ' '+ text2
            jobs.append(dict(title=title, href=href, company=company, content=content))

            print(content)
    else:
        print ('err: нет связи с адрессом')

HH_parser(base_url, headers)
