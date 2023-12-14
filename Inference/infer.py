import json
import numpy as np
from scipy.stats import norm


mapping = {}
log_file = 'stock_values.log'
with open(log_file, 'r') as file:
    lines = file.readlines()
    last_300_lines = lines[-15000:]
    for line in last_300_lines:
        data = json.loads(line)
        if data['payload'][0]['symbol'] in mapping:
            mapping[data['payload'][0]['symbol']].append(data['payload'][2])
        else:
            mapping[data['payload'][0]['symbol']] = [data['payload'][2]]


# print(mapping)
for key in mapping:
    value = mapping[key]
    new_val = []
    
    prev = value[0]
    for val in value[1:]:
        new_val.append(val - prev)
        prev = val
    mapping[key] = new_val


reverse_mapping = {}
data = []
for key, value in mapping.items():
    # print(len(value))
    data.extend(value)
    for val in value:
        if val in reverse_mapping:
            reverse_mapping[val].append(key)
        else:
            reverse_mapping[val] = [key]
# print(reverse_mapping)
# print(data)



# Fit Gaussian distribution
mean = np.mean(data)
std_dev = np.std(data)
percentile_95 = norm.ppf(0.95, loc=mean, scale=std_dev)
data_above_95th_percentile = [x for x in data if x > percentile_95]
Symbols = []
for val in data_above_95th_percentile:
    Symbols.extend(reverse_mapping[val])
Symbols = list(set(Symbols))
print(Symbols)
