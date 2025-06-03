#%%
# Import necessary libraries
import pandas as pd



#%%
# Load the HR data in eine Tabelle

# Absoluter Pfad zur Datei
PATH = "/Users/niklasbrandstetter/Documents/VS Projects/Semester 2/Programmierübung 2/Noah_Brandi/PUE_GruppeA/data/activities/activity.csv"

df = pd.read_csv(PATH)

print(df.head())

print(list(df.columns))  # Zeigt die echten Spaltennamen an


print("Loading HR data...")
#%%
df[["Distance", "HeartRate", "CalculatedPace"]]

#%%
df["HeartRate"].max()
df["HeartRate"].min()
df["HeartRate"].mean()

#%%
df["HeartRate"].plot()

#%%
df["HeartRate"] > 180

df["Zone 5"] = df["HeartRate"] > 180

df["Zone 5"].sum()

#%%
df["Zone 5"].value_counts()

#%%
df

#%%
df.iloc[0,3]

#%%
df.index

#%%
zone5 = df["Zone 5"].mean()
zone5

#%%
df_zone5 = df.groupby("Zone 5").mean()

#%%
df_zone5["HeartRate"]

#%%
df["HeartRate"]

#%%

print("Mean Power in W:", df["PowerOriginal"].mean())
print("Minimum Power in W:", df["PowerOriginal"].mean())
print("Maximum Power in W:", df["PowerOriginal"].mean())

#%%
df["Zone"] = None
df

#%%

max_hr = 200

#%%
hr_zones = {}
counter = 1
for percent in range(50,100,10):
    print(percent/100)
    hr_zones["Zone"+str(counter)] = max_hr * percent/100
    counter = counter + 1

hr_zones

#%%
df["Zone"] = None
df

#%%

current_zone = []
for _, row in df.iterrows():
    current_hr = row["HeartRate"]

    if current_hr > hr_zones["Zone5"]:
        current_zone.append("Zone 5")
    elif current_hr > hr_zones["Zone4"]:
        current_zone.append("Zone 4")
    elif current_hr > hr_zones["Zone3"]:
        current_zone.append("Zone 3")
    elif current_hr > hr_zones["Zone2"]:
        current_zone.append("Zone 2")
    else: 
        current_zone.append("Zone 1")
        
current_zone

#%%
df["Zone"] = current_zone
df["Zone"].value_counts()
   
#%%
df_zone5 = df.groupby("Zone").mean()
df_zone5

# %%

#%%
# Import necessary libraries
import pandas as pd



#%%
# Load the HR data in eine Tabelle

# Absoluter Pfad zur Datei
PATH = "/Users/niklasbrandstetter/Documents/VS Projects/Semester 2/Programmierübung 2/Noah_Brandi/PUE_GruppeA/data/activities/activity.csv"

df = pd.read_csv(PATH)

print(df.head())

print(list(df.columns))  # Zeigt die echten Spaltennamen an


print("Loading HR data...")
#%%
df[["Distance", "HeartRate", "CalculatedPace"]]

#%%
df["HeartRate"].max()
df["HeartRate"].min()
df["HeartRate"].mean()

#%%
df["HeartRate"].plot()

#%%
df["HeartRate"] > 180

df["Zone 5"] = df["HeartRate"] > 180

df["Zone 5"].sum()

#%%
df["Zone 5"].value_counts()

#%%
df

#%%
df.iloc[0,3]

#%%
df.index

#%%
zone5 = df["Zone 5"].mean()
zone5

#%%
df_zone5 = df.groupby("Zone 5").mean()

#%%
df_zone5["HeartRate"]

#%%
df["HeartRate"]

#%%

print("Mean Power in W:", df["PowerOriginal"].mean())
print("Minimum Power in W:", df["PowerOriginal"].mean())
print("Maximum Power in W:", df["PowerOriginal"].mean())

#%%
df["Zone"] = None
df

#%%

max_hr = 200

#%%
hr_zones = {}
counter = 1
for percent in range(50,100,10):
    print(percent/100)
    hr_zones["Zone"+str(counter)] = max_hr * percent/100
    counter = counter + 1

hr_zones

#%%
df["Zone"] = None
df

#%%

current_zone = []
for _, row in df.iterrows():
    current_hr = row["HeartRate"]

    if current_hr > hr_zones["Zone5"]:
        current_zone.append("Zone 5")
    elif current_hr > hr_zones["Zone4"]:
        current_zone.append("Zone 4")
    elif current_hr > hr_zones["Zone3"]:
        current_zone.append("Zone 3")
    elif current_hr > hr_zones["Zone2"]:
        current_zone.append("Zone 2")
    else: 
        current_zone.append("Zone 1")
        
current_zone

#%%
df["Zone"] = current_zone
df["Zone"].value_counts()
   
#%%
df_zone5 = df.groupby("Zone").mean()
df_zone5

# %%

df["Time"] = df.index
from plotly import express as px
# Create background shapes for HR zones
shapes = []
zone_colors = ["#d0f0c0", "#addfad", "#ffd700", "#ffa07a", "#ff4500"]
zone_thresholds = [hr_zones["Zone1"], hr_zones["Zone2"], hr_zones["Zone3"], hr_zones["Zone4"], hr_zones["Zone5"], max_hr]

for i in range(5):
    shapes.append(dict(
        type="rect",
        xref="paper",
        yref="y",
        x0=0,
        x1=1,
        y0=zone_thresholds[i],
        y1=zone_thresholds[i+1],
        fillcolor=zone_colors[i],
        opacity=0.5,
        layer="below",
        line_width=0,
    ))
# Plotting the Heart Rate data with Plotly
fig = px.line(df, x="Time", y="HeartRate", title="Heart Rate Over Time")
fig.update_layout(
    xaxis_title="Time",
    yaxis_title="Heart Rate (bpm)",
    template="plotly_white",
    shapes=shapes
)
fig.show()


# %%
# Anzahl Messpunkte pro Zone
zone_counts = df["Zone"].value_counts().sort_index()
intervall_in_sekunden = 1  # Wenn jede Sekunde eine Messung aufgezeichnet wurde
intervall_in_minuten = intervall_in_sekunden / 60

# Dauer in Minuten pro Zone
time_per_zone_minutes = zone_counts * intervall_in_minuten

# Zeitformat MM:SS
formatted_time = time_per_zone_minutes.apply(lambda x: f"{int(x):02d}:{int((x % 1) * 60):02d}")

# Durchschnittliche Leistung je Zone
avg_power_per_zone = df.groupby("Zone")["PowerOriginal"].mean().sort_index()

# Zusammenführen in DataFrame
zone_summary_df = pd.DataFrame({
    "TimeInZone": formatted_time,
    "AveragePower": avg_power_per_zone
})

print("Zusammenfassung nach Herzfrequenz-Zonen:")
print(zone_summary_df)

# %%
