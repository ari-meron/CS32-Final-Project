from parser import load_all, compatibility, sports, people
from helper_classes.sport import Sport
from helper_classes.person import Person
from scorer import get_direct_score, get_general_score, build_team

def main():
    load_all()
    
    target_sport = input("What sport do you need a team for?: ")
    starters, subs = build_team(target_sport)

    print("STARTERS:")
    print(f"{'Name':<6} {'Direct Score':<15} {'General Score'}")
    for starter in starters:
        print(f"{starter[0]:<6} {starter[1]:<15} {starter[2]}")

    
    print("\nSUBS:")
    print(f"{'Name':<6} {'Direct Score':<15} {'General Score'}")
    for sub in subs:
        print(f"{sub[0]:<6} {sub[1]:<15} {sub[2]}")



if __name__ == '__main__':
    main()
