import urllib.parse as turnUrlCode

import requests
from bs4 import BeautifulSoup


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
    authors = htmlSoup.find_all('span', class_='zz')
    characterNums = htmlSoup.find_all('span', class_='zs')
    brief = htmlSoup.find_all('span', class_='jj')
    links = htmlSoup.find_all('a', class_="sea_xqa")
    totalNum = len(links)
    novels = []
    for i in range(totalNum):
        novel = {}
        novel['名字'] = ''
        novel['作者'] = authors[i].text[3:]
        novel['字数'] = characterNums[i].text[3:]
        novel['简介'] = brief[i].text
        novel['链接'] = baseUrl+links[i].get('href')
        novels.append(novel)
    return novels


def download_Novel(novel_URL):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36 Edg/93.0.961.47'}
    novel_URL = 'https://www.635book.com/1/1251.html'
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
                chapterDict['链接'] = baseUrl+chapter.get('href')
                chapterDict['正文'] = get_Novel_Text(chapterDict['链接'])
                contentList.append(chapterDict)
        return contentList
    else:
        print('Novel download failed')
        return []


def get_Novel_Text(chapter_URL):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36 Edg/93.0.961.47'}
    novel_URL = chapter_URL
    textHtml = requests.get(novel_URL, headers)
    textHtmlSoup = BeautifulSoup(
        textHtml.content.decode('GBK'), 'lxml')
    text = textHtmlSoup.find(
        'div', class_='read-content').text.replace('<br/>', '')
    return text


searchResult = get_Search_Result('凡人修仙传')
decodeResult = decode_Search_Result(searchResult)
