#coding=utf-8
import urllib.request as req
from bs4 import BeautifulSoup
import re



# 解析历史数据信息
def parseHistoryData(playid):
    url = 'http://fenxi.zgzcw.com/' + playid + '/bfyc'
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


    # print(host,visit,host_logo,visit_logo)

def getHtml(url):
    page = req.urlopen(url)
    html = page.read()
    return html

html = getHtml("http://cp.zgzcw.com/lottery/jchtplayvsForJsp.action?lotteryId=47")

soup = BeautifulSoup(html,'lxml')

tables = soup.find_all('table')

# 解析比赛两支队基本信息
for table in tables:
    for tr in table.findAll('tr',class_='beginBet')[::2]:
        playid = tr['playid']
        for td in tr.findAll('td',class_='wh-1'):
            code = td.a.text
        for td in tr.findAll('td',class_='wh-2'):
            title = td['title']
        for td in tr.findAll('td',class_='wh-3'):
            for sp in td.findAll('span'):
                print(sp['title'])
                print(sp.text)
        for td in tr.findAll('td',class_='wh-4 t-r'):
            a = td.a.text
        for td in tr.findAll('td',class_='wh-6 t-l'):
            b = td.a.text
        print(code,title,a,b,playid)
        print('********************************************************************************************')
        parseHistoryData(playid)
