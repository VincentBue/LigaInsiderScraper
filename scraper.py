from bs4 import BeautifulSoup
import requests
from datetime import date
import pickle
import os

BASE_PATH = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_PATH, "Database")
BACKUP_PATH = os.path.join(BASE_PATH, "Backup")
DATABASE_PATH = os.path.join(DATA_PATH, "data.pickle")

POSITIONS = [
    "Torhüter",
    "Abwehrspieler",
    "Mittelfeldspieler",
    "Stürmer"
]

TEAMS = [
    "1. FC Köln",
    "1. FC Union Berlin",
    "1. FSV Mainz 05",
    "Arminia Bielefeld",
    "Bayer 04 Leverkusen",
    "Borussia Dortmund",
    "Borussia Mönchengladbach",
    "Eintracht Frankfurt",
    "FC Augsburg",
    "FC Bayern München",
    "Hertha BSC",
    "RB Leipzig",
    "SC Freiburg",
    "SpVgg Greuther Fürth",
    "TSG 1899 Hoffenheim",
    "VfB Stuttgart",
    "VfL Wolfsburg",
    "VfL Bochum"
]

class Player:
    def __init__(
        self,
        name,
        club,
        position,
        current_points,
        points_history,
        current_market_value,
        market_value_history,
    ):
        self.name = name
        self.club = club
        self.position = position
        self.current_points = current_points
        self.points_history = points_history
        self.current_market_value = current_market_value
        self.market_value_history = market_value_history
        self.last_modified = get_date_string()

    def __eq__(self,
                new):
        return self.name == new.name

    def __repr__(self):
        return ("Player: %s\nTeam: %s\nPosition: %s\nTotal Points: %s\nMarket Value: %s" 
                % (self.name,self.club,self.position,self.current_points,self.current_market_value))

def get_date_string():
    d = date.today()
    date_string = str(d.day)+"/"+str(d.month)+"/"+str(d.year)
    return date_string

def retrieve_players():
    """
    Function that scrapes Tages- gewinner and verlierer.
    Returns: List of player instances.
    """
    date_string = get_date_string()
    links = ['https://www.ligainsider.de/stats/kickbase/marktwerte/tag/gewinner/',
                'https://www.ligainsider.de/stats/kickbase/marktwerte/tag/verlierer/']
    players = []
    for link in links:
        html_text = requests.get(link).text
        soup = BeautifulSoup(html_text, 'lxml')
        table = soup.find('tbody')
        rows = table.find_all('tr')

        # Loop through rows in table on link
        for row in rows:
            cols =  row.find_all('td')
            cols = [x.text.strip() for x in cols][2:-2]
            name = cols[0]
            club = cols[1]
            position = cols[2]
            points = int("".join(cols[3].split(".")))
            current_market_value = int("".join(cols[4][:-1].split(".")))
            assert club in TEAMS, ("Club " + club + " is not in registered teams")
            assert position in POSITIONS, ("Position " + position + " is not in registered positions")
            current_player = Player(
                name=name,
                club=club,
                position=position,
                current_points=points,
                points_history=[(date_string,points)],
                current_market_value=current_market_value,
                market_value_history=[(date_string,current_market_value)]
            )
            players.append(current_player)
    return players

def update_player(p_to_be_updated, p_new):
    if not p_to_be_updated.last_modified == p_new.last_modified:
        p_to_be_updated.club = p_new.club
        p_to_be_updated.position = p_new.position
        p_to_be_updated.current_points = p_new.current_points
        p_to_be_updated.points_history.extend(p_new.points_history)
        p_to_be_updated.current_market_value = p_new.current_market_value
        p_to_be_updated.market_value_history.extend(p_new.market_value_history)
        p_to_be_updated.last_modified = p_new.last_modified
    else:
        print("Warning: It seems you executed two times today. Not updating.")

def merge(players_stored, players_retrieved):
    """
    Merge stored players with players retrieved from retrieve function.
    """
    print("New")
    for p_new in players_retrieved:
        if p_new in players_stored:
            # Update the player
            idx = players_stored.index(p_new)
            # Update player at idx using values of p_new
            update_player(p_to_be_updated=players_stored[idx], p_new=p_new)
        else:
            players_stored.append(p_new)
    return players_stored

def update_data():
    """
    1. Fetch new data by calling retrieve_players.
    2. Open pickle file and get list. Use empty list of pickle file not available.
    3. Call merge.
    4. Write to pickle file using DATABASE_PATH.
    """
    if not os.path.exists(DATA_PATH):
        print("Could not find database folder at", DATA_PATH, "\nCreating...")
        os.mkdir(DATA_PATH)
    if not os.path.exists(BACKUP_PATH):
        print("Could not find backup folder at", BACKUP_PATH, "\nCreating...")
        os.mkdir(BACKUP_PATH)

    print("Retrieving players...")
    players_retrieved = retrieve_players()
    players_stored = []
    if os.path.exists(DATABASE_PATH):
        print("Loading database...")
        with open(DATABASE_PATH, "rb") as f:
            players_stored = pickle.load(f)
        # - Backup
        BACKUP_FILE_PATH = os.path.join(BACKUP_PATH, "-".join(get_date_string().split('/'))+'-data.pickle')
        print("Writing backup...")
        with open(BACKUP_FILE_PATH, "wb") as f:
            pickle.dump(players_stored, f, protocol=pickle.HIGHEST_PROTOCOL)

    print("Merge database...")
    players_stored = merge(players_stored, players_retrieved)
    print("Write to database...")
    with open(DATABASE_PATH, "wb") as f:
        pickle.dump(players_stored, f, protocol=pickle.HIGHEST_PROTOCOL)
    print("Update finished.")

if __name__ == "__main__":
    update_data()
