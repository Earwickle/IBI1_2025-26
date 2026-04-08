# Required Python modules
import datetime
import random
import numpy as np

# Calculate heart rate average and standard deviation
heart_rates = np.array([72, 60, 126, 85, 90, 59, 76, 131, 88, 121, 64])
average_rate = np.mean(heart_rates)
standard_dev = np.std(heart_rates)

# Scotland population = 5,463,300 (2019)
# Zhejiang population = 64,567,588 (2020)
# 78,497 at ZJU in 2024
sample_sizes = {'Scotland': 5463300, 'Zhejiang':64567588}

for population in sample_sizes:
	sample_size = sample_sizes[population]
	sampled_rates = []

	# Record the start time
	start_time = datetime.datetime.now().replace(microsecond=0)

	# Simulate the entire population using observed data
	for rep in range(0,sample_size):
		sampled_rates.append(random.normalvariate(mu=average_rate, sigma=standard_dev))
	end_time = datetime.datetime.now().replace(microsecond=0)

	# How long did the simulation take to run?
	duration = (end_time - start_time)

	# Print output
	print(population, ':', duration)