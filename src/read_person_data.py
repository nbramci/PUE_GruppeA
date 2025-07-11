import json
import os
from .person import Person  # Relativer Modulimport

# -------------------- Personenbezogene Datenverarbeitung --------------------

# Lädt alle Benutzer:innen aus einer JSON-Datei und erstellt Person-Objekte
def load_user_objects(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")

    with open(file_path, 'r') as file:
        data = json.load(file)

    person_list = []
    for person_person_dict in data:
        current_person = Person(person_person_dict["id"],
                                person_person_dict["date_of_birth"],
                                person_person_dict["firstname"],
                                person_person_dict["lastname"],
                                person_person_dict["picture_path"],
                                person_person_dict["ekg_tests"],
                                person_person_dict.get("gender", "unknown"))
        person_list.append(current_person)

    return person_list

# Sucht ein bestimmtes Person-Objekt aus der Liste anhand des Namens
def get_person_object_from_list_by_name(current_user_name, users):
    firstname = current_user_name.split(", ")[1]
    lastname = current_user_name.split(", ")[0]

    for person in users:
        if person.firstname == firstname and person.lastname == lastname:
            return person
        else:
            None