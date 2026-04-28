import csv
from helper_classes/sport.py import Sport

compatibility = {}
sports = {}
people = {}

# creating the compatibility dictionary
def load_compatibility():

    # Opening compatibility.csv
    with open("data/compatibility.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        # Looping through the rows of the csv file
        for row in reader:

            # Getting the first sport and initializing it in the dictionary if it is not already there
            sport_a = row["sport_a"]
            if sport_a not in compatibility:
                compatibility[sport_a] = {
                    "very": set()
                    "somewhat": set()
                }

            # Getting the second sport from the csv and initializing it in the dictionary if it not already there
            sport_b = row["sport_b"]
            if sport_b not in compatibility:
                compatibility[sport_b] = {
                    "very": set()
                    "somewhat": set()
                }

            # Adding the sports to each other's compatibility sets if they are compatible

            tier = row["tier"]
            if tier == "very":
                compatibility[sport_a]["very"].add(sport_b)
                compatibility[sport_b]["very"].add(sport_a)
            elif tier == "somewhat":
                compatibility[sport_a]["somewhat"].add(sport_b)
                compatibility[sport_b]["somewhat"].add(sport_a)

# Creates the sports dictionary from the sports.csv file and the compatibility dictionary
def load_sports():
    with open("data/sports.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        # Looping through the rows of the csv file
        for row in reader:
            name = row["sport"]
            size = row["team_size"]
            very_compatible = compatibility[name]['very']
            somewhat_compatible = compatibility[name]['somewhat']
            sports[name] = Sport(name, size, very_compatible, somewhat_compatible)


def load_people():

    # Opening the people.csv file
    with open("data/people.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        for row in reader:
            



