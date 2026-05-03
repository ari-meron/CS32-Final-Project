"""
generate_dummy_data.py — Probabilistic IM Survey Response Generator
====================================================================

Generates 400 synthetic Google-Forms-style survey responses for the IM
Roster Optimizer project. Each respondent is built by drawing from the
locked probability distributions documented in our planning sessions.

Course technique references (CS32):
  - Chapter 1: file I/O via the csv module; standard control flow
  - Chapter 3: functions, the random module (random.random for Bernoulli
               draws, random.choices for weighted categorical draws,
               random.gauss for normal-distribution skill ratings)
  - Chapter 5: dictionaries used for distribution lookups and per-sport
               name mappings (varsity sport → Section 1 dropdown name)

Output: data/responses.csv (creates the directory if missing)
"""

import csv          # Chapter 1 — CSV reading/writing for tabular file I/O
import math         # Chapter 1 — math.ceil() for asymmetric upward rounding
import os           # Chapter 1 — os.makedirs() to create output directory
import random       # Chapter 3 — randomness primitives (gauss/choices)


# ============================================================================
# REPRODUCIBILITY (Chapter 3 — controlling randomness for deterministic output)
# ============================================================================
# Set a fixed seed so every run of this script produces an identical CSV.
# This is critical for downstream debugging — the parser/scorer can be
# tested against a stable reference dataset.
RANDOM_SEED = 42
random.seed(RANDOM_SEED)


# ============================================================================
# POPULATION-LEVEL CONSTANTS (locked design parameters)
# ============================================================================
N_RESPONDENTS = 400      # Total survey responses to generate
P_VARSITY = 0.20         # P(respondent is a current Harvard varsity athlete);
                         # matches Harvard's stated ~20% varsity rate

OUTPUT_PATH = "data/responses.csv"   # Output relative to working directory


# ============================================================================
# SECTION 2 — IM SPORTS (the 19 House intramural sports)
# ============================================================================
# These names must match sports.csv exactly so downstream joins work.
IM_SPORTS = [
    "Badminton", "Basketball", "Billiards", "Broomball", "Climbing",
    "Dodgeball", "Flag Football", "Foosball", "Inner Tube Water Polo",
    "Pickleball", "Ping Pong", "River Run", "Soccer", "Softball",
    "Spikeball", "Squash", "Tennis", "Ultimate Frisbee", "Volleyball",
]


# ============================================================================
# SECTION 1 — PRE-COLLEGE SPORT DROPDOWN, ORGANIZED INTO 4 POPULARITY TIERS
# ============================================================================
# Tier weights reflect realistic high-school participation among the kind of
# students who attend Harvard (a mix of mass-participation HS sports and
# prep-school favorites). Each individual sport's draw weight equals its
# tier's per-sport weight; tier totals are commented inline.

TIER_1_SPORTS = [   # Mass participation — 12% each (T1 total = 60%)
    "Soccer", "Basketball", "Track & Field", "Tennis", "Swimming",
]
TIER_2_SPORTS = [   # Common HS sports — 5% each (T2 total = 25%)
    "Cross Country", "Baseball", "Lacrosse", "Football (American)", "Crew",
]
TIER_3_SPORTS = [   # Moderate / prep-school favored — 2% each (T3 total = 10%)
    "Softball", "Squash", "Ice Hockey", "Field Hockey", "Wrestling",
]
TIER_4_SPORTS = [   # Niche — ~0.45% each (T4 total = 5%, split across 11)
    "Volleyball", "Cheerleading/Dance", "Ultimate Frisbee", "Water Polo",
    "Gymnastics", "Rugby", "Climbing", "Flag Football", "Badminton",
    "Pickleball", "Ping Pong",
]

