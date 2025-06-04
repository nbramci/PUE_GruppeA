# Import necessary libraries
import pandas as pd

PATH = "data/activities/activity.csv"


def analyze_hr_data(max_hr):
    import pandas as pd
    from plotly import express as px
    df = pd.read_csv(PATH)
    df["Zone"] = None
    # Herzfrequenz-Zonen berechnen
    hr_zones = {}
    counter = 1
    for percent in range(50, 100, 10):
        hr_zones["Zone"+str(counter)] = max_hr * percent/100
        counter = counter + 1
    # Zonen zuordnen
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
    df["Zone"] = current_zone
    df["Time"] = df.index
    # Plotly Shapes für Zonen
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
    fig = px.line(df, x="Time", y="HeartRate", title="Herzfrequenz über Zeit")
    fig.update_layout(
        xaxis_title="Time",
        yaxis_title="Herzfrequenz (bpm)",
        template="plotly_white",
        shapes=shapes
    )
    # Zonenstatistik
    zone_counts = df["Zone"].value_counts().sort_index()
    intervall_in_sekunden = 1
    intervall_in_minuten = intervall_in_sekunden / 60
    time_per_zone_minutes = zone_counts * intervall_in_minuten
    formatted_time = time_per_zone_minutes.apply(lambda x: f"{int(x):02d}:{int((x % 1) * 60):02d}")
    avg_power_per_zone = df.groupby("Zone")["PowerOriginal"].mean().sort_index()
    avg_hr_per_zone = df.groupby("Zone")["HeartRate"].mean().sort_index()
    zone_summary_df = pd.DataFrame({
        "Zeit pro Zone [Min:Sek]": formatted_time,
        "⌀ Leistung pro Zone [W]": avg_power_per_zone,
        "⌀ Herzfrequenz pro Zone [bpm]": avg_hr_per_zone
    })
    print("Leistungswerte (W):")
    print("Mean Power in W", df["PowerOriginal"].mean())
    print("Max Power in W", df["PowerOriginal"].max())
    print("Min Power in W", df["PowerOriginal"].min())
    return df, fig, zone_summary_df

if __name__ == "__main__":
    analyze_hr_data(max_hr=200)