#w24024373 erinroserine
import random
import json
import string
from datetime import datetime, timedelta


# ---------------- BASIC OPTIONS ----------------

GENDERS = ["Male", "Female"]
CATEGORIES = ["A", "B", "C", "D"]
PRISONS = ["HMP Durham", "HMP Frankland", "HMP Low Newton", "HMP Holme House"]

DISABILITIES = ["None", "Autism", "ADHD", "Dyslexia", "Blindness", "Physical disability"]
MENTAL_HEALTH = ["None", "Depression", "Anxiety", "PTSD"]
RELIGIONS = ["None", "Christian", "Muslim", "Hindu", "Sikh"]
BUS_ROUTES = ["22", "18", "34a", "56"]
UK_CITIES = ["Newcastle", "Durham", "Sunderland", "Middlesbrough"]

RHU_LIST = ["Safe Haven", "Durham house", "Safe Haven"]
EMPLOYMENT_OPTIONS = ["Job centre", "College", "Industrial estate", "None"]
TRIGGERS = ["None", "Gambling", "Pubs", "Certain areas"]


# ---------------- HELPER FUNCTIONS ----------------

def random_name():
    first = ["James", "Sarah", "John", "Emily", "Michael", "Aisha"]
    last = ["Smith", "Brown", "Taylor", "Wilson", "Johnson"]
    return random.choice(first) + " " + random.choice(last)


def random_address():
    num = random.randint(1, 200)
    street = random.choice(["High Street", "Church Road", "Station Road"])
    city = random.choice(UK_CITIES)
    postcode = "NE" + str(random.randint(1, 9)) + random.choice(string.ascii_uppercase)
    return f"{num} {street}, {city}, {postcode}"


def random_dates():
    release = datetime.now() + timedelta(days=random.randint(-30, 180))
    licence_days = random.choice([90, 180, 365, 730])
    end = release + timedelta(days=licence_days)
    return release.strftime("%Y-%m-%d"), end.strftime("%Y-%m-%d"), licence_days


def random_coords():
    return {
        "lat": round(random.uniform(54.5, 55.2), 5),
        "lon": round(random.uniform(-2.0, -1.3), 5)
    }


# ---------------- MAIN RECORD ----------------

def generate_licensee():
    release_date, end_date, licence_days = random_dates()
    status = random.choice(["Pending", "Allocated", "Exited"])

    return {
        # -------- PERSONAL INFORMATION --------
        "name": random_name(),
        "prison_role_id": f"PR{random.randint(100000, 999999)}",
        "gender": random.choice(GENDERS),
        "release_date": release_date,
        "end_of_licence": end_date,
        "current_location": random.choice(PRISONS),
        "category": random.choice(CATEGORIES),
        "home_address": random_address(),
        "photo": None,

        # -------- MATCHING ATTRIBUTES --------
        "security_category": random.choice(CATEGORIES),
        "night_curfew": random.choice([True, False]),
        "weekend_curfew": random.choice([True, False]),
        "victim_exclusion_zones": [random_coords() for _ in range(random.randint(0, 2))],
        "school_exclusion_distance_m": random.choice([0, 500, 1000, 1500]),
        "excluded_prisoners": random.choice(
            ["None", random_name(), random_name() + ", " + random_name()]
        ),
        "disability": random.choice(DISABILITIES),
        "accessibility_needs": random.choice([True, False]),
        "general_exclusion_zone": random.choice(["None", "City centre", "Specific streets"]),
        "drug_search_required": random.choice([True, False]),
        "associate_restrictions": random.choice(
            ["None", random_name(), random_name() + " (no contact)"]
        ),
        "young_offender_suitable": random.choice([True, False]),
        "medical_access_needed": random.choice(
            ["None", "A&E", "Mental health clinic", "Specialist care"]
        ),
        "transport_links_needed": random.sample(BUS_ROUTES, random.randint(1, 3)),
        "religious_needs": random.choice(RELIGIONS),
        "mental_health_needs": random.choice(MENTAL_HEALTH),
        "family_access_location": random.choice(UK_CITIES),
        "prior_rhu_experience": random.choice(["None"] + RHU_LIST),
        "employment_or_training": random.choice(EMPLOYMENT_OPTIONS),
        "offending_triggers": random.choice(TRIGGERS),
        "licence_period_days": licence_days,

        # -------- FUTURE EXPANSION --------
        "future_expansion_1": random.choice(["Option A", "Option B", "None"]),
        "future_expansion_2": random.randint(0, 100),
        "future_expansion_3": random.choice(["TBD", "N/A"]),

        # -------- STUDENT SUGGESTED  --------
        "pet_therapy": random.choice(["Yes", "No", "Preferred"]),
        "support_level": random.choice(
            ["High", "Medium", "Low", "Independent"]
        ),

        # -------- NOTES --------
        "notes": random.choice([
            "No concerns",
            "Requires monitoring",
            "Settling well",
            "Needs additional support"
        ]),

        # -------- STATUS INFO --------
        "status": status,
        "current_rhu": random.choice(RHU_LIST) if status == "Allocated" else None,
        "days_until_housing": random.randint(1, 60) if status == "Pending" else None,
        "days_until_exit": random.randint(1, 365) if status == "Allocated" else None
    }


# ---------------- DATASET ----------------

def generate_dataset(count=1000):
    return [generate_licensee() for _ in range(count)]


if __name__ == "__main__":
    data = generate_dataset(1000)

    with open("prison_housing_data.json", "w") as f:
        json.dump(data, f, indent=2)

    print("Dataset generated")
    print("Sample record:")
    print(json.dumps(data[0], indent=2))