# Concatenate into one ordered list and build a parallel weight list. Order
# is preserved across both lists, which random.choices() requires.
ALL_DROPDOWN_SPORTS = (
    TIER_1_SPORTS + TIER_2_SPORTS + TIER_3_SPORTS + TIER_4_SPORTS
)
DROPDOWN_WEIGHTS = (
    [0.12] * len(TIER_1_SPORTS)        # 5 × 0.12 = 0.60
    + [0.05] * len(TIER_2_SPORTS)      # 5 × 0.05 = 0.25
    + [0.02] * len(TIER_3_SPORTS)      # 5 × 0.02 = 0.10
    + [0.05 / len(TIER_4_SPORTS)] * len(TIER_4_SPORTS)  # 11 × ~0.00455 = 0.05
)
# Total weight = 1.00


# ============================================================================
# SECTION 3 — VARSITY SPORT DISTRIBUTION (proportional to Harvard team sizes)
# ============================================================================
# When a respondent is varsity, their sport is drawn proportional to the
# actual size of each Harvard varsity team. Sources: CollegeFactual EADA
# data (federal filings) supplemented with gocrimson.com roster scrapes
# for teams missing from the federal data (rowing, squash, sailing,
# skiing, cross country). Total = 1,217 athletes ≈ Harvard's stated ~1,200.
VARSITY_SPORT_WEIGHTS = [
    ("Track & Field",    267),  # M+W combined
    ("Football",         132),
    ("Men's Rowing",      87),  # heavyweight + lightweight
    ("Lacrosse",          80),  # M+W
    ("Swimming & Diving", 77),  # M+W
    ("Ice Hockey",        62),  # M+W
    ("Soccer",            60),  # M+W
    ("Women's Rowing",    44),
    ("Volleyball",        35),  # M+W
    ("Water Polo",        35),  # M+W
    ("Cross Country",     35),  # M+W
    ("Basketball",        34),  # M+W
    ("Baseball",          33),
    ("Wrestling",         33),
    ("Sailing",           30),  # combined coed
    ("Tennis",            29),  # M+W
    ("Squash",            27),  # M+W
    ("Fencing",           26),  # M+W
    ("Softball",          25),
    ("Skiing",            24),  # combined coed (alpine + nordic)
    ("Field Hockey",      24),  # W only
    ("Golf",              18),  # M+W
]


# ============================================================================
# COHERENCE MAPPING — varsity sport → Section 1 dropdown representation
# ============================================================================
# A current varsity athlete must list their sport in Section 1 at HS Varsity
# level (P=1.0). When the varsity sport is identical to a dropdown sport,
# the mapping is direct. When it's not in the 26-sport dropdown (Sailing,
# Fencing, Skiing, Golf), the respondent picks "Other" in the dropdown and
# writes the sport name into the specification field — for the CSV, we
# store the actual sport name in the slot to keep the schema flat.
# Chapter 5 — dictionary used as a lookup table.
VARSITY_TO_SECTION1_NAME = {
    "Track & Field":     "Track & Field",
    "Football":          "Football (American)",
    "Men's Rowing":      "Crew",       # Both rowing teams collapse to "Crew"
    "Women's Rowing":    "Crew",       # in the Section 1 dropdown
    "Lacrosse":          "Lacrosse",
    "Swimming & Diving": "Swimming",   # Dropdown lacks "& Diving"
    "Ice Hockey":        "Ice Hockey",
    "Soccer":            "Soccer",
    "Volleyball":        "Volleyball",
    "Water Polo":        "Water Polo",
    "Cross Country":     "Cross Country",
    "Basketball":        "Basketball",
    "Baseball":          "Baseball",
    "Wrestling":         "Wrestling",
    "Tennis":            "Tennis",
    "Squash":            "Squash",
    "Softball":          "Softball",
    "Field Hockey":      "Field Hockey",
    # The four below are NOT in the 26-sport dropdown. The respondent would
    # pick "Other" in the form; we store the actual name in the CSV slot.
    "Sailing":           "Sailing",
    "Fencing":           "Fencing",
    "Skiing":            "Skiing",
    "Golf":              "Golf",
}


# ============================================================================
# HELPER FUNCTIONS (Chapter 3 — modular function design)
# ============================================================================

def clip_to_skill_range(value):
    """Clip an integer to the valid skill rating range [1, 10]."""
    return max(1, min(10, value))


