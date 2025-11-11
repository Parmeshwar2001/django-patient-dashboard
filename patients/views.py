from pymongo import MongoClient
from django.shortcuts import render


def get_db_handle():
    client = MongoClient("mongodb://localhost:27017/")
    db = client["patient_db"]
    collection = db["patients"]
    return collection

def patient_list(request):
    client = MongoClient("mongodb://localhost:27017/")
    db = client["patient_db"]
    collection = db["patients"]

    data = list(collection.find({}, {"_id": 0}))

    total_patients = len(data)
    male_count = len([d for d in data if d.get("GENDER") == "M"])
    female_count = len([d for d in data if d.get("GENDER") == "F"])

    # Count patients per state
    state_counts = {}
    for d in data:
        state = d.get("STATE", "Unknown")
        state_counts[state] = state_counts.get(state, 0) + 1

    # Unique states and genders for dropdowns
    states = sorted(list({d.get("STATE", "Unknown") for d in data}))
    genders = sorted(list({d.get("GENDER", "Unknown") for d in data}))

    context = {
        "patients": data,
        "total_patients": total_patients,
        "male_count": male_count,
        "female_count": female_count,
        "state_counts": state_counts,
        "states": states,
        "genders": genders,
    }

    return render(request, "patients/patient_list.html", context)