from datetime import datetime

class Person:
    def __init__(self, id: int, date_of_birth: str, firstname: str, lastname: str, picture_path: str, ekg_tests, gender="unknown"):
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