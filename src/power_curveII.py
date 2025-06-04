import numpy as np
import pandas as pd

def calculate_power_curve(power_data, resolution=1):
    """
    Berechnet die Power-Curve (max. Durchschnittsleistung über Zeitintervalle).
    
    Args:
        power_data (array-like): Leistungsdaten in Watt.
        resolution (int): Zeitliche Auflösung in Sekunden (Standard: 1 Sekunde).

    Returns:
        pd.DataFrame: DataFrame mit 'Duration_s' und 'AvgPower_Watt'.
    """
    power_array = np.array(power_data)
    n = len(power_array)
    results = []

    for window in range(1, n + 1):
        rolling_avg = pd.Series(power_array).rolling(window=window).mean()
        max_avg = rolling_avg.max()
        duration = window * resolution
        results.append((duration, max_avg))

    df_result = pd.DataFrame(results, columns=["Duration_s", "AvgPower_Watt"])
    return df_result