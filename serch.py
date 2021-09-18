import urllib.parse as turnUrlCode

import requests
from bs4 import BeautifulSoup
import datetime,time

def get_Search_Result(keyword):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36 Edg/93.0.961.47'}
    serchUrl = 'https://www.635book.com/modules/article/search.php?keywords=all&searchkey='
    keyword = keyword.encode('GBK')
    targetUrl = serchUrl+turnUrlCode.quote(keyword)+'&submit=%CB%D1%CB%F7'
    resp = requests.get(targetUrl, headers=headers)
    if resp.status_code == 200:
        htmlSoup = BeautifulSoup(resp.content.decode('GBK'), 'lxml')
        novelNum = len(htmlSoup.find_all(
            'ul', class_='other_s')[0].find_all('li'))
        if novelNum > 0:
            return htmlSoup
        else:
            print('Err: No result found')
            return None
    else:
        print('Err: requests failed')
        return None


def decode_Search_Result(htmlSoup):
    baseUrl = 'https://www.635book.com'
    bookNames=htmlSoup.find_all('span', class_='bq')
    authors = htmlSoup.find_all('span', class_='zz')
    characterNums = htmlSoup.find_all('span', class_='zs')
    brief = htmlSoup.find_all('span', class_='jj')
    links = htmlSoup.find_all('a', class_="sea_xqa")
    totalNum = len(links)
    novels = []
    for i in range(totalNum):
        novel = {}
        novel['名字'] = bookNames[i].a.text.replace(' ', '').replace('\r\n','')
        novel['作者'] = authors[i].text[3:]
        novel['字数'] = characterNums[i].text[3:]
        novel['简介'] = brief[i].text
        novel['链接'] = baseUrl+links[i].get('href')
        novels.append(novel)
    return novels


def download_Novel(novel_URL):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36 Edg/93.0.961.47'}
    detailHtml = requests.get(novel_URL, headers)
    baseUrl = 'https://www.635book.com'
    if detailHtml.status_code == 200:
        detailHtmlSoup = BeautifulSoup(
            detailHtml.content.decode('GBK'), 'lxml')
        content = detailHtmlSoup.find_all('div', class_='mulu')[
            0].find_all('a')
        contentList = []
        if content:
            for chapter in content:
                chapterDict = {}
                chapterDict['标题'] = chapter.text
                if chapter.text == '':
                    continue
                my_Print('下载 '+chapter.text)
                chapterDict['链接'] = baseUrl+chapter.get('href')
                try:
                    chapterDict['正文'] = get_Novel_Text(chapterDict['链接'])
                except:
                     chapterDict['正文']='下载失败'
                     my_Print(chapter.text+'下载失败,60秒后重试')
                     time.sleep(60)
                contentList.append(chapterDict)
                time.sleep(3)
        return contentList
    else:
        print('Novel download failed')
        return []

def save_Novel(name,contentList):
    with open(name+'.txt','w',encoding='utf-8',errors='ignore') as f:
        for chapter in contentList:
            f.write(chapter['标题']+'\n'+chapter['链接']+chapter['正文'])   
def get_Novel_Text(chapter_URL):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36 Edg/93.0.961.47'}
    novel_URL = chapter_URL
    textHtml = requests.get(novel_URL, headers)
    textHtmlSoup = BeautifulSoup(
        textHtml.content.decode('gb18030',errors='ignore'), 'lxml')
    text = textHtmlSoup.find(
        'div', class_='read-content').text.replace('<br/>', '')
    return text

def output_Results(decodeResult):
    idx=0
    for i in decodeResult:
        print('------------------------------',idx,'------------------------------')
        for j in i.keys():print(j+':',i[j])
        print('序号：',idx)
        idx+=1
        print('------------------------------------------------------------')
def my_Print(msg):
    print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),'[*]:',msg)
if __name__ == '__main__':
    print('------------------------------------------------------------')
    my_Print('欢迎使用《夏季吧爬》小说下载软件')
    my_Print('使用教程：')
    my_Print('1.输入你要搜索的小说名字。')
    my_Print('2.对搜索结果进行检索并确定你要下载的小说的序号')
    my_Print('3.耐心等待下载完成')
    print('------------------------------------------------------------')
    targetName=''
    while targetName=='':
        targetName=input('输入你要搜索的小说名字并回车\n')
        if targetName=='':my_Print('错误，请不要直接回车')
    my_Print('全网搜索'+targetName+'中...')
    searchResult = get_Search_Result(targetName)
    my_Print('搜索完毕！共'+str(len(searchResult))+'个结果')
    my_Print('解码中....')
    decodeResult = decode_Search_Result(searchResult)
    novel_Num=len(decodeResult)
    my_Print('解码成功！输出如下：')
    output_Results(decodeResult)
    targetNum=''
    while targetNum=='':
        try:
            targetNum=int(input('输入你要下载的小说序号并回车(0-'+str(novel_Num-1)+'）\n'))
            if targetNum>=novel_Num:
                targetNum=''
                my_Print('输入超过最大范围！请重试')
        except: my_Print('错误，输入正确的数字')
    my_Print('正在下载 '+decodeResult[targetNum]['名字'])
    downloadResult=download_Novel(decodeResult[targetNum]['链接'])
    save_Novel(decodeResult[targetNum]['名字'],downloadResult)
    my_Print(decodeResult[targetNum]['名字']+' 下载完成!')
    my_Print('按任意键退出')
    input('')