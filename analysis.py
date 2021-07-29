#from scraper import *
import pickle
import matplotlib.pyplot as plt
import numpy as np
from scraper import Player
import os


BASE_PATH = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_PATH, "Database")
BACKUP_PATH = os.path.join(BASE_PATH, "Backup")
DATABASE_PATH = os.path.join(DATA_PATH, "data.pickle")


data = {}
if os.path.exists(DATABASE_PATH):
    print("Loading database...")
    with open(DATABASE_PATH, "rb") as f:
        data = pickle.load(f)
        print("Data loaded")
else:
    print("Database not found")

print(data['Ridle Baku'].current_market_value)


def basic_graph(player):
    """
    Plots basic graph of given player
    x-Axes = Date
    y-Axes = Market value
    """
    unzipped = zip(*player.market_value_history)
    dates = unzipped[0]
    market_values = unzipped[1]
    x = np.arange(len(dates))

    plt.xticks(x, dates)
    plt.plot(x,market_values)
    plt.show()

    




basic_graph(data['Ridle Baku'])


"""
fig, ax = plt.subplots()
ax.plot([1,2,3,4] , [data['Ridle Baku'].current_market_value,
         data['Ridle Baku'].current_market_value + 100000,
         data['Ridle Baku'].current_market_value + 800000,
         data['Ridle Baku'].current_market_value + 800000])

fig, ay = plt.subplots()
ay.plot([1,2,3,4],[1,4,2,3])
"""


