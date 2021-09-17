import requests
import urllib.parse as turnUrlCode
from bs4 import BeautifulSoup
def get_Serch_Result(keyword):
    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36 Edg/93.0.961.47'}
    serchUrl='https://www.635book.com/modules/article/search.php?keywords=all&searchkey='
    keyword='凡人修仙传'.encode('GBK')
    targetUrl=serchUrl+turnUrlCode.quote(keyword)+'&submit=%CB%D1%CB%F7'
    resp=requests.get(targetUrl, headers=headers)
    if resp.status_code==200:
        htmlSoup= BeautifulSoup(resp.content.decode('GBK'),'lxml')
        novels=htmlSoup.find_all('ul',class_='other_s')[0].find_all('li')
        if novels:
            return novels
        else: print('Err: No result found')
    else: print('Err: requests failed')
get_Serch_Result(1)