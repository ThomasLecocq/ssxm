import matplotlib.pyplot as plt
import pandas as pd
from obspy import read

from ssxm import ssxm


# CONFIG
rule = "30S"
bands = [[0.1, 1.0], [1.0, 5.0], [5.0, 10.0]] # in Hz
percentiles = [10, 95]


# Read a trace
st = read("BE.MEM..HHZ.D.2017.010")

st.detrend("demean")

# array holding results, much faster than appending on the fly
rsam = []
# select component
Z = st.select(component="Z")
for tr in Z:
    data =  tr.data
    fs = tr.stats.sampling_rate
    starttime = tr.stats.starttime.datetime

    tmp = ssxm(data, fs, id, starttime, rule=rule, bands=bands, percentiles=percentiles)
    rsam.append(tmp)

# merging the array holding results now
rsam = pd.concat(rsam)

# grouping by "bands" and names
bands = rsam.groupby('band')
nbands = len(bands)

# plotting all bands
plt.figure(figsize=(10, 8))
i = 1
for id, band in bands:
    ax = plt.subplot(nbands, 1, i)
    band.plot(ax=ax)
    plt.title(id)
    plt.xlabel("")
    plt.legend(ncol=4)
    i += 1
plt.tight_layout()
plt.show()
