import numpy as np
from functions import plot_fids

import pandas as pd

df = pd.read_csv('correct.csv')

pos = df[['x','y','z']].to_numpy()

fig =plot_fids(pos*100)
fig.show()