def sample_pre_college_sport_count():
    """Draw the number of pre-college sports a respondent will list.

    Locked distribution (capped at 3 since the form has only 3 slots):
        0 sports = 15%
        1 sport  = 35%
        2 sports = 30%
        3 sports = 20%

    The 3-sport bucket absorbs respondents who hypothetically played 4+
    sports — the form has no place to record more than 3, so they list
    their top 3.
    Chapter 3 — random.choices() weighted draw.
    """
    counts  = [0,    1,    2,    3   ]
    weights = [0.15, 0.35, 0.30, 0.20]
    return random.choices(counts, weights=weights, k=1)[0]


def sample_pre_college_sport(exclude=None):
    """Draw one sport from the 4-tier weighted dropdown distribution.

    The optional `exclude` argument is a set of sports already chosen for
    this respondent — those are filtered out before sampling so the same
    sport never appears twice in slots 1–3 (without-replacement semantics).

    Chapter 3 — random.choices(); Chapter 5 — set membership for exclusion.
    """
    if exclude is None:
        exclude = set()
    available = [
        (sport, weight)
        for sport, weight in zip(ALL_DROPDOWN_SPORTS, DROPDOWN_WEIGHTS)
        if sport not in exclude
    ]
    sports, weights = zip(*available)
    return random.choices(sports, weights=weights, k=1)[0]


def sample_pre_college_level():
    """Draw the highest level reached for one pre-college sport.

    Locked distribution (per-sport, applied independently to every slot):
        Casual     = 55%
        HS JV      = 10%
        HS Varsity = 35%
    Chapter 3 — random.choices() weighted draw.
    """
    levels  = ["Casual", "HS JV", "HS Varsity"]
    weights = [0.55,     0.10,    0.35       ]
    return random.choices(levels, weights=weights, k=1)[0]


def sample_skill_for_pre_college_level(level):
    """Draw a 1–10 skill rating conditional on the pre-college level.

    All distributions are normal(mean, sd=1.5), clipped to [1, 10]. The
    rounding convention differs by level to encode an asymmetric upward
    bias for the higher tiers (a strong HS Varsity player rounds UP, never
    down — this prevents the strong-player signal from being diluted by
    rounding):
        Casual     → normal(4.0, 1.5), standard rounding
        HS JV      → normal(5.0, 1.5), standard rounding
        HS Varsity → normal(7.5, 1.5), CEILING rounding (math.ceil)

    Chapter 3 — random.gauss(); Chapter 1 — round() vs math.ceil().
    """
    if level == "Casual":
        raw = random.gauss(4.0, 1.5)
        return clip_to_skill_range(round(raw))
    elif level == "HS JV":
        raw = random.gauss(5.0, 1.5)
        return clip_to_skill_range(round(raw))
    elif level == "HS Varsity":
        raw = random.gauss(7.5, 1.5)
        return clip_to_skill_range(math.ceil(raw))
    else:
        raise ValueError(f"Unknown pre-college level: {level!r}")


def sample_im_experience():
    """Draw an IM experience bucket for one (respondent, IM sport) pair.

    Locked distribution (uniform across all 19 IM sports):
        Never played = 75%
        1 season     = 20%
        2+ seasons   =  5%

    The 25% overall participation rate (20+5 = 25 historical players per
    sport) reflects the empirical House IM participation rate.
    Chapter 3 — random.choices().
    """
    buckets = ["Never played", "1 season", "2+ seasons"]
    weights = [0.75,            0.20,       0.05        ]
    return random.choices(buckets, weights=weights, k=1)[0]


def sample_im_skill(experience):
    """Draw a 1–10 IM skill rating conditional on the experience bucket.

    Returns None for 'Never played' (the form skips skill rating in that
    case). For experienced players, distributions are:
        1 season   → normal(5.25, 1.5), standard rounding
        2+ seasons → normal(6.5, 1.5), CEILING rounding
    Chapter 3 — random.gauss(); Chapter 1 — round() vs math.ceil().
    """
    if experience == "Never played":
        return None
    elif experience == "1 season":
        raw = random.gauss(5.25, 1.5)
        return clip_to_skill_range(round(raw))
    elif experience == "2+ seasons":
        raw = random.gauss(6.5, 1.5)
        return clip_to_skill_range(math.ceil(raw))
    else:
        raise ValueError(f"Unknown IM experience bucket: {experience!r}")


