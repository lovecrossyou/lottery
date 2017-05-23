import urllib.request
from bs4 import BeautifulSoup
import os,sys

# 读取文件
def readFile(file):
    f = open(file,'r')
    all_lines = f.read()
    return all_lines

file_name = 'demo_1.html'

def parseInfo():
    html = readFile(file_name)
    soup = BeautifulSoup(html, 'lxml')
    tables = soup.findAll('table',class_='tab-add2')

    tabledatas = []

    for table in tables:
        titles = []
        thead = table.thead
        tbody = table.tbody
        # 获取标题
        if(thead!=None):
            tds = thead.findAll('td')
            for td in tds:
                titles.append(td.text)
        # 获取数据
        if(tbody !=None):
            trs = tbody.findAll('tr')
            datas = []
            for tr in trs:
                tds = tr.findAll('td')
                line_data = []
                for td in tds:
                    script = td.script
                    if(script!=None):
                        script.clear()
                    line_data.append(td.text)
                datas.append(line_data)
            tabledatas.append((titles, datas), )
    print(tabledatas)

parseInfo()