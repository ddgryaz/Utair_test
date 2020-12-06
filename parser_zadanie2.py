from bs4 import BeautifulSoup
import csv


def rename_uik_number(uik_bad_name):
    true_name = uik_bad_name.split(' ')[1:]
    true_name1 = ''.join(true_name)[1:]
    return true_name1


def rename_part(part_bad):
    true_val = part_bad.split('\n')[1]
    true_val1 = true_val[:-1]
    return true_val1


def get_data():
    data = {"uiks": [], "parts": []}
    for i in range(2, 40):
        f = open(f'sites/{i}.html', 'r').read()
        soup = BeautifulSoup(f, 'lxml')
        body = soup.find('body')
        table = body.find('table', width="100%", cellpadding="0", height="80%").find('tbody')
        trs = table.find('tr', height="100%")
        table2 = trs.find('table', style="width:100%;border-color:#000000").find('tbody').find('tr',
                                                                                               style="height:100%")
        table3 = table2.find('td', width="90%").find('div', style="width:100%; bgcolor:white;overflow:scroll").find(
            'table').find('tbody')
        ntr = table3.find('tr', valign="top")
        tds = ntr.find_all('td')
        for td in tds:
            uik_bad_name = td.find('nobr').find('a').text
            uik_name = rename_uik_number(uik_bad_name)
            data["uiks"].append(uik_name)
            # return data
        vtr = table3.find_all('tr')[18:]
        for vt in vtr:
            tds = vt.find_all('td')
            for td in tds:
                part_bad = td.text
                part = rename_part(part_bad)
                data["parts"].append(part)
    return data


def write_csv():
    data = get_data()
    with open('data_zadanie2.csv', 'a') as f:
        fieldnames = ['№ УИКа', '% за КПРФ']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        # writer.writeheader()
        new_data = zip(data["uiks"], data["parts"])
        for row in new_data:
            writer.writerow({fieldnames[0]: row[0], fieldnames[1]: row[1]})


def main():
    write_csv()


if __name__ == '__main__':
    main()
