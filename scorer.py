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

def direct_score(person, target_sport):

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

def general_score(person, target_sport):

    if person.is_banned:
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
        
        tier = sports[target_sport].get_tier(sport)

        im_skill = im[target_sport]['rating']
        im_experience  = im[target_sport]['experience']

        general_score += im_skill * IM_MULTIPLIERS[im_experience] * TIER_MULTIPLIERS[tier]

    # Getting total score for precollege
    for sport in pre_college:

        if sport == target_sport:
            continue

        tier = sports[target_sport].get_tier(sport)

        pre_skill = pre_college[target_sport]['rating']

        general_score += pre_skill * TIER_MULTIPLIERS[tier]

    return general_score


def build_team(target_sport):

    target = sports[target_sport]
    n_starters = target.size
    n_subs = target.ceil(target.size / 2)

    starters = []
    subs = []

    tier1 = []
    tier2 = []

    for person in people:
        direct_score = direct_score(person, target_sport)
        general_score = general_score(person, target_sport)

        if direct_score != 0:
            tier1.append((person.name, direct_score, general_score))
        else:
            tier2. append((person.name, direct_score, general_score))
        
    
    sorted_tier1 = sorted(tier1, key=lambda x: x[1])
    sorted_tier2 = sorted(tier1, key=lambda x: x[2])

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









    






    

    
