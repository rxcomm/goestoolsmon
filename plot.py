import json
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib as mpt

mpt.style.use('bmh')
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

axes[0].plot(timestamp, viterbi, 'C0', label="Viterbi Errors")
axes[1].plot(timestamp, reed_solomon, 'C0', label="Reed Solomon Errors")
axes[1].plot(timestamp, skipped_symbols, 'C2', label="Skipped Symbols")
axes[2].plot(timestamp, gain, 'C0', label="Costas Loop Gain")
axes[2].plot(timestamp, omega, 'C2', label="Costas Loop Bandwidth")
axes[3].plot(timestamp, frequency, 'C0', label="Frequency Offset")

for ax in fig.get_axes():
    #ax.label_outer()
    ax.legend()
plt.setp(axes[0].get_xticklabels(), visible=False)
plt.setp(axes[1].get_xticklabels(), visible=False)

#plt.xticks(rotation=90)
axes[0].set_ylabel('Counts per packet')
#axes[0].set_ylim([100,300])
axes[1].set_ylabel('Counts per packet')
axes[1].set_ylim([-0.1,8.1])
axes[2].set_xlabel('Time (DD HH:MM)')
axes[2].set_ylabel('Gain (V/V)\nBandwidth (Hz)')
axes[2].set_ylim([0,8])
axes[3].set_xlabel('Time (DD HH:MM)')
axes[3].set_ylabel('Frequency (Hz)')

plt.subplots_adjust(top=0.985, bottom=0.057, left=0.038, right=0.983, hspace=0.051, wspace=0.126)
fig.text(.5, .01, 'One Second Average Performance', ha='center', fontsize=14)
plt.show()
