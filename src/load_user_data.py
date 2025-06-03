#Open JSON File and load data
import json
import os
from PIL import Image

#example usage
FILE_PATH = "data\person_db.json"  # Replace with your actual file path

def load_user_data(file_path):
    """
    Load user data from a JSON file.

    Args:
        file_path (str): Path to the JSON file.

    Returns:
        dict: User data loaded from the JSON file.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")
    
    with open(file_path, 'r') as f:
        user_data = json.load(f)
    
    return user_data

def get_all_names(user_data):
    """
    Extract all user names from the user data.
    """
    user_names = []
    #gehe durch alle Einträge in der JSON-Datei
    for person_dict in user_data:
         #füge den firstname zu den user_names hinzu

        user_names.append(person_dict['lastname']+ ", "+ person_dict['firstname'])
    return user_names

def get_image(person_name):
    image_path = get_image_path(person_name)
    image = Image.open(image_path)
    return image

def get_image_path(current_user):
    """
    Get the image path for a given person name.
    """
    firstname = current_user.split(", ")[1]
    lastname = current_user.split(", ")[0]
    user_data = load_user_data(FILE_PATH)

    for person_dict in user_data:
        if person_dict['firstname'] == firstname and person_dict['lastname'] == lastname:
            path_to_image = person_dict['picture_path']
    return path_to_image

if __name__ == "__main__":
    user_data = load_user_data(FILE_PATH)
    print(user_data)
    name_list = get_all_names(user_data)
    print(name_list)
