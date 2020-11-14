from flask import Flask, render_template, jsonify, request
import requests
from bs4 import BeautifulSoup
# from pymongo import MongoClient  # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)

app = Flask(__name__)

# client = MongoClient('mongodb://test:test@localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
# db = client.dbsparta  # 'dbsparta'라는 이름의 db를 만들거나 사용합니다.
# Goalkeeper
# Defender
# Midfielder
# Forward

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/search', methods=['GET'])
def search_players():
    print("[search_players] START")
    position_info = request.args.get('position')
    if position_info == "goalkeepers":
        position_html = "Goalkeeper"
    elif position_info == "defender":
        position_html = "Defender"
    elif position_info == "midfielder":
        position_html = "Midfielder"
    elif position_info == "forward":
        position_html = "Forward"
    else:
        print("position_info is not matched")

    result = []

    url = "https://en.psg.fr/teams/first-team/squad"
    response_data = requests.get(url)
    soup = BeautifulSoup(response_data.text, 'html.parser')

    # PARSER FOR ALL PLAYERS
    a_tags = soup.select("#toggleTab0-tab-target > div.container.player-list > section")

    for a_tag in a_tags:
        players = a_tag.select('a')
        for player in players:
            position = player.select_one(
                "div.player-card__main > div.player-card__body > div.player-card__details > p.player-card__position")
            img = player.select_one(
                "div.player-card__main > div.player-card__body > div.player-card__mobile-avatar.u-visible-mobile > figure > img")[
                "data-src"]
            if position.text == position_html:
                link = player['href']
                player_name = link.split('/')[-1]
                # print(position.text, player_name, img)
                result.append([position.text, player_name, img])

    print("[search_players] END")
    return jsonify({'result': 'success', 'goalkeepers': result})

@app.route('/goalkeepers')
def show_goalkeepers():
    return render_template('player_goalkeepers.html')

@app.route('/defender')
def show_defender():
    return render_template('player_defender.html')

@app.route('/midfielder')
def show_midfielder():
    return render_template('player_midfielder.html')

@app.route('/forward')
def show_forward():
    return render_template('player_forward.html')

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
