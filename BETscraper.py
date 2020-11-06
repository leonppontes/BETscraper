from bs4 import BeautifulSoup 
from selenium import webdriver  
import time 

while True:

    url = "https://www.365scores.com/pt-br/football/live"
    driver = webdriver.Chrome('./chromedriver/chromedriver.exe') 
    driver.get(url) 
    time.sleep(5) 
    html = driver.page_source 
    soup = BeautifulSoup(html, "html.parser") 

    score = []
    link = []

    for aux1 in soup.find_all('div', {'class' : 'game-card-score'}):
        score.append(aux1)
    
    for aux2 in soup.find_all('a', class_="link game-card"):
        link.append(aux2['href'])

    aux = 0

    for url in link :
        gameLink = link[aux]
        scoreNumber = score[aux].text
        homeScore = int(scoreNumber[0])
        awayScore = int(scoreNumber[2]) 
        if homeScore == 0 and awayScore == 0 :
            driver.get('https://www.365scores.com{}/stats'.format(gameLink))
            time.sleep(5) 
            htmlAux = driver.page_source 
            soupAux = BeautifulSoup(htmlAux, "html.parser")
            stat = []
            for stats in soupAux.find_all('div', {'class' : '_l4qo4t text-component'}):
                stat.append(stats)
                homeShots = int(stat[0].text)
                awayShots = int(stat[1].text)
                minute = soupAux.find('div', {'class' : 'rectangle-label-component _ymtkw3'})
                minStr = minute.text
                minStr = minStr[:2]
                if minStr[0].isdigit() :
                    minNum = int(minStr)
                    if minNum < 45 :
                        if homeShots > 4 or awayShots > 4 :
                            print("APOSTAR NO JOGO \ntempo:", minNum,"\nChutes time da casa:", homeShots,"\nChutes time visitante", awayShots)
        aux = aux + 1
    driver.close()
    time.sleep(60)