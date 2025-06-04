#%% CSV Einlesen und in dataframe speichern

import pandas as pd

def find_peaks(df_ekg : pd.DataFrame, threshold : float, min_peak_distance : int):
    """
    A Function that takes a DataFrame and returns a list of index-positions of the peaks"""

    list_of_index_of_peaks = []

    last_peaks_index = 0

    for index, row in df_ekg.iterrows():
        if index < df_ekg.index.max() -1:

        # wenn row["Voltage in mV"] größer als das vorhergehenden und das folgende
            if row["Voltage in mV"] >= df_ekg.iloc[index-1]["Voltage in mV"] and row ["Voltage in mV"] >= df_ekg.iloc[index+1]["Voltage in mV"]:
            # dann füge den aktuellen index zur Liste hinzu

                # Wenn der Threshold überschritten wird und auch der letzte gespeicherte index mindestens den abstand hat
                if row["Voltage in mV"] > threshold and index - last_peaks_index > min_peak_distance:
                    list_of_index_of_peaks.append(index)
                    last_peaks_index = index

    return list_of_index_of_peaks


#%%

if __name__ == "__main__":

    df_ekg = pd.read_csv("../data/ekg_data/01_Ruhe.txt", sep = "	", names = ["Voltage in mV", "Time in s"])
    df_ekg = df_ekg.iloc[0:5000]

    threshold = 0.95 * df_ekg["Voltage in mV"].max()  # Dynamischer Schwellenwert basierend auf dem Maximum des Signals
    min_peak_distance = 10
        
    list_of_index_of_peaks = find_peaks(df_ekg, threshold, min_peak_distance)

    # plot the row["Voltage in mV"] and mark the peaks with red dots
    import plotly.express as plx
    fig = plx.line(df_ekg, x = df_ekg.index, y = "Voltage in mV", title = "EKG Signal with Peaks")
    fig.add_scatter(x = list_of_index_of_peaks, y = df_ekg.iloc[list_of_index_of_peaks]["Voltage in mV"], mode = "markers", marker = dict(color = "red", size = 10), name = "Peaks")
    fig.update_layout(xaxis_title = "Index", yaxis_title = "Voltage in mV")
    fig.show()

# %%
