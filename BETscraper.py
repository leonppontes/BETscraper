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
            if stat :
                homeShotsL1 = int(stat[0].text)
                awayShotsL1 = int(stat[1].text)
                homeShotsL2 = int(stat[2].text)
                awayShotsL2 = int(stat[3].text)
                homeShots = homeShotsL1 + homeShotsL2
                awayShots = awayShotsL1 + awayShotsL2
                minute = soupAux.find('div', {'class' : 'rectangle-label-component _ymtkw3'})
                if minute:
                    minStr = minute.text
                    minStr = minStr[:2]
                    if minStr[0].isdigit() and minStr[1].isdigit():
                        minNum = int(minStr)
                        if minNum < 45 :
                            if homeShots > 4 or awayShots > 4 :
                                print("APOSTAR NO JOGO \ntempo:", minNum,"\nChutes time da casa:", homeShots,"\nChutes time visitante", awayShots, "\nLink:", gameLink, "\n")
        aux = aux + 1
    driver.close()
    time.sleep(60)