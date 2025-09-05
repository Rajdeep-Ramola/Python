from bs4 import BeautifulSoup
import requests

response=requests.get("https://news.ycombinator.com/news")
webpage=response.text
soup=BeautifulSoup(webpage,"html.parser") #to parse the html of website

articles=soup.find_all(name="span",class_="titleline") #to find all anchor tags with class storylink
article_text=[]
article_link=[]
article_upvotes=[]
for article_tags in articles:
    text=article_tags.getText() #to get the text of article in a sequence
    article_text.append(text)
    link=article_tags.get("href") #to get links of articles
    article_link.append(link)

#Now to find upvotes of different articles
scores=soup.find_all(name="span",class_="score")#to find all the upvotes
for score in scores:
    upvote=int(score.getText().split()[0])
    article_upvotes.append(upvote)

print(article_text)
print(article_link)
print(article_upvotes)

