#Open JSON File and load data
import json
import os
from PIL import Image

#example usage
FILE_PATH = "data/person_db.json"
DEFAULT_IMAGE =  "data/pictures/none.jpg"

# Definition einer Personenklasse

class Person():

    def __init__(self, id : int, date_of_birth : str, firstname : str, lastname : str, picture_path : str, ekg_tests, gender = "unknown"):
        self.id = id
        self.date_of_birth = date_of_birth
        self.firstname = firstname
        self.lastname = lastname
        self.picture_path = picture_path
        self.ekg_tests = ekg_tests
        self.gender = gender

    def get_full_name(self):
        return self.lastname + ", " + self.firstname

    def calc_age(self):
        from datetime import datetime
        current_year = datetime.now().year
        return current_year - int(self.date_of_birth)

    def calc_max_heart_rate(self):
        age = self.calc_age()
        if hasattr(self, "gender") and self.gender.lower() == "female":
            return 226 - age
        return 220 - age

    @classmethod
    def load_by_id(cls, id, db):
        for person in db:
            if person.id == id:
                return person
        raise ValueError(f"Person mit ID {id} nicht gefunden.")


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

def get_person_object_from_list_by_name(current_user_name, users):
    firstname = current_user_name.split(", ")[1]
    lastname = current_user_name.split(", ")[0]

    for person in users:
        if person.firstname == firstname and person.lastname == lastname:
            return person
        else:
            None


if __name__ == "__main__":
    
    person_list = load_user_objects(FILE_PATH)
    
    print(person_list)