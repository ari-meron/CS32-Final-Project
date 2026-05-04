import math
from helper_classes.person import Person
from helper_classes.sport import Sport
from parser import load_all, compatibility, sports, people


# Direct IM history with the target sport: contribution = bucket × rating
IM_MULTIPLIERS = {
    "1 season":   1.1,
    "2+ seasons": 1.2,
}

# Transferable pre-college skill: applies when a person played a sport
# OTHER than the target, modulated by the compatibility tier between
# the source sport and the target. Contribution = tier × rating.
TIER_MULTIPLIERS = {
    "very":     0.75,
    "somewhat": 0.25,
    "not":      0.0,
}

# Gets person's score based on direct experience with target_sport
def get_direct_score(person, target_sport):

    # Returning 0 for banned athletes
    if person.is_banned(target_sport):
        return 0

    # Getting persons experience
    im = person.im_experience_with(target_sport)
    pre_college = person.pre_college_experience_with(target_sport)

    # Getting Direct Experience Score
    direct_score = 0

    if im != None:
        im_skill = im[1]
        im_experience  = im[0]

        direct_score += im_skill * IM_MULTIPLIERS[im_experience]

    if pre_college != None:
        direct_score += pre_college[1]

    return direct_score

# Gets score for non-direct experience with target_sport
def get_general_score(person, target_sport):

    if person.is_banned(target_sport):
        return 0

    # Getting persons experience
    im = person.im_experience
    pre_college = person.pre_college_experience

    # Getting general experience scores
    general_score = 0

    # Getting total IM experience scores
    for sport in im:

        if sport == target_sport:
            continue
        
        tier = sports[sport].get_tier(target_sport)

        if sport in im:
            im_skill = im[sport]['rating']
            im_experience  = im[sport]['experience']

            general_score += im_skill * IM_MULTIPLIERS[im_experience] * TIER_MULTIPLIERS[tier]

    # Getting total score for precollege
    for sport in pre_college:

        if sport == target_sport:
            continue

        tier = sports[target_sport].get_tier(sport)

        if sport in pre_college:

            pre_skill = pre_college[sport]['rating']

            general_score += pre_skill * TIER_MULTIPLIERS[tier]

    # Returning Addative Score
    return general_score


def build_team(target_sport):

    # Gets numbers we need
    target = sports[target_sport]
    n_starters = target.size
    n_subs = math.ceil(target.size / 2)

    # Initializes return lists
    starters = []
    subs = []

    # Initializes lists of all players depending on experience
    tier1 = []
    tier2 = []

    for name in people:
        person = people[name]
        direct_score = round(get_direct_score(person, target_sport), 2)
        general_score = round(get_general_score(person, target_sport), 2)

        # Sort into tier 1 if the person has direct experience, tier 2 otherwise
        if direct_score != 0:
            tier1.append((person.name, direct_score, general_score))
        else:
            tier2. append((person.name, direct_score, general_score))
        
    # Sorting Tier 1 and Tier 2 based on direct and general score respectively
    sorted_tier1 = sorted(tier1, key=lambda x: x[1], reverse = True)
    sorted_tier2 = sorted(tier1, key=lambda x: x[2], reverse = True)

    # Assign's people to team and subs in all different scenarios for number of people with direct experience
    if len(sorted_tier1) >= n_starters + n_subs:
        starters = sorted_tier1[:n_starters]
        subs = sorted_tier1[n_starters:n_starters + n_subs]

    elif len(sorted_tier1) > n_starters and len(sorted_tier1) < n_starters + n_subs:
        starters = sorted_tier1[:n_starters]
        subs = sorted_tier1
        n_subs_left = n_subs - len(subs)
        subs.append(sorted_tier2[:n_subs_left])
    
    elif len(sorted_tier1) == n_starters:
        starters = sorted_tier1
        subs = sorted_tier2[:n_subs]

    elif len(sorted_tier1) < n_starters:
        # Filling starters:
        starters = sorted_tier1
        n_starters_left = n_starters - len(starters)
        starters.append(sorted_tier2[:n_starters_left])

        # Filling Subs
        subs = sorted_tier2[n_starters_left:n_starters_left + n_subs]

    return starters, subs









    






    

    
