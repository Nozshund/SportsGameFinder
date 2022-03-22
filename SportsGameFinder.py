import requests
import json
from datetime import datetime
#ISO format
mlb_date_format = "%Y-%m-%d"
mlb_api_base_url = "http://statsapi.mlb.com"
mlb_today_schedule_url = "http://statsapi.mlb.com/api/v1/schedule/games/?sportId=1"
mlb_teams_url = "http://statsapi.mlb.com/api/v1/teams"
mlb_test_url = "http://statsapi.mlb.com/api/v1/sports/"
mlb_venue_url = "http://statsapi.mlb.com/api/v1/venues"



#rough sketch of logic
#3 variables
#City where games are played
#Teams playing in that city
#time span for days (1 = same day)
#time frame (no option, whole season)

#get the city, teams, optional time span for dates, optional time frame
#find time spans where all teams play a game in the city

#get all days with games in given time frame (default whole season)
#get all games in which one of the given teams is playing and game is held in given city
#see what date(s) within the time span have games

#TODO THOUGHT:  Create separate classes for all sports to pull/get data, all output common object that is then processed the same way
#allows us to use the below code, just need to create our own objects to look through


def __main__():        
    url = create_mlb_schedule_date_url_full_year() 
    full_schedule_data = get_json(url)        
    #write_json_file(full_schedule_data,"mlb_data.json")
    
        
    city = 'New York City'
    teams = ['Yankees','Mets']
    
    team_json = get_mlb_teams_data(teams)
    write_json_file(team_json,"team.json")
    
        
    venue_ids = get_venue_ids(team_json)
    
    team_ids = get_ids(team_json)
    #print(team_ids)
    
    game_data = []
    for date in full_schedule_data["dates"]:
        team_games = {}
        for team in team_ids:
            team_games[team] = []
            
        for game in date["games"]:
        
            if game["venue"]["id"] in venue_ids:
            
                if game["teams"]["away"]["team"]["id"] in team_ids:
                    team_games[game["teams"]["away"]["team"]["id"]].append(game)
                    
                if game["teams"]["home"]["team"]["id"] in team_ids:
                    team_games[game["teams"]["home"]["team"]["id"]].append(game)        
                        
        found_game = 0
        for k,v in team_games.items():
            if len(v) > 0:
                found_game += 1
        
        if found_game == len(team_ids):
            for k,v in team_games.items():
                game_data += v
        
            
    
    #print(game_data)
    write_json_file(game_data,"game_data.json")
    
    
    #game_day = json["dates"]    
    #game_day_date = game_day[0]    
    #test2 = game_day_date["date"]
    #test = datetime.strptime(test2,mlb_date_format)
    #print(test)
    
def get_json(url):
    try:
        response = requests.get(url)
        #TODO Test this error handling
        if response.status_code != 200:
            print(f'Error getting json from URL {url}\n Response code = {response.status_code}')
        return response.json()
    except Exception as err:
        print(f"Exception: {err}")
        
def create_mlb_schedule_date_url(startDate, endDate):    
    return mlb_api_base_url + f'/api/v1/schedule/games/?sportId=1&startDate={startDate.date().isoformat()}&endDate={endDate.date().isoformat()}'
    
def create_mlb_schedule_date_url_full_year():
    return create_mlb_schedule_date_url(datetime(year = 2022, month = 1, day = 1),datetime(year = 2022, month = 12, day = 31))
    
def get_mlb_teams_data(teams):
    json = get_json(mlb_teams_url)
    teams_json = []
    
    for team in json["teams"]:
        if team["teamName"] in teams and team["sport"]["id"] == 1:
            teams_json.append(team)     
    #print(teams_json)
    return teams_json

def get_ids(json_data):
    id_list = []
    for data in json_data:
        id_list.append(data["id"])
    return id_list
    
def get_venue_ids(json_data):
    id_list = []
    for data in json_data:
        id_list.append(data["venue"]["id"])
    return id_list
    
def write_json_file(data_to_write,file_name):
    file = open(file_name, "w")
    file.write(json.dumps(data_to_write, indent = 4))
    file.close()           
    
__main__()