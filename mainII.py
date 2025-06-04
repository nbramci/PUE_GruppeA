import pandas as pd
import matplotlib.pyplot as plt
from src.power_curveII import calculate_power_curve

# Daten laden
df = pd.read_csv("data/activities/activity.csv")
df["PowerOriginal"] = pd.to_numeric(df["PowerOriginal"], errors='coerce')
df = df.dropna(subset=["PowerOriginal"])

# Power-Curve berechnen
power_curve_df = calculate_power_curve(df["PowerOriginal"].values, resolution=1)

# Plot erstellen
plt.figure(figsize=(10, 5))
plt.plot(power_curve_df["Duration_s"], power_curve_df["AvgPower_Watt"])
plt.xlabel("Dauer (Sekunden)")
plt.ylabel("Durchschnittliche Leistung (Watt)")
plt.title("Power-Curve")
plt.grid(True)
plt.tight_layout()
plt.show()