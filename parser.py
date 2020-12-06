from bs4 import BeautifulSoup
import requests
import csv
from urls_for_parsing import urls_h


def rename_title(title_bad_name):
    true_name = title_bad_name.split(' ')[3]
    true_name1 = true_name[1:]
    return true_name1


def get_html(url):
    r = requests.get(url)
    return r.text


def get_data(html):
    soup = BeautifulSoup(html, 'lxml')
    lis = soup.find_all('div', class_='center-colm')

    for li in lis:
        title_bad_name = li.find('h2').text.strip()
        title = rename_title(title_bad_name)
        tables = soup.find('div', class_='table margtab')
        trs = tables.find_all('tr')[1:]
        for tr in trs:
            tds = tr.find_all('td')
            name = tds[1].find('nobr').text
            part = tds[3].text

            data = {
                'title': title,
                'name': name,
                'part': part
            }
            write_csv(data)


def write_csv(data):
    with open('data_krasnodar.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerow([
            data['title'],
            data['name'],
            data['part'],
        ])


def main():
    for i in urls_h:
        url = i
        get_data(get_html(url))

    # Открыть для парсинга ТИК Западная г. Краснодара
    # pattern = 'http://www.krasnodar.vybory.izbirkom.ru/region/krasnodar?action=ik&vrn=423401827{}'
    # for i in range(4986, 5098, 2):
    #     url = pattern.format(str(i))
    #     get_data(get_html(url))


if __name__ == '__main__':
    main()
