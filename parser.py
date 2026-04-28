import csv
from helper_classes/sport.py import Sport

compatibility = {}
sports = {}
people = {}

IM_SPORTS = [
    "Badminton", "Basketball", "Billiards", "Broomball", "Climbing",
    "Dodgeball", "Flag Football", "Foosball", "Inner Tube Water Polo",
    "Pickleball", "Ping Pong", "River Run", "Soccer", "Softball",
    "Spikeball", "Squash", "Tennis", "Ultimate Frisbee", "Volleyball",
]

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
    """Read sports.csv and instantiate one Sport object per IM sport.

    Precondition: load_compatibility() must have already run.

    Chapter 1 — file I/O; Chapter 8 — class instantiation.
    """
    with open("data/sports.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["sport"]
            size = int(row["team_size"])

            # Defensive lookup — a sport might not appear in compatibility.csv
            # at all (a niche IM sport like Foosball or Billiards may have
            # no V/S pairs). Default to empty sets in that case.
            sport_compat = compatibility.get(name, {
                "very":     set(),
                "somewhat": set(),
            })

            sports[name] = Sport(
                name,
                size,
                sport_compat["very"],
                sport_compat["somewhat"],
            )



def load_people():
"""Read the survey CSV and instantiate one Person object per respondent.

For each row:
    - Section 1: build pre_college_experience from slots 1-3 plus the
                FSM-parsed free-text overflow field
    - Section 2: build im_experience from the 19 per-sport columns
                (skipping "Never played" entries — absence implies never)
    - Section 3: extract varsity status and sport name

Chapter 1 — file I/O; Chapter 5 — dict construction; Chapter 8 — Person
instantiation.
"""
with open(RESPONSES_CSV, encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:

        # ---- Section 1: pre-college sports (3 explicit slots) ----
        pre_college_experience = {}
        for slot in (1, 2, 3):
            sport = row[f"pre_college_sport_{slot}"]
            if sport == "":
                continue
            level = row[f"pre_college_sport_{slot}_level"]
            skill = row[f"pre_college_sport_{slot}_skill"]
            # guarding for emtpy skill strings
            rating = int(skill) if skill else None
            pre_college_experience[sport] = {
                "experience": level, 
                "rating": rating,
            }

        # ---- Section 2: IM experience (19 sports) ----
        im_experience = {}
        for sport in IM_SPORTS:
            col_key = sport.lower().replace(" ", "_")
            experience = row[f"im_{col_key}_experience"]
            if experience == "Never played":
                continue                       
            skill = row[f"im_{col_key}_skill"]
            rating = int(skill) if skill else None
            im_experience[sport] = {
                "experience": experience     
                "rating": rating
            }

        # ---- Section 3: varsity status ----
        is_varsity = row["is_varsity"] == "yes"
        # Person.is_banned compares varsity to a target via exact string
        # match — None for non-varsity respondents avoids accidental hits
        varsity_sport = row["varsity_sport"] if is_varsity else None

        # ---- Build the Person object ----
        name = row["respondent_id"]
        people[name] = Person(name, varsity_sport, pre_college_experience, im_experience)
        




