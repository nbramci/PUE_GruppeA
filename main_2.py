import pandas as pd
import numpy as np
from src.power_curve_2 import power_curve

# CSV-Datei einlesen
df = pd.read_csv("data/activities/activity.csv")

# Leistungswerte als Array extrahieren
power_array = np.array(df["PowerOriginal"])

# Leistungskurve berechnen und anzeigen
power_curve(power_array)