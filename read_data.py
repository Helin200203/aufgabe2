import pandas as pd
import json

def read_my_csv(file_path="activity.csv"):
    column_names = ["HeartRate", "Duration", "PowerOriginal"]
    df = pd.read_csv(file_path, sep=",", header=0, usecols=column_names)
    df["Duration"] = df.index
    return df

def load_person_data(file_path="data/person_db.json"):
    """Eine Funktion, die weiß, wo die Personendatenbank ist, und ein Wörterbuch mit den Personen zurückgibt."""
    with open(file_path, "r") as file:
        person_data = json.load(file)
    return person_data

def get_person_list(file_path="data/person_db.json"):
    """Eine Funktion, die eine Liste von Personen zurückgibt."""
    person_data = load_person_data(file_path)
    return [f"{person['lastname']}, {person['firstname']}" for person in person_data]

def find_person_data_by_name(suchstring, file_path="data/person_db.json"):
    """Eine Funktion, der Nachname, Vorname als ein String übergeben wird und die die Person als Dictionary zurückgibt."""
    person_data = load_person_data(file_path)
    
    if suchstring == "None":
        return {}

    try:
        lastname, firstname = suchstring.split(", ")
    except ValueError:
        return {}

    for person in person_data:
        if person["lastname"] == lastname and person["firstname"] == firstname:
            return person

    return {}