def sample_varsity_sport():
    """Draw one Harvard varsity sport, weighted by actual team size.
    Chapter 3 — random.choices() with non-normalized integer weights.
    """
    sports  = [name  for name,  count in VARSITY_SPORT_WEIGHTS]
    weights = [count for name,  count in VARSITY_SPORT_WEIGHTS]
    return random.choices(sports, weights=weights, k=1)[0]


# ============================================================================
# RESPONDENT GENERATOR (one full survey response)
# ============================================================================

def generate_respondent(respondent_id):
    """Build one respondent's full survey response as a flat dict.

    The order of operations is deliberate:
      1. Section 3 (varsity) — decided FIRST because it constrains Section 1
         via the coherence rule.
      2. Section 1 (pre-college) — slot 1 is forced for varsity athletes;
         remaining slots are sampled normally.
      3. Section 2 (IM experience) — independent per (respondent, sport).
    """
    # ----- Section 3: varsity status -----
    is_varsity = random.random() < P_VARSITY      # Bernoulli draw
    varsity_sport = sample_varsity_sport() if is_varsity else None

    # ----- Section 1: pre-college sports -----
    n_sports = sample_pre_college_sport_count()

    # Coherence: a varsity athlete MUST list their sport in Section 1.
    # If they happened to roll n_sports=0, force it up to 1.
    if is_varsity and n_sports == 0:
        n_sports = 1

    pre_college_slots = []     # List of dicts {sport, level, skill}
    used_sports = set()        # For without-replacement draws across slots

    if is_varsity:
        # Varsity coherence: slot 1 is forced — the varsity sport at HS
        # Varsity level. Map to the Section 1 dropdown name (or write-in).
        section1_name = VARSITY_TO_SECTION1_NAME[varsity_sport]
        pre_college_slots.append({
            "sport": section1_name,
            "level": "HS Varsity",
            "skill": sample_skill_for_pre_college_level("HS Varsity"),
        })
        used_sports.add(section1_name)

    # Fill remaining slots up to n_sports using the normal tiered
    # distribution, excluding any sport already used.
    remaining_slots = n_sports - len(pre_college_slots)
    for _ in range(remaining_slots):
        sport = sample_pre_college_sport(exclude=used_sports)
        used_sports.add(sport)
        level = sample_pre_college_level()
        skill = sample_skill_for_pre_college_level(level)
        pre_college_slots.append({
            "sport": sport,
            "level": level,
            "skill": skill,
        })

    # Pad to exactly 3 slots so the CSV has consistent columns
    while len(pre_college_slots) < 3:
        pre_college_slots.append({"sport": "", "level": "", "skill": ""})

    # ----- Section 2: per-IM-sport experience and skill -----
    section2_data = {}
    for im_sport in IM_SPORTS:
        experience = sample_im_experience()
        skill = sample_im_skill(experience)
        # Use sanitized column names (lowercase, underscores) so the parser
        # has a predictable schema. Chapter 1 — string formatting.
        col_key = im_sport.lower().replace(" ", "_")
        section2_data[f"im_{col_key}_experience"] = experience
        section2_data[f"im_{col_key}_skill"] = "" if skill is None else skill

    # ----- Assemble the full row dict (Chapter 5 — dict composition) -----
    row = {
        "respondent_id": respondent_id,
        "pre_college_sport_1":       pre_college_slots[0]["sport"],
        "pre_college_sport_1_level": pre_college_slots[0]["level"],
        "pre_college_sport_1_skill": pre_college_slots[0]["skill"],
        "pre_college_sport_2":       pre_college_slots[1]["sport"],
        "pre_college_sport_2_level": pre_college_slots[1]["level"],
        "pre_college_sport_2_skill": pre_college_slots[1]["skill"],
        "pre_college_sport_3":       pre_college_slots[2]["sport"],
        "pre_college_sport_3_level": pre_college_slots[2]["level"],
        "pre_college_sport_3_skill": pre_college_slots[2]["skill"],
    }
    row.update(section2_data)
    row["is_varsity"]   = "yes" if is_varsity else "no"
    row["varsity_sport"] = varsity_sport if is_varsity else ""

    return row


