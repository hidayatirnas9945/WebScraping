from bs4 import BeautifulSoup
import requests
import re
import pandas as pd
import threading

KabupatenDict={
    "163":'BOGOR',
    "164":'SUKABUMI',
    "165":'CIANJUR',
    "166":'BANDUNG',
    "167":'GARUT',
    "168":'TASIKMALAYA',
    "169":'CIAMIS',
    "170":'KUNINGAN',
    "171":'CIREBON',
    "172":'MAJALENGKA',
    "173":'SUMEDANG',
    "174":'INDRAMAYU',
    "175":'SUBANG',
    "176":'PURWAKARTA',
    "177":'KARAWANG',
    "178":'BEKASI',
    "179":'BANDUNG BARAT',
    "180":'PANGANDARAN',
    "181":'KOTA BOGOR',
    "182":'KOTA SUKABUMI',
    "183":'KOTA BANDUNG',
    "184":'KOTA CIREBON',
    "185":'KOTA BEKASI',
    "186":'KOTA DEPOK',
    "187":'KOTA CIMAHI',
    "188":'KOTA TASIKMALAYA',
    "189":'KOTA BANJAR'
}

KabKotaList=[]
NSPPList=[]
PonPesList=[]
PendiriList=[]
AlamatList=[]
TeleponList=[]
WebsiteList=[]
SantriList=[]
DeskripsiList=[]
i=0

def getInfoPonPes(idProfile):
    SourcePonPes=requests.get(f'http://pbsb.ditpdpontren.kemenag.go.id/pdpp/{idProfile}').text
    SoupPonPes=BeautifulSoup(SourcePonPes, 'lxml')
    DataPondok=SoupPonPes.find('div', class_='desc-pondok')
    ClassPendiri=DataPondok.find_all('div', class_='pendiri-pondok')

    NamaPonPes=DataPondok.find('h3').text
    NSPP=DataPondok.find('div', class_='nspp-pondok').text.replace('NSPP', '').strip()
    Pendiri=ClassPendiri[0].text.strip()
    Alamat=ClassPendiri[1].text.strip()
    Telp=ClassPendiri[3].text.strip()
    Website=ClassPendiri[4].text.strip()
    DescPondok=re.sub(r'\s{2,}', ' ', SoupPonPes.find('div', class_='des-pondok').text).strip()
    JumlahSantri=SoupPonPes.find('h2', class_='color-green').text
    
    KabKotaList.append(nama_kab)
    NSPPList.append(str(NSPP))
    PonPesList.append(NamaPonPes)
    PendiriList.append(Pendiri)
    AlamatList.append(Alamat)
    TeleponList.append(str(Telp))
    WebsiteList.append(Website)
    SantriList.append(JumlahSantri)
    DeskripsiList.append(DescPondok)

for id_kab, nama_kab in KabupatenDict.items():
    NextPage=True
    Source=f'http://pbsb.ditpdpontren.kemenag.go.id/pdpp/loadpp?loadpp=&id_kabupaten={id_kab}&id_provinsi=32&page=1'
    while NextPage:
        SourcePage=requests.get(Source).text
        SoupPage=BeautifulSoup(SourcePage, 'lxml')
        PonPesPage=SoupPage.find_all('div', class_='nama-pondok-search')
        
        PonPesAddrList=[]
        for each in PonPesPage:
            PonPesAddrList.append(each.find('a')['href'])
          
        threads=[]
        for each in PonPesAddrList:
            t=threading.Thread(target=getInfoPonPes, args=(each,))
            threads.append(t)

        for t in threads:
            t.start()
            i+=1
            print(i)

        for t in threads:
            t.join()

        try:
            Pagination=SoupPage.find('ul', class_='pagination')
            PaginationNumber=Pagination.find_all('li')
            Source=PaginationNumber[-1].find('a')['href']
            NextPage=True
        except:
            NextPage=False

print('Retrieving data is done ...')
data={'Kabupaten/Kota':KabKotaList, 'NSPP':NSPPList, 'Pondok Pesantren':PonPesList, 'Pendiri':PendiriList, 'Alamat':AlamatList, 'Telepon':TeleponList, 'Website':WebsiteList, 'Jumlah Santri':SantriList, 'Deskripsi':DeskripsiList}
DF=pd.DataFrame(data)
DF.to_csv('Data Pondok Pesantren.csv', index=False)