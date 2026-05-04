from parser import load_all, compatibility, sports, people
from helper_classes.sport import Sport
from helper_classes.person import Person
from scorer import get_direct_score, get_general_score, build_team

def main():
    load_all()
    
    target_sport = input("What sport do you need a team for?: ")
    starters, subs = build_team(target_sport)

    print('Starters:')
    for starter in starters:
        print(f'Name: {starter[0]}, Direct Score: {starter[1]}, General Score: {starter[2]}')
    print('Subs:')
    for sub in subs:
        print(f'Name: {sub[0]}, Direct Score: {sub[1]}, General Score: {sub[2]}')


if __name__ == '__main__':
    main()
