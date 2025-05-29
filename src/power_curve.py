import matplotlib.pyplot as plt
import numpy as np
from sort import bubble_sort
from load_data import load_data
from datetime import datetime

#Zuständig damit die Daten im richtigen Ordner gefunden werden 
import os
here = os.path.dirname(__file__)
data_path = os.path.join(here, '..', 'data', 'activity.csv')
data = load_data(data_path)

power_W = data['PowerOriginal']
N_steps = len(power_W)
Time = np.arange(N_steps)
sorted_power = bubble_sort(power_W)


plt.figure(figsize=(10, 6))
plt.plot(sorted_power[::-1])
plt.xlabel('Time(s)')
plt.ylabel('Power (W)')
plt.title('Power Curve')
plt.savefig('figures/power_curve.png')
plt.show()