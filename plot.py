import json
from datetime import datetime
import matplotlib.pyplot as plt

with open("data.json", "r") as f:
    data = f.readlines()

timestamp = []
viterbi = []
reed_solomon = []
skipped_symbols = []
gain = []
frequency = []
omega = []

for line in data:
    element = json.loads(line)
    timestamp.append(datetime.fromisoformat(element["timestamp"]))
    viterbi.append(element["viterbi_errors"])
    reed_solomon.append(element["reed_solomon_errors"])
    skipped_symbols.append(element["skipped_symbols"])
    gain.append(element["gain"])
    frequency.append(element["frequency"])
    omega.append(element["omega"])


nrows = 2
ncols = 2
fig = plt.figure()
axes = [ fig.add_subplot(nrows, ncols, r * ncols + c + 1) for r in range(0, nrows) for c in range(0, ncols) ]

axes[0].plot(timestamp, viterbi)
axes[1].plot(timestamp, reed_solomon, timestamp, skipped_symbols)
axes[2].plot(timestamp, gain, timestamp, omega)
axes[3].plot(timestamp, frequency)

#plt.xticks(rotation=90)
axes[0].set_xticks([])
axes[0].set_ylabel('Viterbi Errors')
axes[1].set_xticks([])
axes[1].set_ylabel('Reed Solomon Errors (blue)\nSkipped Symbols (orange)')
axes[2].set_xlabel('Time')
axes[2].set_ylabel('Gain (blue)\nOmega (orange)')
axes[3].set_xlabel('Time')
axes[3].set_ylabel('Frequency OffSet (Hz)')
plt.show()
