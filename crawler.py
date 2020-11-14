from bs4 import BeautifulSoup
import requests

url = "https://en.psg.fr/teams/first-team/squad"

response_data = requests.get(url)
soup = BeautifulSoup(response_data.text, 'html.parser')

# PARSER FOR ALL PLAYERS
a_tags = soup.select("#toggleTab0-tab-target > div.container.player-list > section")

for a_tag in a_tags:
    players = a_tag.select('a')
    for player in players:
        position = player.select_one("div.player-card__main > div.player-card__body > div.player-card__details > p.player-card__position")
        img = player.select_one("div.player-card__main > div.player-card__body > div.player-card__mobile-avatar.u-visible-mobile > figure > img")["data-src"]
        if position.text == "Forward":
            link = player['href']
            player_name = link.split('/')[-1]
            print(position.text, player_name, img)

# Goalkeeper
# Defender
# Midfielder
# Forward