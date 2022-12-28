import re
import requests
from bs4 import BeautifulSoup

import jieba
from collections import Counter

url = "https://news.cnstock.com/news,bwkx-202212-4995035.htm"
Prob = 0.5

def countchn(string):
    '''
    计算中文数字和中文出现频率
    '''
    pattern = re.compile(u'[\u1100-\uFFFDh]+?')
    result = pattern.findall(string)
    chnnum = len(result)
    possible = chnnum/len(str(string))
    return (chnnum, possible)

def statchn(string):
    cut_words = ""
    string = string.strip('\n')
    string = re.sub("[A-Za-z0-9\：\·\—\，\。\“ \”]", "", string)
    seg_list = jieba.cut(string, cut_all=False)
    cut_words += (" ".join(seg_list))
    all_words = cut_words.split()
    c = Counter()
    for x in all_words:
        if len(x) > 1 and x != '\r\n':
            c[x] += 1

    return sorted(c.items(), key=lambda x: x[1], reverse=True)


resp = requests.get(url)
resp.encoding = BeautifulSoup(resp.content, "lxml").original_encoding 
bs = BeautifulSoup(resp.text, "lxml")

span_list = bs.find_all('span')
part = bs.find_all('p')
article = ''
date = ''
for span in span_list:
    if 'class' in span.attrs and span['class'] == ['timer']:
        date = span.text
        break

for paragraph in part:
    chnstatus = countchn(str(paragraph))
    possible = chnstatus[1]
    if possible > Prob:
       article += str(paragraph)

while article.find('<') != -1 and article.find('>') != -1:
      string = article[article.find('<'):article.find('>')+1]
      article = article.replace(string,'')
while article.find('\u3000') != -1:
      article = article.replace('\u3000','')

article = ' '.join(re.split(' +|\n+', article)).strip() 

print("[INFO] 感兴趣文本： \n {}\n".format(article))
print("[INFO] 文本词频统计：\n{}".format(statchn(article)))
