#coding=utf-8
import urllib.request as req
from bs4 import BeautifulSoup
import re
import threading
from pymongo import MongoClient

client = MongoClient('127.0.0.1', 27017)


def saveData():
    db_name = 'lottery'
    db = client[db_name]
    collection_lottery = db['lottery']

    collection_lottery.save({
        'name':'zhuzhu'
    })

# 解析历史数据信息
def parseHistoryData(baseinfo):
    url = 'http://fenxi.zgzcw.com/' + baseinfo[4] + '/bfyc'
    html = getHtml(url)
    soup = BeautifulSoup(html, 'lxml')
    host = soup.find('div',class_='host-name').a.text
    visit = soup.find('div',class_='visit-name').a.text
    host_logo = soup.find('div',class_='host-logo').img['src']
    visit_logo = soup.find('div',class_='visit-logo').img['src']

    # 上赛季信息以及排名
    print(baseinfo)

    team_add_info = soup.find('div',class_='team-add-info')
    print(team_add_info.find('div',class_='team-add-info-zd').text)
    print(team_add_info.find('div',class_='team-add-info-kd').text)

    team_info = soup.find('div', class_='team-info')
    print(team_info.find('div', class_='team-info-h').text)
    print(team_info.find('div', class_='team-info-v').text)
    print('********************************************************************************************')



def getHtml(url):
    # 伪装浏览器头
    headers = {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
    q = req.Request(url, headers=headers)
    page = req.urlopen(q).read()
    page = page.decode('utf-8')
    return page


def begin(url):
    soup = BeautifulSoup(getHtml(url), 'lxml')
    tables = soup.find_all('table')

    threads = []

    # 解析比赛两支队基本信息
    for table in tables:
        for tr in table.findAll('tr', class_='beginBet')[::2]:
            playid = tr['playid']
            for td in tr.findAll('td', class_='wh-1'):
                code = td.a.text
            for td in tr.findAll('td', class_='wh-2'):
                title = td['title']
            # for td in tr.findAll('td', class_='wh-3'):
            #     for sp in td.findAll('span'):
            #         print(sp['title'])
            #         print(sp.text)
            for td in tr.findAll('td', class_='wh-4 t-r'):
                a = td.a.text
            for td in tr.findAll('td', class_='wh-6 t-l'):
                b = td.a.text
            baseinfo = (code, title, a, b, playid)
            t = threading.Thread(target=parseHistoryData, args=(baseinfo,))
            threads.append(t)
    files = range(len(threads))
    for i in files:
        threads[i].start()
    for i in files:
        threads[i].join()

url  =  "http://cp.zgzcw.com/lottery/jchtplayvsForJsp.action?lotteryId=47"
begin(url)
