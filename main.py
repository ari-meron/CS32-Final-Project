from parser import load_all, compatibility, sports, people
from helper_classes.sport import Sport
from helper_classes.person import Person
from scorer import get_direct_score, get_general_score, build_team

def main():
    load_all()
    
    target_sport = input("What sport do you need a team for?: ")
    starters, subs = build_team(target_sport)

    print(starters)
    print(subs)


if __name__ == '__main__':
    main()
