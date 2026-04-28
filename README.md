# CS32-Final-Project
Ari and Cotton's CS32 FP

Our vision is to revolutionize the system used to direct Currier's IM sports teams. We aim to build an algorithm to help put together team lineups for Currier IM sports. Currier has great engagement in IM sports, which is great, but comes at the cost of having to make decisions on lineups. We want to build a system that will take data on each person's sports experience and skills, and then build an algorithm that will take that input and spit out a team. 

We are currently working on collecting data (see the google forms link to take a look at what our collection form looks like: https://docs.google.com/forms/d/e/1FAIpQLSe9Z3H5nqNsGBGjexu6MpprxUBiiFXFQrOFewkHqCBtRtTfFA/viewform?usp=publish-editor)

# Project Structure

Our repo contains the following folders and files:

## data

We have a data folder that includes the files:

- sports.csv
- people.csv
- compatibility.csv
- generate_dummy_data.py

### sports.csv

The sports.csv file is a csv file that contains a list of IM sports and the number of spots/players required to build a team

### people.csv

This file is a csv file that contains a list of people in Currier (or dummy observations to bolster the data). The people are the observations (rows in the csv), with columns variables being the sports those observations play, and their relative experience and skill level.

### compatibility.csv

A csv file that contains information on how compatible the skills from different sports are with each other. A sport can be either very, somewhat, or not compatible with another

### generate_dummy_data.py

A function that generates realistic dummy data points to increase the size of our data file for testing.


## helper_classes

The helper_classes folder contains two files:

- person.py
- sport.py

### person.py

A python file that defines the Person class. The Person class will have the attributes: varsity, outside_experience

### sport.py

A python file that defines the Sport class. The Sport class will have the attributes: name, size, very_compatible, somewhat_compatible

- name: (str) name of the sport
- size: (int) team size for the sport
- very_compatible: (set) set of sports that sport is very compatible with
- somewhat_compatible: (set) set of sports that sport is somewhat compatible with

The Sport class will also have the function compatibility_tier(other_sport) which will find how compatible other_sport is with the sport the Sport class object has.

## Other Files

Outside of these two folder there are 3 python files in our repository:

- scorer.py
- parser.py
- main.py

### parser.py

A python file that contains the methods load_sports() and load_people(). The functions take data from the sports.csv, compatibility.csv, and people.csv files, to build the sports and people dictionaries.

The sports dictionary is a dictionary that contains entries for sports and corresponding Sport objects

The people dictionary is a dictionary that contains entries for people and corresponding Person objects

### scorer.py

A python file that contains the following functions:

- score()
- build_team()

The score function takes parameters person and target_sport and then outputs a numerical score for that person (higher score means that the person should be included in the team, lower score means they shouldn't) based on the compatibility of the person's sports experience with that sport

The build_team() function takes the target_sport parameter, and then outputs a set of people who should make up the team for that sport

### main.py

The main.py file contains a main function that takes user input as to what sport they want to build a team for, then it outputs a team for that sport.


