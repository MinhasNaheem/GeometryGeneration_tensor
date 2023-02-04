from functions import compute_intermarker

import pandas as pd

df = pd.read_csv('Values.csv')

arr = df[['xx','yy','zz']].to_numpy()

imd = compute_intermarker(arr,len(arr))
print(imd)