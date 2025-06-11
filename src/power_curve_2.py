import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.io as pio

# Setze Plotly Renderer auf Browser
pio.renderers.default = "browser"


def power_curve(power_array: np.ndarray, interval_seconds: float = 1.0) -> pd.DataFrame:
    # NaN-Werte entfernen
    power_array = power_array[~np.isnan(power_array)]
    
    # Schwellenwerte definieren (z. B. 0–max Leistung in 5-W-Schritten)
    max_power = np.max(power_array)
    thresholds = np.arange(0, max_power + 5, 5)
    
    times_over_threshold = [np.sum(power_array > threshold) * interval_seconds for threshold in thresholds]
    
    df_curve = pd.DataFrame({
        "Power (W)": thresholds,
        "Time over Threshold (s)": times_over_threshold
    })

    # Interaktives Plotly-Diagramm erstellen
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df_curve["Time over Threshold (s)"],
        y=df_curve["Power (W)"],
        mode="lines+markers",
        marker=dict(size=6),
        line=dict(width=2),
        name="Power-Curve"
    ))
    fig.update_layout(
        title="Zeit über Leistungsschwelle",
        xaxis_title="Zeit (s)",
        yaxis_title="Leistung (W)",
        hovermode="x unified"
    )
    fig.show()

    return df_curve