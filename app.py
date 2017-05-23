#coding=utf-8
import threading
import urllib.request

from bs4 import BeautifulSoup
from pymongo import MongoClient

conn = MongoClient('127.0.0.1', 27017)
db_name = 'lottery'
db = conn.lottery
collection_game = db['game']
collection_team = db['team']


def saveTeamInfo(teamInfo):
    # team信息
    collection_team.insert({
        'name': teamInfo[0],
        'info': teamInfo[1]
    })
    print(teamInfo)


def saveGameInfo(gameInfo):
    # 保存比赛信息
    collection_game.insert({
        'host':gameInfo[2],
        'visit':gameInfo[3],
        'title':gameInfo[1],
        'playid':gameInfo[4],
        'time':gameInfo[0],
        'result':''
    })
    # print(gameInfo)


# 解析历史数据信息
def parseHistoryData(gameInfo):
    url = 'http://fenxi.zgzcw.com/' + gameInfo[4] + '/bfyc'
    html = getHtml(url)
    soup = BeautifulSoup(html, 'lxml')
    host = soup.find('div',class_='host-name').a.text
    visit = soup.find('div',class_='visit-name').a.text
    host_logo = soup.find('div',class_='host-logo').img['src']
    visit_logo = soup.find('div',class_='visit-logo').img['src']

    # 上赛季信息以及排名

    team_add_info = soup.find('div',class_='team-add-info')
    print(team_add_info.find('div',class_='team-add-info-zd').text)
    print(team_add_info.find('div',class_='team-add-info-kd').text)

    team_info = soup.find('div', class_='team-info')
    print(team_info.find('div', class_='team-info-h').text)
    print(team_info.find('div', class_='team-info-v').text)

    f = open("demo_1.html", 'wb')
    f.write(html)
    f.close()
    print('done....')
    # teamHostInfo = (host,)
    # teamVisitInfo = ()
    # saveGameInfo(gameInfo)


def getHtml(url):
    proxy_ip = {'http': '171.10.31.41:8080'}  # 想验证的代理IP
    proxy_support = urllib.request.ProxyHandler(proxy_ip)
    opener = urllib.request.build_opener(proxy_support)
    opener.addheaders = [("User-Agent", "Mozilla/5.0 (Windows NT 10.0; WOW64)")]
    urllib.request.install_opener(opener)
    return urllib.request.urlopen(url).read()




def begin(url):
    soup = BeautifulSoup(getHtml(url), 'lxml')
    tables = soup.find_all('table')

    threads = []

    # 解析比赛两支队基本信息
    for table in tables:
        for tr in table.findAll('tr', class_='beginBet')[::2]:
            playid = tr.find('td',class_='wh-10 b-l')['newplayid']
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

url  =  "http://cp.zgzcw.com/lottery/jchtplayvsForJsp.action?lotteryId=47&type=jcmini"
begin(url)
