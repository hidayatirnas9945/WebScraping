from bs4 import BeautifulSoup
import requests
import re
import pandas as pd
import threading

data={
    'No':[],
    'Kabupaten Kota':[],
    'Kecamatan':[],
    'Nama Masjid':[],
    'ID Masjid':[],
    'Tipologi':[],
    'Alamat':[],
    'Luas Tanah':[],
    'Status Tanah':[],
    'Luas Bangunan':[],
    'Tahun Berdiri':[],
    'Jumlah SDM Jamaah':[],
    'Jumlah SDM Imam':[],
    'Jumlah SDM Khatib':[],
    'Jumlah SDM Muazin':[],
    'Jumlah SDM Remaja':[],
    'Telepon':[],
    'Keterangan':[]
}

def GetOneRow(tr):
    cols=0
    for td in tr.find_all('td'):
        data[list(data.keys())[cols]].append(td.text)
        cols+=1

NumberOfPage=0
addr='http://simas.kemenag.go.id/index.php/profil/masjid/page/?provinsi_id=13'
while addr:
    Source=requests.get(addr).text
    Soup=BeautifulSoup(Source, 'lxml')
    TBody=Soup.find('tbody', {'id':'the-list'})

    threads=[]
    for tr in TBody.find_all('tr'):
        GetOneRow(tr)
    
    Pagination=Soup.find('div', class_='paging')
    Pages=Pagination.find_all('a')
    addr=None
    for page in Pages:
        if page.text=='>':
            addr=page['href']
    
    NumberOfPage+=1
    print(f'Page {NumberOfPage} is done..')

df=pd.DataFrame(data)
df.to_csv('Data Masjid.csv', index=False)

