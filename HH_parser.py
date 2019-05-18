import time
import csv
import requests
from bs4 import BeautifulSoup as bs

headers ={'accept': '*/*',
          'user-agent': 'Chrome/71.0.3578.98'}

base_url ='https://novokuznetsk.hh.ru/search/vacancy?clusters=true&enable_snippets=true&text=Python&area=1202&from=cluster_area'

def HH_parser(base_url, headers):
    jobs =[]
    urls =[]
    urls.append(base_url)

    session = requests.session()
    request = session.get(base_url, headers=headers)
    if request.status_code == 200:
        start = time.time() #запускаем таймер модуль time
        #soup = bs(request.content,'html.parser') #дефолтный парсер python
        soup = bs(request.content,'lxml') # парсер lxml +53%

        '''обработка нескольких страниц'''

        try:
            pagination = soup.find_all('a', attrs={'data-qa':'pager-page'})
            count = int(pagination[-1].text)
            for i in range(count):
                '''краткая форма записи ('dosome {1},format 1=i)'''
                url =f'https://novokuznetsk.hh.ru/search/vacancy?clusters=true&enable_snippets=true&text=Python&area=1202&from=cluster_area&page={i}'
                if url not in urls:
                    urls.append(url)
        except:
            pass

    for url in urls:
        request = session.get(url, headers=headers)
        soup = bs(request.content, 'lxml')
        divs = soup.find_all('div', attrs={'data-qa':'vacancy-serp__vacancy'})
        for div in divs:
            try:
                title = div.find('a', attrs={'data-qa':'vacancy-serp__vacancy-title'}).text
                href = div.find('a', attrs={'data-qa':'vacancy-serp__vacancy-title'}) ['href']
                company = div.find('a', attrs={'data-qa':'vacancy-serp__vacancy-employer'}).text
                text1 = div.find('div', attrs={'data-qa':'vacancy-serp__vacancy_snippet_responsibility'}).text
                text2 = div.find('div', attrs={'data-qa':'vacancy-serp__vacancy_snippet_requirement'}).text
                content =text1 + ' '+ text2
                jobs.append(dict(title=title, href=href, company=company, content=content))
            except:
                pass
        #finish = time.time()
        #resalt = finish - start
        #print ('lxml = '+str(resalt))
        #print(len(jobs))
        #for i in pagination :
        #    print(i)
        #print (pagination[-1].text) #последнее значение извлекаем текст
    else:
        print ('error o done status code = '+str(request.status_code))
    return jobs


def files_write (jobs):
    with open('parser_jobs.csv','w', newline='') as file:
        #a_pen = csv.writer(file)
        #a_pen.writerow(('название вакансии', 'URL', 'компания', 'описание'))
        #TypeOut =['title', 'href', 'company', 'content']
        a_pen = csv.writer(file, delimiter = ';')
        a_pen.writerow(('название вакансии', 'URL', 'компания', 'описание'))

        for job in jobs:
            try:
                a_pen.writerow((job['title'], job['href'], job['company'], job['content']))
            except:
                pass


jobs = HH_parser(base_url, headers)
files_write (jobs)
