import streamlit as st
from src.load_user_data import get_image, load_user_data, get_all_names
from PIL import Image


#sicherstellen, dass die Session-Variable existiert
if "current_user" not in st.session_state:
    st.session_state.current_user = ""

FILE_PATH = "data/person_db.json"  # Replace with your actual file path
user_data = load_user_data(FILE_PATH)
name_list = get_all_names(user_data)


#Eine Überschrift der ersten Ebene
st.title("EKG-APP")

#Eine Überschrift der zweiten Ebene
st.write("# Versuchsperson auswählen")

#Auswahlbox
st.session_state.current_user = st.selectbox(
    "Wählen Sie eine Versuchsperson aus",
    options = name_list, key = "sbVersuchsperson")

st.write("aktuelle Versuchsperson: ", st.session_state.current_user)


#Bild mit Caption anzeigen
st.image(get_image(st.session_state.current_user), caption=st.session_state.current_user)