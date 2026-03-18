import numpy as np       
import matplotlib.pyplot as plt  

N = 10  
x = np.random.rand(N)
y = np.random.rand(N)
plt.scatter(x, y, marker='o')
plt.show()