# ============================================================================
# CSV WRITER (Chapter 1 — file I/O via csv.DictWriter)
# ============================================================================

def write_responses_csv(rows, output_path):
    """Write all respondent dicts to a CSV file."""
    if not rows:
        return
    fieldnames = list(rows[0].keys())
    parent_dir = os.path.dirname(output_path)
    if parent_dir:
        os.makedirs(parent_dir, exist_ok=True)
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

def main():
    """Generate N_RESPONDENTS rows, write to OUTPUT_PATH, print sanity stats."""
    rows = [generate_respondent(i) for i in range(1, N_RESPONDENTS + 1)]
    write_responses_csv(rows, OUTPUT_PATH)

    # ----- Sanity stats -----
    n = len(rows)
    n_varsity = sum(1 for r in rows if r["is_varsity"] == "yes")

    varsity_by_sport = {}
    for r in rows:
        if r["is_varsity"] == "yes":
            sport = r["varsity_sport"]
            varsity_by_sport[sport] = varsity_by_sport.get(sport, 0) + 1

    free_level_counts   = {"Casual": 0, "HS JV": 0, "HS Varsity": 0}
    forced_level_counts = {"Casual": 0, "HS JV": 0, "HS Varsity": 0}
    for r in rows:
        is_varsity_resp = r["is_varsity"] == "yes"
        for slot_idx in (1, 2, 3):
            level = r[f"pre_college_sport_{slot_idx}_level"]
            if level not in free_level_counts:
                continue
            if is_varsity_resp and slot_idx == 1:
                forced_level_counts[level] += 1
            else:
                free_level_counts[level] += 1
    total_free   = sum(free_level_counts.values())
    total_forced = sum(forced_level_counts.values())

    im_buckets = {"Never played": 0, "1 season": 0, "2+ seasons": 0}
    for r in rows:
        for im_sport in IM_SPORTS:
            col_key = im_sport.lower().replace(" ", "_")
            bucket = r[f"im_{col_key}_experience"]
            im_buckets[bucket] += 1
    total_im = sum(im_buckets.values())

    print(f"Generated {n} responses → {OUTPUT_PATH}")
    print(f"  Varsity rate: {n_varsity}/{n} = {n_varsity/n:.1%} (target 20.0%)")
    print()
    print(f"  Pre-college level breakdown — FREE slots only ({total_free}):")
    print(f"    (Excludes slot 1 of varsity athletes, which is always forced "
          f"to HS Varsity)")
    for level, count in free_level_counts.items():
        target = {"Casual": 0.55, "HS JV": 0.10, "HS Varsity": 0.35}[level]
        pct = count / total_free if total_free else 0
        print(f"    {level:11s}: {count:4d} ({pct:.1%}) [target {target:.0%}]")
    print(f"  Forced HS Varsity slots (varsity-coherence): {total_forced}")
    print()
    print(f"  IM experience breakdown ({total_im} sport-respondent pairs):")
    for bucket, count in im_buckets.items():
        target = {"Never played": 0.75, "1 season": 0.20,
                  "2+ seasons": 0.05}[bucket]
        print(f"    {bucket:13s}: {count:5d} ({count/total_im:.1%}) "
              f"[target {target:.0%}]")
    print()
    print(f"  Varsity sport breakdown ({n_varsity} varsity respondents):")
    for sport, count in sorted(varsity_by_sport.items(),
                               key=lambda kv: -kv[1]):
        print(f"    {sport:22s}: {count}")


if __name__ == "__main__":
    main()
