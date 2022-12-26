import requests # request img from web
import shutil # save img locally
import json
import base64

class Poster:
    def __init__(self):
        pass

    def search_game(self, name):
        url = "https://game-service-ixdm6djuha-uc.a.run.app/game/?name={}".format(name)
        response = requests.get(url=url)
        games = []
        for object in json.loads(response.text):
            game = {}
            game["id"] = object["id"]
            game["name"] = object["name"]
            games.append(game)

        return games
        print(json.loads(response.text)[0]["name"])
        print(json.loads(response.text)[1]["name"])


    def search_user(self, name):
        url = "https://user-service-ixdm6djuha-uc.a.run.app/user/?username={}".format(name)
        response = requests.get(url=url)
        users = []
        for object in json.loads(response.text):
            user = {}
            user["id"] = object["id"]
            user["username"] = object["username"]
            users.append(user)

        return users
        print(json.loads(response.text)[0]["name"])
        print(json.loads(response.text)[1]["name"])


    def add_game(self, game_json):
        print("HERE")
        print(game_json)
        response = requests.post(url="https://game-service-ixdm6djuha-uc.a.run.app/game/", json=game_json)
        #print(response.json)
        #print(response.text)
        return


    def delete_game(self, game_id):
        url="https://game-service-ixdm6djuha-uc.a.run.app/game/{}".format(game_id)
        response = requests.delete(url)
        return
        
    def delete_user(self, game_id):
        #url="https://game-service-ixdm6djuha-uc.a.run.app/game/{}".format(game_id)
        #response = requests.delete(url)
        return

    
        
        

       


    
            



