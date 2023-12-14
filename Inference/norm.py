import numpy as np
from scipy.stats import norm



# Your data
data = [12, 14, 15, 18, 19, 20, 22, 24, 25, 30, 32, 35, 36, 40, 42, 45, 50, 55, 60]

# Fit Gaussian distribution
mean = np.mean(data)
std_dev = np.std(data)

# Calculate the 95th percentile
percentile_95 = norm.ppf(0.95, loc=mean, scale=std_dev)

# Filter data points above the 95th percentile
data_above_95th_percentile = [x for x in data if x > percentile_95]

print("Data points above the 95th percentile:", data_above_95th_percentile)
