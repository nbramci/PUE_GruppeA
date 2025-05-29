import numpy as np
from sort import bubble_sort
import matplotlib.pyplot as plt # type: ignore

def load_data(file_path):
    """
    Lädt eine CSV-Datei mit numerischen Spaltennamen und gibt die Daten als Dictionary zurück.
    :param file_path: Pfad zur CSV-Datei
    :return: Dictionary mit Spaltennamen als Schlüssel und NumPy-Arrays als Werte
    """
    data_array = np.genfromtxt(file_path, delimiter=',', dtype=None, names=True, encoding='utf-8')
    return {column: data_array[column] for column in data_array.dtype.names}



if __name__ == "__main__":
    data = load_data('data/activity.csv')
    power_W = data['PowerOriginal']
    print(power_W)
    sorted_power_W = bubble_sort(power_W)
    print(sorted_power_W[::-1])