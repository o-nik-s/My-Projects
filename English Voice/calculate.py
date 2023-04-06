import math
import pandas as pd

p = lambda x: round(math.log(x*100,25)**2,0)

def calculate_p(data):
    data["p"] = data.freq.apply(p).astype(int)    
    data["sumP"] = 0
    sumP = 0
    for i in range(len(data)):
        sumP += data.iloc[i, 2]
        data.iloc[i, 3] = sumP
    return data