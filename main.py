import streamlit as st
from src.load_user_data import get_image, load_user_data, get_all_names
from PIL import Image
import pandas as pd
from plotly import express as px
from src.analyze_hr_data import analyze_hr_data


#sicherstellen, dass die Session-Variable existiert
if "current_user" not in st.session_state:
    st.session_state.current_user = ""

FILE_PATH = "data/person_db.json"
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

#Daten anzeigen
st.write("# Analyse der Aktivitätsdaten")

#Maximale Herzfrequenz eingeben
max_hr = st.number_input("Bitte maximale Herzfrequenz eingeben:", min_value=60, max_value=300, value=200, step=1)

#Daten analysieren und Plot erstellen
df, fig, zone_summary_df = analyze_hr_data(max_hr)

st.plotly_chart(fig, use_container_width=True)

st.write("Zusammenfassung nach Herzfrequenz-Zonen:")
st.dataframe(zone_summary_df)