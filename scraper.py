from urllib.request import urlopen as uOp
from bs4 import BeautifulSoup as suop
from time import strptime
from csv import writer
import pandas as pd
import locale
import threading
locale.setlocale(locale.LC_ALL, '')
#url open frequency
wait = 10

#url to open
url = 'https://covid19.saglik.gov.tr'

def main(url):
    #create client to open url
    client = uOp(url)
    html_cont = client.read()
    client.close()

    parse = suop(html_cont, 'html.parser')

    date_div = parse.findAll('div', {'class': 'takvim text-center'})
    date_list = date_div[0].findAll('p')

    if 'İ' in date_list[1].text:
        mnth_num = strptime(date_list[1].text.replace('İ', 'I'), '%B')
    elif 'I' in date_list[1].text:
        mnth_num = strptime(date_list[1].text.lower().replace('i', 'ı'), '%B')
    else:
        mnth_num = strptime(date_list[1].text, '%B')

    date = date_list[0].text + '.' + str(mnth_num.tm_mon) + '.' + date_list[2].text

    data_dict = {}

    tot_case_divs = parse.findAll('div', {'class': 'col-6 col-sm-6'})
    daily_case_divs = parse.findAll('div', {'class': 'col-lg-6 col-md-6 col-sm-12'})

    for i in tot_case_divs[0].div.findAll('li'):
        d_key_tot = i.findAll('span')[0].text.replace(' ', '').replace('\n', '').replace('\r', ' ').strip()
        d_val_tot = i.findAll('span')[1].text.replace('.', '')
        data_dict[d_key_tot] = int(d_val_tot)

    for i in daily_case_divs[1].div.findAll('li'):
        d_key_daily = i.findAll('span')[0].text.replace(' ', '').replace('\n', '').replace('\r', ' ').strip()
        d_val_daily = i.findAll('span')[1].text.replace('.', '')
        data_dict[d_key_daily] = int(d_val_daily)

    def append_to_csv(file_name, list_of_elem):
        with open(file_name, 'a+', newline='') as write_obj:
            csv_writer = writer(write_obj)
            csv_writer.writerow(list_of_elem)

    fin_row = [date, data_dict['TOPLAM VAKA SAYISI'], data_dict['TOPLAM VEFAT SAYISI'],
               data_dict['TOPLAM İYİLEŞEN HASTASAYISI'], data_dict['TOPLAM TEST SAYISI'],
               data_dict['BUGÜNKÜ VAKA SAYISI'], data_dict['BUGÜNKÜ İYİLEŞEN SAYISI'], data_dict['BUGÜNKÜ TEST SAYISI']]

    check_last_entry = pd.read_csv('corona.csv').iloc[-1].tolist()

    if fin_row != check_last_entry:
        append_to_csv('corona.csv', fin_row)
        print(f'Appended!')
        print(f'Last row: {check_last_entry}\n Fetched Row: {fin_row}')
    else:
        print(f'Last row is equal to fetched row. Not appended!')
        print(f'Last row: {check_last_entry}\nFetched Row: {fin_row}\n')


ticker = threading.Event()
while not ticker.wait(wait):
    main(url=url)
