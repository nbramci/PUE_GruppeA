import streamlit as st
from src.read_person_data import load_user_objects, get_person_object_from_list_by_name
from PIL import Image
import pandas as pd
from plotly import express as px
from src.analyze_hr_data import analyze_hr_data


# -------------------- Session-Initialisierung --------------------
#sicherstellen, dass die Session-Variable existiert
if "current_user" not in st.session_state:
    st.session_state.current_user_name = "NONE"
if "current_user_name" not in st.session_state:
    st.session_state.current_user_name = "NONE"

# -------------------- Benutzerdaten laden --------------------
FILE_PATH = "data/person_db.json"
user_data = load_user_objects(FILE_PATH)
name_list = [user.get_full_name() for user in user_data]


# -------------------- Benutzeroberfläche: Versuchsperson auswählen --------------------
#Eine Überschrift der ersten Ebene
st.title("EKG-APP")

#Eine Überschrift der zweiten Ebene
st.write("# Versuchsperson auswählen")

#Auswahlbox
st.session_state["current_user_name"] = st.selectbox(
    "Wählen Sie eine Versuchsperson aus",
    options = name_list, key = "sbVersuchsperson")

st.write("aktuelle Versuchsperson: ", st.session_state["current_user_name"])

st.session_state["current_user"] = get_person_object_from_list_by_name(st.session_state["current_user_name"], user_data)

st.image(st.session_state["current_user"].picture_path, caption=st.session_state["current_user"].get_full_name())
st.markdown(f"**ID der Versuchsperson:** `{st.session_state['current_user'].id}`")

# -------------------- Benutzerinformationen anzeigen --------------------
# Alter und maximale Herzfrequenz anzeigen
st.write(f"Alter: {st.session_state['current_user'].calc_age()} Jahre")
st.write(f"Maximale Herzfrequenz (geschätzt): {st.session_state['current_user'].calc_max_heart_rate()} bpm")

# -------------------- Aktivitätsdaten analysieren --------------------
#Daten anzeigen
st.write("# Analyse der Aktivitätsdaten")

#Maximale Herzfrequenz eingeben
max_hr = st.number_input("Bitte maximale Herzfrequenz eingeben:", min_value=60, max_value=300, value=200, step=1)

#Daten analysieren und Plot erstellen
df, fig, zone_summary_df = analyze_hr_data(max_hr)

st.plotly_chart(fig, use_container_width=True)

st.write("Zusammenfassung nach Herzfrequenz-Zonen:")
st.dataframe(zone_summary_df)

# -------------------- EKG-Tests analysieren --------------------
# EKG-Tests visuelle und funktionale Einbindung
from src.ekgdata import EKGdata

st.write("# Analyse eines EKG-Tests")

ekg_tests = st.session_state["current_user"].ekg_tests
if ekg_tests:
    ekg_options = {f"Test {i+1} am {t['date']}": t["id"] for i, t in enumerate(ekg_tests)}
    selected_label = st.selectbox("Wählen Sie einen EKG-Test", list(ekg_options.keys()))
    selected_id = ekg_options[selected_label]

    ekg = EKGdata.load_by_id(selected_id, user_data)
    ekg.find_peaks()
    if ekg.time_was_corrected:
        st.warning("Hinweis: In der ausgewählten EKG-Datei wurden fehlerhafte Zeitstempel erkannt. Diese wurden automatisch korrigiert. Die Ergebnisse können dennoch Ungenauigkeiten enthalten.")
    estimated_hr = ekg.estimate_hr()
    ekg.plot_time_series()

    st.plotly_chart(ekg.fig, use_container_width=True)
    st.write(f"Geschätzte Herzfrequenz aus dem EKG: {round(estimated_hr)} bpm")
else:
    st.info("Keine EKG-Daten für diese Person verfügbar.")

# -------------------- Herzfrequenz-Verlauf visualisieren --------------------
# Herzfrequenz-Verlauf anzeigen
st.write("## Herzfrequenz-Verlauf")
hr_fig = ekg.plot_hr_over_time()
st.plotly_chart(hr_fig, use_container_width=True)