import json
import pandas as pd
import plotly.express as px

# -------------------- Klasse zur EKG-Datenverarbeitung --------------------

# Klasse EKG-Data für Peakfinder, die uns ermöglicht peaks zu finden

class EKGdata:

    # EKG-Test aus der Datenbank laden anhand der ID
    @staticmethod
    def load_by_id(id, db):
        for person in db:
            for ekg_dict in person.ekg_tests:
                if ekg_dict["id"] == id:
                    return EKGdata(ekg_dict)
        raise ValueError(f"EKG-Test mit ID {id} nicht gefunden.")

    # Konstruktor: EKG-Daten laden und vorbereiten
    def __init__(self, ekg_dict):
        self.time_was_corrected = False

        self.id = ekg_dict["id"]
        self.date = ekg_dict["date"]
        self.data = ekg_dict["result_link"]
        self.df = pd.read_csv(self.data, sep='\t', header=None, names=['Messwerte in mV','Zeit in ms',])
        self.df = self.df.dropna()
        self.df = self.df[self.df["Messwerte in mV"].between(100, 1500)]
        self.df = self.df[self.df["Messwerte in mV"] > 100]

        # Zeitreihe korrigieren, wenn sie zurückspringt
        zeit_diff = self.df["Zeit in ms"].diff()
        reset_index = zeit_diff[zeit_diff < 0].index

        if not reset_index.empty:
            start_idx = reset_index[0]
            offset = self.df.loc[start_idx - 1, "Zeit in ms"] + 1
            self.df.loc[start_idx:, "Zeit in ms"] += offset
            self.time_was_corrected = True

    # Peaks (Herzschläge) im EKG-Signal finden
    def find_peaks(self):
        from scipy.signal import find_peaks
        peaks, _ = find_peaks(self.df["Messwerte in mV"], height=330, distance=200, prominence=0.9)
        self.peaks = peaks

    # Mittlere Herzfrequenz basierend auf den Peaks berechnen
    def estimate_hr(self):
        if not hasattr(self, "peaks"):
            raise ValueError("Peaks wurden noch nicht gefunden. Bitte zuerst find_peaks() aufrufen.")
        peak_times = self.df["Zeit in ms"].iloc[self.peaks].values / 1000  # in Sekunden
        rr_intervals = peak_times[1:] - peak_times[:-1]
        avg_rr = rr_intervals.mean()
        self.estimated_hr = 60 / avg_rr if avg_rr > 0 else 0
        return self.estimated_hr

    # EKG-Zeitreihe als Plot darstellen
    def plot_time_series(self):
        visible_df = self.df.head(5000)
        fig = px.line(visible_df, x="Zeit in ms", y="Messwerte in mV", title="EKG-Zeitreihe")
        if hasattr(self, "peaks"):
            visible_peaks = [p for p in self.peaks if p < len(visible_df)]
            peak_df = visible_df.iloc[visible_peaks]
            fig.add_scatter(x=peak_df["Zeit in ms"], y=peak_df["Messwerte in mV"],
                            mode='markers', marker=dict(color='red', size=6), name="Peaks")
        self.fig = fig
        return fig
    
    # Herzfrequenz-Verlauf über die Zeit berechnen und visualisieren
    def plot_hr_over_time(self):
        if not hasattr(self, "peaks"):
            raise ValueError("Bitte zuerst find_peaks() aufrufen.")

        peak_times = self.df["Zeit in ms"].iloc[self.peaks].values / 1000  # in Sekunden
        rr_intervals = peak_times[1:] - peak_times[:-1]
        hr_values = 60 / rr_intervals

        # Zeitpunkte für die HR-Werte: Mittelpunkt der Intervalle
        time_points = (peak_times[1:] + peak_times[:-1]) / 2

        hr_df = pd.DataFrame({"Zeit (s)": time_points, "Herzfrequenz (bpm)": hr_values})
        fig = px.line(hr_df, x="Zeit (s)", y="Herzfrequenz (bpm)", title="Herzfrequenz über die Zeit")
        return fig


# Testlauf bei direktem Ausführen dieser Datei
if __name__ == "__main__":
    print("This is a module with some functions to read the EKG data")
    file = open("data/person_db.json")
    person_data = json.load(file)
    ekg_dict = person_data[0]["ekg_tests"][0]
    print(ekg_dict)
    ekg = EKGdata(ekg_dict)
    print(ekg.df.head())
