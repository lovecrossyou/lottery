#coding=utf-8
import urllib.request as req
from bs4 import BeautifulSoup


def getHtml(url):
    page = req.urlopen(url)
    html = page.read()
    return html

html = getHtml("http://cp.zgzcw.com/lottery/jchtplayvsForJsp.action?lotteryId=47")

soup = BeautifulSoup(html,'lxml')
table = soup.find_all(id='hide_box_1')[0]
lists = table.find(class_='beginBet')

for list in lists:
    print(list)
    print('******************************************')
print(len(lists))